"""
Sphinx plugin to run example scripts and create a gallery page.

Lightly modified from the mpld3 project.

"""
from __future__ import division
import os
import os.path as op
import re
import glob
import token
import tokenize
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



RST_TEMPLATE = """
.. _{sphinx_tag}:

{docstring}

.. image:: {img_file}

**Python source code:** :download:`[download source: {fname}]<{fname}>`

.. literalinclude:: {fname}
    :lines: {end_line}-
"""


def indent(s, N=4):
    """indent a string"""
    return s.replace('\n', '\n' + N * ' ')


class ExampleGenerator(object):
    """Tools for generating an example page from a file"""
    def __init__(self, filename, target_dir):
        self.filename = filename
        self.target_dir = target_dir
        self.extract_docstring()
        with open(filename, "r") as fid:
            self.filetext = fid.read()

        outfilename = op.join(target_dir, self.rstfilename)

        # Only actually run it if the output RST file doesn't
        # exist or it was modified less recently than the example
        if (not op.exists(outfilename) or
                (op.getmtime(outfilename) < op.getmtime(filename))):

            self.exec_file()
        else:

            print("skipping {0}".format(self.filename))

    @property
    def dirname(self):
        return op.split(self.filename)[0]

    @property
    def fname(self):
        return op.split(self.filename)[1]

    @property
    def modulename(self):
        return op.splitext(self.fname)[0]

    @property
    def pyfilename(self):
        return self.modulename + '.py'

    @property
    def rstfilename(self):
        return self.modulename + ".rst"

    @property
    def htmlfilename(self):
        return self.modulename + '.html'

    @property
    def pngfilename(self):
        pngfile = self.modulename + '.png'
        return "_static/" + pngfile

    @property
    def sphinxtag(self):
        return self.modulename

    @property
    def pagetitle(self):
        return self.docstring.strip().split('\n')[0].strip()

    @property
    def plotfunc(self):
        match = re.search(r"msme\.(plot+\w+)\(", self.filetext)
        if match:
            return match.group(1)
        match = re.search(r"msme\.(.+map)\(", self.filetext)
        if match:
            return match.group(1)
        match = re.search(r"msme\.(.+Grid)\(", self.filetext)
        if match:
            return match.group(1)
        return ""

    def extract_docstring(self):
        """ Extract a module-level docstring
        """
        lines = open(self.filename).readlines()
        start_row = 0
        if lines[0].startswith('#!'):
            lines.pop(0)
            start_row = 1

        docstring = ''
        first_par = ''
        tokens = tokenize.generate_tokens(lines.__iter__().__next__)
        for tok_type, tok_content, _, (erow, _), _ in tokens:
            tok_type = token.tok_name[tok_type]
            if tok_type in ('NEWLINE', 'COMMENT', 'NL', 'INDENT', 'DEDENT'):
                continue
            elif tok_type == 'STRING':
                docstring = eval(tok_content)
                # If the docstring is formatted with several paragraphs,
                # extract the first one:
                paragraphs = '\n'.join(line.rstrip()
                                       for line in docstring.split('\n')
                                       ).split('\n\n')
                if len(paragraphs) > 0:
                    first_par = paragraphs[0]
            break

        self.docstring = docstring
        self.short_desc = first_par
        self.end_line = erow + 1 + start_row

    def exec_file(self):
        print("running {0}".format(self.filename))

        plt.close('all')
        my_globals = {'pl': plt,
                      'plt': plt}
        exec(compile(open(self.filename, "rb").read(), self.filename, 'exec'), my_globals)

        fig = plt.gcf()
        fig.canvas.draw()
        pngfile = op.join(self.target_dir, self.pngfilename)
        self.html = '<img src=../%s>' % self.pngfilename
        fig.savefig(pngfile, dpi=75, bbox_inches="tight")

    def toctree_entry(self):
        return "   ./%s\n\n" % op.splitext(self.htmlfilename)[0]


def main(app):
    static_dir = op.join(app.builder.srcdir, '_static')
    target_dir = op.join(app.builder.srcdir, '.')
    image_dir = op.join(app.builder.srcdir, '_static')
    source_dir = op.abspath(op.join(app.builder.srcdir,
                                              '..', 'examples'))
    if not op.exists(static_dir):
        os.makedirs(static_dir)

    if not op.exists(target_dir):
        os.makedirs(target_dir)

    if not op.exists(image_dir):
        os.makedirs(image_dir)

    if not op.exists(source_dir):
        os.makedirs(source_dir)

    banner_data = []

    toctree = ("\n\n"
               ".. toctree::\n"
               "   :hidden:\n\n")
    contents = "\n\n"

    # Write individual example files
    for filename in glob.glob(op.join(source_dir, "colors.py")):

        ex = ExampleGenerator(filename, target_dir)

        banner_data.append({"title": ex.pagetitle,
                            "url": op.join('examples', ex.htmlfilename),
                            })
        shutil.copyfile(filename, op.join(target_dir, ex.pyfilename))
        output = RST_TEMPLATE.format(sphinx_tag=ex.sphinxtag,
                                     docstring=ex.docstring,
                                     end_line=ex.end_line,
                                     fname=ex.pyfilename,
                                     img_file=ex.pngfilename)
        with open(op.join(target_dir, ex.rstfilename), 'w') as f:
            f.write(output)

        toctree += ex.toctree_entry()
    if len(banner_data) < 10:
        banner_data = (4 * banner_data)[:10]


def setup(app):
    app.connect('builder-inited', main)

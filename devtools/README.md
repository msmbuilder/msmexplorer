Developer Notes / Tools
=======================

How to do a release
-------------------

### Pre-release

- Tag issues and pull requests with a milestone for the particular version.
- Use the "changelog" tag to tag pull requests that need to be recorded in `docs/changelog.rst`.
  You've been encouraging people to update the changelog *with* their pull requests, though, right?
- Update `docs/changelog.rst`. Change the tag from "changelog" to "changelogged".
- Optionally create an issue about cutting the release.
- Fix and close all open issues and PRs with the release's milestone.

### Release

- `git checkout master && git fetch origin && git reset --hard origin/master`
- `git clean -fdx`
- Update the version number in `setup.py`, change `ISRELEASED` to `True`.
- Verify the version number in `devtools/conda-recipe/meta.yaml` is "0.0.0".
- Add the date of release to `docs/changelog.rst`, add a blurb.
- Commit and push to master. The commit should only include the version number changes and
  should be given a message like "Release x.y.z".
- Tag that commit on GitHub. For version x.y.z, the tag should be `x.y.z` (no "v" prefix)
  and the title should be "MSMExplorer x.y" (no .z). You should copy-paste the changelog entry
  for the GitHub release notes. Beware of the transition from `rst` to markdown. In particular,
  you might have to change the headings from underlined to prefixed with `##`. You should
  also delete "hard-wrap" linebreaks because GitHub will keep them in! (and you don't want
  that). Use the preview tab.
- The docs will build. Make sure this is successful and they are live at msmbuilder.org/msmexplorer.
  The docs will be sent to msmbuilder.org/msmexplorer/x.y.z instead of development/ because you
  set `ISRELEASED`. You can cancel the Travis build triggered by the "tag" because docs
  are set to deploy only from `master`.
- Verify that `versions.json` was updated properly.
- Create the canonical source distribution using `python setup.py sdist --formats=gztar,zip`.
  Inspect the files in dist/ to make sure they look right.
- Upload to PyPI using `twine upload [path to sdist files]`.
- File a pull request against the
  [conda-recipes](https://github.com/omnia-md/conda-recipes) repository.
  Use the PyPI link as the "source". Make sure the requirements match those
  in the msmexplorer recipe in `devtools/conda-recipe`. We don't want the package
  that gets tested with every pull request to differ from the one people actually get!
  Conda binaries should be automatically built.
- Make an announcement on the mailing list.

### Post-release

- Update the version number in `setup.py`, change `ISRELEASED` to `False`.
- Verify the version number in `devtools/conda-recipe/meta.yaml` is "0.0.0".
- Add a new "development" entry in `docs/changelog.rst`.
- Commit and push to master.
- Make sure there is a x.(y+1) milestone already created
- Create a new x.(y+2) milestone [y is still the value of the release you just did]
- Close the x.y milestone.
- Update this file (`devtools/README.md`) with anything you learned or
  changed during this release creation.
- Open an Issue for x.(y+1) release schedule.

### Point releases

If you want to include a minor or important fix, you can create a point release.
For version x.y.z, this would mean bumping `z`.

- `git checkout x.y.0` (the tag)
- `git checkout -b x.y` (make x.y branch)
- Make a commit that updates the versions, isreleased in setup.py and conda recipe.
  This time, change to `x.y.(z+1).dev0` instead of `x.(y+1).0.dev0`
- `git push origin x.y -u`
- Backport or cherry-pick the fixes you need.
- Go through the above for creating a release. Make sure you tag
  the commit on the x.y branch. If you don't want release notes
  (e.g. for a really minor fix), you can create an unannotated tag.

```
vim: tw=90
```

import warnings

import numpy as np
from matplotlib.pyplot import close

# Show warnings for our package
warnings.filterwarnings('always', module='msmbuilder.*')

# Show warnings for packages where we want to be conscious of warnings
warnings.filterwarnings('always', module='mdtraj.*')
warnings.filterwarnings('always', module='scipy.*')
warnings.filterwarnings('always', module='nglview.*')
warnings.filterwarnings('always', module='matplotlib.*')
warnings.filterwarnings('always', module='seaborn.*')


class PlotTestCase(object):

    def setUp(self):
        np.random.seed(42)

    def tearDown(self):
        close('all')

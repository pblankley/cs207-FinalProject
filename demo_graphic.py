import numpy as np
import chemkin207 as ck
import os

import matplotlib as mpl
#if os.environ.get('DISPLAY','') == '':
#    print('no display found. Using non-interactive Agg backend')
#    mpl.use('Agg')
import matplotlib.pyplot as plt

# create a reaction set from the chemkin207 module
demo_reaction = ck.ReactionSet("demo_xmls/rxns_reversible.xml")
concs = np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5]).reshape(-1, 1)

# plot a single query specie
demo_reaction.plot('H2O2', concs, 1500, 3000)

# plot a list of query species
demo_reaction.plot(['O2','H2'], concs, 1500, 3000)
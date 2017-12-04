import numpy as np
import chemkin207 as ck
import os


# create a reaction set from the chemkin207 module
demo_reaction = ck.ReactionSet("demo_xmls/rxns_reversible.xml")
concs = np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5]).reshape(-1, 1)

# Table output - txt
demo_reaction.to_table('H2O2', concs, temps = [1500],
                       out_file = './tables/txt_table', out_type = 'txt')

# Table output - latex
demo_reaction.to_table(['O2','H2'], concs, temps = [1000, 2000, 3000],
                       out_file = './tables/latex_table', out_type = 'latex')

# Table output - csv
demo_reaction.to_table(['O2','H2', 'OH'], concs, temps = np.linspace(3000, 3500, 51),
                       out_file = './tables/csv_table', out_type = 'csv')

# Table output - hdf5
demo_reaction.to_table(['O2','H2', 'OH'], concs, temps = np.linspace(3000, 3500, 20),
                       out_file = './tables/hdf5_table', out_type = 'hdf5')
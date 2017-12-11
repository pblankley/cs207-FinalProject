import numpy as np
import chemkin207 as ck
import os


# create a reaction set from the chemkin207 module
demo_reaction = ck.ReactionSet("demo_xmls/rxns_reversible.xml")
demo_reaction2 = ck.ReactionSet("demo_xmls/rxns.xml")

concs = np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5])

# Single table output - txt
demo_reaction.to_table('H2O2', concs, temps = [1500],
                       out_file = './tables/txt_table', out_type = 'txt')

# Single table output - latex
demo_reaction.to_table(['O2','H2'], concs, temps = [1000, 2000, 3000],
                       out_file = './tables/latex_table', out_type = 'latex')

# Single table output - csv
demo_reaction.to_table(['O2','H2', 'OH'], concs, temps = np.linspace(3000, 3500, 51),
                       out_file = './tables/csv_table', out_type = 'csv')

# Single table output - hdf5
demo_reaction.to_table(['O2','H2', 'OH'], concs, temps = np.linspace(3000, 3500, 20),
                       out_file = './tables/hdf5_table', out_type = 'hdf5')

# Multi table output - csv
concs_multi = [np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5]),
        np.array([3.0, 0.1, 0.05, 1.5, 2.25, 0.33])]

multi_reaction = ck.MultiReactionOutput([demo_reaction, demo_reaction2])
multi_reaction.to_table_multi(['O2', 'OH'], concs=concs_multi, temps = [1500, 2500, 3500],
                              output_dir = './tables/multi_demo', out_type = 'csv')

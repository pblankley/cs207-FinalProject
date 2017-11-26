import numpy as np
import chemkin207 as ck

# create a reaction set from the chemkin207 module
demo_reaction = ck.ReactionSet("demo_xmls/rxns_reversible.xml")
concs = np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5]).reshape(-1, 1)

min_rate = demo_reaction.find_rates('H2', concs, 1500, 2000, precision = 100, type = 'min')
print('H2 min rates {} at occured at temperature {}'.format(min_rate[0], min_rate[1]))

query_species = ['H2','O2']
print('{} max rates: {} with corresponding temperatures'
      .format(query_species, demo_reaction.find_rates(query_species, concs, 1500, 2000, precision = 100, type = 'max')))


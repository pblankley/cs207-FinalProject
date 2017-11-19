#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16

@author: ryanjanssen
"""

import numpy as np
import chemkin as ck
import os

import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


# Demo of chemkin module
# Parses rxns.xml and calculates chemical reaction rates for each of the six species

# Pull data from .xml file, and set concentration rates
demo_reaction = ck.ReactionSet("demo_xmls/rxns_reversible.xml")
concs = np.array([2.0, 1.0, .5, 1.0, 1.0, 1.0, 0.5, 1.5]).reshape(-1, 1)

# Calculate reaction rates vs T
T_range = np.arange(1500,3000)

# Plot the rates against the temperature
rates_plot = np.zeros((len(T_range), len(concs)))
for i, T in enumerate(T_range):
    rates_plot[i,:] = demo_reaction.reaction_rates(concs, T)

# Plot the 6 reaction rates
for i, specie in enumerate(demo_reaction.species):
    plt.plot(T_range,rates_plot[:,i], label = specie)

# Print out the parameters
#print('Parameters for the demo reaction : {}'.format(demo_reaction.get_params()))

# Print out the reaction rates for each specie
reaction_rates = demo_reaction.reaction_rates(concs, 1500)
print('The reaction rate for each specie at Temperature {} : '.format(1500))
for index, specie in enumerate(demo_reaction.get_params()['species']):
    print('specie {} : {}'.format(specie, reaction_rates[index]))

plt.xlabel("Temperature (K)")
plt.ylabel("Reaction rate")
plt.title("Reaction rate of each specie")
plt.legend()
plt.show()

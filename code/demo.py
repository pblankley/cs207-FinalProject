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
demo_reaction = ck.ReactionSet("demo_xmls/rxns.xml")
concs = np.array([2.0, 1.0, 2.0, 0.5, 1.5, 2.5]).reshape(-1, 1)

print(demo_reaction)
 
# Calculate reaction rates vs T
T_range = np.arange(1273,5273)

rates_plot = np.zeros((len(T_range), len(concs)))
for i, T in enumerate(T_range):
    rates_plot[i,:] = demo_reaction.reaction_rates(concs, T)

# Plot the 6 reaction rates
for i, specie in enumerate(demo_reaction.species):
    plt.plot(T_range,rates_plot[:,i], label = specie)

plt.xlabel("Temperature (K)")
plt.ylabel("Reaction rate")
plt.title("Reaction rate of each specie")
plt.legend()
plt.show()
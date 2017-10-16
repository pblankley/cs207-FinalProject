#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16

@author: ryanjanssen
"""
import numpy as np

# !!! Adding this here temporarily until we figure out the import bug
def get_reactions(name):
    """ This function takes in the name of the input xml file, and returns a dictionary of relevant information for
        a set of chemical reactions
    ------
    Args: name: name of the input xml file
    ------
    Returns: reaction_dict, dictionary of data for a reaction.  Contains the following keys:
             reaction_dict['species'] : list of strings, species of the reaction
             reaction_dict['As']: list of floats, corresponding to reaction parameter A for each equation
                                           = NaN for any equations that don't use A.
             reaction_dict['bs']: list of floats, corresponding to reaction parameter b for each equation
                                           = NaN for any equations that don't use b.
             reaction_dict['Es']: list of floats, corresponding to reaction parameter E for each equation
                                           = NaN for any equations that don't use E.
             reaction_dict['ks']: list of floats, corresponding to reaction parameter k for each equation
                                           = NaN for any equations that don't use k (ie, non-constant equations).
             reaction_dict['rxn_types']: List of strings. Elements Correspond to same reactions as reaction_parameters.
                                           Each string is one of { 'Arrhenius', 'modifiedArrhenius', 'Constant' }
             reaction_dict['vprime'] : np array, full vprime matrix of all reactions in the xml file
             reaction_dict['v2prime'] : np array, full v2prime matrix of all reactions in the xml file
    """
    reaction_dict = {}
    tree = ET.parse(name)
    chemical_reactions = tree.getroot()
    if chemical_reactions == []:
        raise ValueError('Unable to locate reaction data in xml')

    # Get the list and number of species
    species_list = []
    for ele in chemical_reactions.iter('phase'):
        for e in ele.find('speciesArray').text.split():
            species_list.append(e)
    reaction_dict['species'] = species_list
    if species_list == []:
        raise ValueError('Invalid species list in xml')

    # Get the reaction rate types and parameters for each reaction
    As, bs, Es, ks = [], [], [], []
    rxn_types = []

    reactions_list = chemical_reactions.find('reactionData').findall('reaction')
    if reactions_list == []:
        raise ValueError('Invalid reactions list in xml')

    for reaction_data in reactions_list:
        for coeff_set in reaction_data.find('rateCoeff'):
            rxn_types.append(coeff_set.tag)
            if coeff_set.tag == 'Arrhenius':
                As.append(float(coeff_set.find('A').text))
                bs.append(float('nan'))
                Es.append(float(coeff_set.find('E').text))
                ks.append(float('nan'))
            elif coeff_set.tag == 'modifiedArrhenius':
                As.append(float(coeff_set.find('A').text))
                bs.append(float(coeff_set.find('b').text))
                Es.append(float(coeff_set.find('E').text))
                ks.append(float('nan'))
            elif coeff_set.tag == 'Constant':
                As.append(float('nan'))
                bs.append(float('nan'))
                Es.append(float('nan'))
                ks.append(float(coeff_set.find('k').text))

    reaction_dict['As'], reaction_dict['bs'], reaction_dict['Es'], reaction_dict['ks'] = As, bs, Es, ks
    reaction_dict['rxn_types'] = rxn_types

    # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
    vprime = np.zeros((len(species_list), len(reactions_list)))
    reaction_count = 0

    for reaction_data in chemical_reactions.find('reactionData').findall('reaction'):
        # Find the reactants data
        reactants_text = reaction_data.find('reactants').text

        # Split the data
        for specie_concentration in reactants_text.split(' '):

            # Get the name of the specie and its concentration
            specie = specie_concentration.split(':')[0]
            concentration = float(specie_concentration.split(':')[1])
            vprime[species_list.index(specie)][reaction_count] = concentration # Update at the index

        # Move to the next equation
        reaction_count += 1

    reaction_dict['vprime'] = vprime

    # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
    v2prime = np.zeros((len(species_list), len(reactions_list)))
    reaction_count = 0

    for reaction_data in chemical_reactions.find('reactionData').findall('reaction'):

        # Find the reactants data
        products_text = reaction_data.find('products').text

        # Split the data
        for specie_concentration in products_text.split(' '):

            # Get the name of the specie and its concentration
            specie = specie_concentration.split(':')[0]
            concentration = float(specie_concentration.split(':')[1])
            v2prime[species_list.index(specie)][reaction_count] = concentration  # Update at the index

    reaction_dict['v2prime'] = v2prime

    # Move to the next equation
    reaction_count += 1

    return reaction_dict


# Testing suite for XML parser.
# NOTE: Requires accompanying XML test suite to be places in \test_xmls to function properly

def test_working_xml():
    # Test a standard output
    expected_dict = {'species': ['H', 'O', 'OH', 'H2', 'H2O', 'O2'],
                     'As': [35200000000.0, 0.0506, float('nan')],
                     'bs': [float('nan'), 2.7, float('nan')],
                     'Es': [71400.0, 26300.0, float('nan')],
                     'ks': [float('nan'), float('nan'), 1000.0],
                     'rxn_types': ['Arrhenius', 'modifiedArrhenius', 'Constant'],
                     'vprime': np.array([[ 1.,  0.,  0.],
                                      [ 0.,  1.,  0.],
                                      [ 0.,  0.,  1.],
                                      [ 0.,  1.,  1.],
                                      [ 0.,  0.,  0.],
                                      [ 1.,  0.,  0.]]),
                     'v2prime': np.array([[ 1.,  0.,  0.],
                                      [ 1.,  0.,  0.],
                                      [ 1.,  0.,  0.],
                                      [ 0.,  0.,  0.],
                                      [ 1.,  0.,  0.],
                                      [ 0.,  0.,  0.]])}
    assert (get_reactions('test_xmls/rxns.xml') == expected_dict)


test_working_xml()


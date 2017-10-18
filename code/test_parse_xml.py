#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16

@author: ryanjanssen
"""
import numpy as np
import chemkin as ck

# Testing suite for XML parser.
# NOTE: Requires accompanying XML test suite to be places in \test_xmls to function properly

def test_working_xml():
    # Test a standard output
    expected_dict = {'species': ['H', 'O', 'OH', 'H2', 'H2O', 'O2'],
                     'A': [35200000000.0, 0.0506, float('nan')],
                     'b': [float('nan'), 2.7, float('nan')],
                     'E': [71400.0, 26300.0, float('nan')],
                     'k': [float('nan'), float('nan'), 1000.0],
                     'coeftype': ['Arrhenius', 'modifiedArrhenius', 'Constant'],
                     'vprime': np.array([[ 1.,  0.,  0.],
                                      [ 0.,  1.,  0.],
                                      [ 0.,  0.,  1.],
                                      [ 0.,  1.,  1.],
                                      [ 0.,  0.,  0.],
                                      [ 1.,  0.,  0.]]),
                     'v2prime': np.array([[ 0.,  1.,  1.],
                                          [ 1.,  0.,  0.],
                                          [ 1.,  1.,  0.],
                                          [ 0.,  0.,  0.],
                                          [ 0.,  0.,  1.],
                                          [ 0.,  0.,  0.]])}
    actual_dict = ck.get_reactions("test_xmls/rxns.xml")
    assert np.array_equal(actual_dict['species'], expected_dict['species'])
    for i in range(len(expected_dict['A'])):
        assert actual_dict['A'][i] == expected_dict['A'][i] or np.isnan(actual_dict['A'][i])
        assert actual_dict['b'][i] == expected_dict['b'][i] or np.isnan(actual_dict['b'][i])
        assert actual_dict['E'][i] == expected_dict['E'][i] or np.isnan(actual_dict['E'][i])
        assert actual_dict['k'][i] == expected_dict['k'][i] or np.isnan(actual_dict['k'][i])
    assert np.array_equal(actual_dict['coeftype'], expected_dict['coeftype'])
    assert np.array_equal(actual_dict['vprime'], expected_dict['vprime'])
    assert np.array_equal(actual_dict['v2prime'], expected_dict['v2prime'])


def test_xml_file_not_found():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/the_ghost_of_files.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_empty_xml_file():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_empty_file.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_missing_arrhenius_parameters():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_constant_parameters():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_constant_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_modified_arrhenius_parameters():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_modified_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactants():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_reactants.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactions():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_reactions.xml")
    except ValueError as err:
        assert(type(err)==ValueError)


def test_missing_species():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_missing_species.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_unexpected_reactant():
    # Test for an empty xml file
    try:
        ck.get_reactions("test_xmls/rxns_test_unexpected_reactant.xml")
    except ValueError as err:
        assert(type(err)==ValueError)


test_working_xml()
test_xml_file_not_found()
test_empty_xml_file()
test_missing_arrhenius_parameters()
test_missing_constant_parameters()
test_missing_modified_arrhenius_parameters()
test_missing_reactants()
test_missing_reactions()
test_missing_species()
test_unexpected_reactant()
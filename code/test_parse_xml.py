#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16

@author: ryanjanssen
"""
import numpy as np
import parse_xml as pa

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
                     'v2prime': np.array([[ 0.,  1.,  1.],
                                          [ 1.,  0.,  0.],
                                          [ 1.,  1.,  0.],
                                          [ 0.,  0.,  0.],
                                          [ 0.,  0.,  1.],
                                          [ 0.,  0.,  0.]])}
    actual_dict = pa.get_reactions("test_xmls/rxns.xml")
    assert np.array_equal(actual_dict['species'], expected_dict['species'])
    for i in range(len(expected_dict['As'])):
        assert actual_dict['As'][i] == expected_dict['As'][i] or np.isnan(actual_dict['As'][i])
        assert actual_dict['bs'][i] == expected_dict['bs'][i] or np.isnan(actual_dict['bs'][i])
        assert actual_dict['Es'][i] == expected_dict['Es'][i] or np.isnan(actual_dict['Es'][i])
        assert actual_dict['ks'][i] == expected_dict['ks'][i] or np.isnan(actual_dict['ks'][i])
    assert np.array_equal(actual_dict['rxn_types'], expected_dict['rxn_types'])
    assert np.array_equal(actual_dict['vprime'], expected_dict['vprime'])
    assert np.array_equal(actual_dict['v2prime'], expected_dict['v2prime'])


def test_xml_file_not_found():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/the_ghost_of_files.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_empty_xml_file():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_empty_file.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_missing_arrhenius_parameters():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_constant_parameters():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_constant_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_modified_arrhenius_parameters():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_modified_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactants():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_reactants.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactions():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_reactions.xml")
    except ValueError as err:
        assert(type(err)==ValueError)


def test_missing_species():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_missing_species.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_unexpected_reactant():
    # Test for an empty xml file
    try:
        pa.get_reactions("test_xmls/rxns_test_unexpected_reactant.xml")
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
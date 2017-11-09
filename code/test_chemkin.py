#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Oct 16 17:12:32 2017
    
    @author: paulblankley
    """
import numpy as np
from chemkin import ReactionSet 

# LINE 249, 377
def test_reaction_rates():
    x = np.array([[1.],[2.],[1.]])
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    assert(np.array_equal(rrr.progress_rates(x,10),[40.0,10.0]))
    assert(np.array_equal(rrr.reaction_rates(x,10)[0],[-60.0,-70.0,70.0]))


def test_reaction_coef():
    rrr = ReactionSet('test_xmls/reaction_coef_1.xml')
    assert(rrr.reaction_coefs(900)[0][0]==0.00044989777442266471)
    assert(rrr.reaction_coefs(900)[1][0]==1.5783556022951033)


def test_set_params():
    rrr = ReactionSet('test_xmls/reaction_coef_1.xml')
    rrr.reaction_coefs(900)
    rrr.set_params(1,k=10,coeftype='Constant')
    assert(rrr.reaction_coefs(900)[1][0]==10.0)

def test_init_value_error(): # Hits test in get_reaction
    try:
        rrr = ReactionSet('test_xmls/reaction_init_value_1.xml')
    except ValueError as err:
        assert(type(err) == ValueError)


def test_init_A_error():
    try:
        rrr = ReactionSet('test_xmls/reaction_init_value_2.xml')
    except ValueError as err:
        assert(type(err) == ValueError)


def test_coef_type_error():
    try:
        rrr = ReactionSet('test_xmls/reaction_init_type_1.xml')
    except ValueError as err:
        assert(type(err) == ValueError)


def test_T_val_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    T = -1
    try:
        rrr.reactions[0].reaction_coef(T)
    except ValueError as err:
        assert(type(err) == ValueError)


def test_T_type_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    T = 'fsag'
    try:
        rrr.reactions[0].reaction_coef(T)
    except TypeError as err:
        assert(type(err) == TypeError)
        

def test_progress_rate_x_shape_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].progress_rate(np.array([[1],[2],[3],[4]]),1)
    except ValueError as err:
        assert (type(err) == ValueError)



def test_progress_rate_T_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].progress_rate(np.array([[1],[2],[3]]),-144)
    except ValueError as err:
        assert (type(err) == ValueError)


def test_progress_rate_T_error_2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].progress_rate(np.array([[1],[2],[3]]), 'f')
    except TypeError as err:
        assert (type(err) == TypeError)

def test_progress_rate_T_error_3():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].progress_rate(np.array([[1],[2],[3]]), [1,2,3])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_reaction_rate_x_shape_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].reaction_rate(np.array([[1],[2],[3],[4]]),1)
    except ValueError as err:
        assert (type(err) == ValueError)


def test_reaction_rate_T_error():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].reaction_rate(np.array([[1],[2],[3]]),-144)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_reaction_rate_T_error_2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.reactions[0].reaction_rate(np.array([[1],[2],[3]]), 'f')
    except ValueError as err:
        assert (type(err) == ValueError)


def test_arrhenius_k_overflow():
    rrr = ReactionSet('test_xmls/reaction_arr_over_1.xml')
    try:
        rrr.reactions[0]._arrhenius(100)
    except OverflowError as err:
        assert (type(err) == OverflowError)

test_arrhenius_k_overflow()

def test_mod_arrhenius_k_overflow():
    rrr = ReactionSet('test_xmls/reaction_arr_over_2.xml')
    try:
        rrr.reactions[0]._mod_arrhenius(100)
    except OverflowError as err:
        assert (type(err) == OverflowError)


def test_set_param_error_A_type():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, A = 'f')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_A_type2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, A = [1,2])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_b_type():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, b = [1,2])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_b_type2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(1, b = 'f')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_E_type():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, E = [1,2,3])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_E_type2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(1, E = 'sefg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_R_type():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, R = [1,2,33])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_R_type2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(1, R = 'setttg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_k_type():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(0, k = [-1,2,33])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_k_type2():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(1, k = 'seyretttg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_coeftype():
    rrr = ReactionSet('test_xmls/reaction_rate_1.xml')
    try:
        rrr.set_params(1, coeftype = 'seyretttg')
    except ValueError as err:
        assert (type(err) == ValueError)

# Parser section of testing 
## UPDATE FOR NEW PARSER
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
    actual_dict = ReactionSet("test_xmls/rxns.xml").get_params()
    assert np.array_equal(actual_dict['species'], expected_dict['species'])
    for i in range(len(expected_dict['A'])):
        assert actual_dict['A'][i] == expected_dict['A'][i] or actual_dict['A'][i] == 0
        assert actual_dict['b'][i] == expected_dict['b'][i] or actual_dict['b'][i] == 0
        assert actual_dict['E'][i] == expected_dict['E'][i] or actual_dict['E'][i] == 0
        assert actual_dict['k'][i] == expected_dict['k'][i] or actual_dict['k'][i] == 0
    assert np.array_equal(actual_dict['coeftype'], expected_dict['coeftype'])
    assert np.array_equal(actual_dict['vprime'], expected_dict['vprime'])
    assert np.array_equal(actual_dict['v2prime'], expected_dict['v2prime'])


def test_xml_file_not_found():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/the_ghost_of_files.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_empty_xml_file():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_empty_file.xml")
    except FileNotFoundError as err:
        assert(type(err)==FileNotFoundError)


def test_missing_arrhenius_parameters():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_constant_parameters():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_constant_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_modified_arrhenius_parameters():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_modified_arrhenius_parameters.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactants():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_reactants.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_missing_reactions():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_reactions.xml")
    except ValueError as err:
        assert(type(err)==ValueError)


def test_missing_species():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_missing_species.xml")
    except AttributeError as err:
        assert(type(err)==AttributeError)


def test_unexpected_reactant():
    # Test for an empty xml file
    try:
        ReactionSet("test_xmls/rxns_test_unexpected_reactant.xml")
    except ValueError as err:
        assert(type(err)==ValueError)


# This part of tests check the functionality of reaction_dict['reversible']
def test_reversible_missing_tag():
    # Test for missing reversible tag
    try:
        ReactionSet("test_xmls/rxns_test_reversible_missing_tag.xml")
    except ValueError as err:
        assert(type(err) == ValueError)

def test_type_missing_tag():
    # Test for missing type tag
    try:
        ReactionSet("test_xmls/rxns_test_type_missing_tag.xml")
    except ValueError as err:
        assert(type(err) == ValueError)

def test_reversible_tag_error():
    # Test for invalid reversible tag attribute: i.e. not yes nor no
    try:
        ReactionSet("test_xmls/rxns_test_reversible_tag_error.xml")
    except ValueError as err:
        assert(type(err) == ValueError)

# UPDATE FOR NEW PARSER 
def test_reversible_input():
    # Test a standard output
    expected_dict = {'species': ['H', 'O', 'OH', 'H2', 'H2O', 'O2'],
                     'A': [35200000000.0, 0.0506, float('nan')],
                     'b': [float('nan'), 2.7, float('nan')],
                     'E': [71400.0, 26300.0, float('nan')],
                     'k': [float('nan'), float('nan'), 1000.0],
                     'coeftype': ['Arrhenius', 'modifiedArrhenius', 'Constant'],
                     'vprime': np.array([[1., 0., 0.],
                                         [0., 1., 0.],
                                         [0., 0., 1.],
                                         [0., 1., 1.],
                                         [0., 0., 0.],
                                         [1., 0., 0.]]),
                     'v2prime': np.array([[0., 1., 1.],
                                          [1., 0., 0.],
                                          [1., 1., 0.],
                                          [0., 0., 0.],
                                          [0., 0., 1.],
                                          [0., 0., 0.]]),
                     'reversible': [False, True, False]}
    actual_dict = ReactionSet("test_xmls/rxns_test_reversible_input.xml").get_params()
    assert np.array_equal(actual_dict['species'], expected_dict['species'])
    for i in range(len(expected_dict['A'])):
        assert actual_dict['A'][i] == expected_dict['A'][i] or actual_dict['A'][i] == 0
        assert actual_dict['b'][i] == expected_dict['b'][i] or actual_dict['b'][i] == 0
        assert actual_dict['E'][i] == expected_dict['E'][i] or actual_dict['E'][i] == 0
        assert actual_dict['k'][i] == expected_dict['k'][i] or actual_dict['k'][i] == 0
    assert np.array_equal(actual_dict['coeftype'], expected_dict['coeftype'])
    assert np.array_equal(actual_dict['vprime'], expected_dict['vprime'])
    assert np.array_equal(actual_dict['v2prime'], expected_dict['v2prime'])
    assert actual_dict['reversible'] == expected_dict['reversible']
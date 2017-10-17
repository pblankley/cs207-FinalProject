#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Mon Oct 16 17:12:32 2017
    
    @author: paulblankley
    """
import numpy as np
from chemkin import Reaction

def test_reaction_rates():
    vp = np.array([[1.,2.],[2.,0.],[0.,2.]])
    vpp = np.array([[0.,0.],[0.,1.],[2.,1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('nan'),float('nan')], \
        'b': [float('nan'),float('nan')], 'E': [float('nan'),float('nan')], \
            'k': [10,10], 'coeftype': ['Constant','Constant']}
    x = np.array([[1.],[2.],[1.]])
    rrr = Reaction(pdict)
    assert(rrr.progress_rate(x,10)==[40.0,10.0])
    assert(rrr.reaction_rate(x,10)==[-60.0,-70.0,70.0])

def test_reaction_coef():
    vp = np.array([[1.,2.],[2.,0.],[0.,2.]])
    vpp = np.array([[0.,0.],[0.,1.],[2.,1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045,.00045], \
        'b': [1.2,1.2], 'E': [1.7,1.7], \
            'k': [float('nan'),float('nan')], 'coeftype': ['Arrhenius','modifiedArrhenius']}
    rrr = Reaction(pdict)
    assert(rrr.reaction_coef(900)==[0.00044989777442266471,1.5783556022951033])

def test_set_params():
    vp = np.array([[1.,2.],[2.,0.],[0.,2.]])
        vpp = np.array([[0.,0.],[0.,1.],[2.,1.]])
            pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045,.00045], \
                'b': [1.2,1.2], 'E': [1.7,1.7], \
                'k': [float('nan'),float('nan')], 'coeftype': ['Arrhenius','modifiedArrhenius']}
                    rrr = Reaction(pdict)
                        rrr.reaction_coef(900)
                            rrr.set_params(1,k=10,coeftype='Constant')
                                assert(rrr.reaction_coef(900)==[0.00044989777442266471, 10])

# New Test Suite
def test_init_shape():
    vp = np.array([[1,2],[2,0]])
    vpp = np.array([1,2])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    try:
        rrr = Reaction(pdict)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_init_value_error():
    vp = np.array([[1,2],[2,0]])
    vpp = np.array([[1,2],[2,1]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': ['f', .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    try:
        rrr = Reaction(pdict)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_init_type_error():
    vp = np.array([[1,2],[2,0]])
    vpp = np.array([[1,2],[2,1]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.00045, .00045], \
        'b': [[1,2], 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    try:
        rrr = Reaction(pdict)
    except TypeError as err:
        assert(type(err) == TypeError)

def test_init_A_error():
    vp = np.array([[1,2],[2,0]])
    vpp = np.array([[1,2],[2,1]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [-2, .00045], \
        'b': [1, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    try:
        rrr = Reaction(pdict)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_coef_type_error():
    vp = np.array([[1,2],[2,0]])
    vpp = np.array([[1,2],[2,1]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [555, .00045], \
        'b': [1, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Invalid', 'modifiedArrhenius']}
    try:
        rrr = Reaction(pdict)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_T_val_error():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    T = -1
    try:
        rrr.reaction_coef(T)
    except ValueError as err:
        assert(type(err) == ValueError)

def test_T_type_error():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    T = 'fsag'
    try:
        rrr.reaction_coef(T)
    except TypeError as err:
        assert(type(err) == TypeError)
'''
    def test_progress_rate_x_shape_error():
    # Test for line 173 in chemkin.py
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
    'b': [1.2, 1.2], 'E': [1.7, 1.7], \
    'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
    rrr.progress_rate(np.array([[1],[2],[3],[4]]),1)
    except ValueError as err:
    assert (type(err) == ValueError)
    '''

def test_progress_rate_T_error():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.progress_rate(np.array([[1],[2],[3]]),-144)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_progress_rate_T_error_2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.progress_rate(np.array([[1],[2],[3]]), 'f')
    except TypeError as err:
        assert (type(err) == TypeError)

def test_progress_rate_T_error_3():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.progress_rate(np.array([[1],[2],[3]]), [1,2,3])
    except TypeError as err:
        assert (type(err) == TypeError)
'''
    def test_reaction_rate_x_shape_error():
    # Test for line 214 in chemkin.py
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
    'b': [1.2, 1.2], 'E': [1.7, 1.7], \
    'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
    rrr.reaction_rate(np.array([[1],[2],[3],[4]]),1)
    except ValueError as err:
    assert (type(err) == ValueError)
    '''

def test_reaction_rate_T_error():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.reaction_rate(np.array([[1],[2],[3]]),-144)
    except ValueError as err:
        assert (type(err) == ValueError)

def test_reaction_rate_T_error_2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [.00045, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('nan'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.reaction_rate(np.array([[1],[2],[3]]), 'f')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_arrhenius_k_overflow():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr._arrhenius(0,100)
    except OverflowError as err:
        assert (type(err) == OverflowError)

def test_mod_arrhenius_k_overflow():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr._mod_arrhenius(0,100)
    except OverflowError as err:
        assert (type(err) == OverflowError)

def test_set_param_error_A_type():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, A = 'f')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_A_type2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, A = [1,2])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_b_type():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, b = [1,2])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_b_type2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.5, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(1, b = 'f')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_E_type():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, E = [1,2,3])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_E_type2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.5, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(1, E = 'sefg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_R_type():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, R = [1,2,33])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_R_type2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.5, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(1, R = 'setttg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_k_type():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [float('inf'), .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(0, k = [-1,2,33])
    except TypeError as err:
        assert (type(err) == TypeError)

def test_set_param_error_k_type2():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.5, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(1, k = 'seyretttg')
    except ValueError as err:
        assert (type(err) == ValueError)

def test_set_param_error_coeftype():
    vp = np.array([[1., 2.], [2., 0.], [0., 2.]])
    vpp = np.array([[0., 0.], [0., 1.], [2., 1.]])
    pdict = {'vprime': vp, 'v2prime': vpp, 'A': [0.5, .00045], \
        'b': [1.2, 1.2], 'E': [1.7, 1.7], \
            'k': [float('inf'), float('nan')], 'coeftype': ['Arrhenius', 'modifiedArrhenius']}
    rrr = Reaction(pdict)
    try:
        rrr.set_params(1, coeftype = 'seyretttg')
    except ValueError as err:
        assert (type(err) == ValueError)

test_reaction_rates()
test_reaction_coef()
test_set_params()

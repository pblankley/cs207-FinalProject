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
     
test_reaction_rates()
test_reaction_coef()
test_set_params()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 10:36:18 2017

@author: paulblankley
"""
import reaction_coeffs as rc


# Testing suite for reaction coeffs

def test_arrhenius_num():
    # Test arrhenius
    rr1 = rc.ReactionRates(9,1.5,1500)
    assert(rr1.arrhenius()==8.998917553672602)
    rr2 = rc.ReactionRates(.03,10.2,1200)
    assert(rr2.arrhenius()==0.0299693445162384)
    
    # Test modified arrhenius
    rr3 = rc.ReactionRates(9,1.2,1.5,1500)
    assert(rr3.mod_arrhenius()==58277.3484653231062111)
    rr4 = rc.ReactionRates(.03,.01,10.2,1200)
    assert(rr4.mod_arrhenius()==0.03217133305160313)

def test_arrhenius_over_under():
    # Test for overflows
    rr1 = rc.ReactionRates(2.0,1.2,float('-inf'),1500)
    try:
        rr1.arrhenius()
    except OverflowError as err:   
        assert(type(err)==OverflowError)
        
    try:
        rr1.mod_arrhenius()
    except OverflowError as err:   
        assert(type(err)==OverflowError)
    
    # Test for underflows
    rr2 = rc.ReactionRates(2.0,3.4,float('inf'),1200)
    try:
        rr2.arrhenius()
    except FloatingPointError as err:   
        assert(type(err)==FloatingPointError)
    
    try:
        rr2.mod_arrhenius()
    except FloatingPointError as err:   
        assert(type(err)==FloatingPointError)

def test_set_params():
    # Test parameters actually set by method
    rr1 = rc.ReactionRates(9,1.2,1.5,1500)
    rr1.set_params(A=10,b=2,E=3,T=1000,R=9)
    assert(rr1.A==10)
    assert(rr1.b==2)
    assert(rr1.E==3)
    assert(rr1.T==1000)
    assert(rr1.R==9)
    
    # Test error catching when setting parameters
    try:
        rr1.set_params(A='3j')
    except ValueError as err:
        assert(type(err)==ValueError)
    try:
        rr1.set_params(A=[3,5])
    except TypeError as err:
        assert(type(err)==TypeError)

def test_class_init():
    # Test for inputs too short or too long
    try:
        rr1 = rc.ReactionRates(1.2,3.2,3.4,2.1,4)
    except ValueError as err:
        assert(type(err)==ValueError)
    try:
        rr1 = rc.ReactionRates(1.2,3.2)
    except ValueError as err:
        assert(type(err)==ValueError)
        
    # Test for strictly positive A and T
    try:
        rr1 = rc.ReactionRates(-1.2,3.2,3.4,2.1)
    except ValueError as err:
        assert(type(err)==ValueError)
    try:
        rr1 = rc.ReactionRates(1.2,3.2,-4)
    except ValueError as err:
        assert(type(err)==ValueError)
    
    # Test for not float inputs in init
    try:
        rr1 = rc.ReactionRates('3j',2,1)
    except ValueError as err:
        assert(type(err)==ValueError)
    try:
        rr1 = rc.ReactionRates(5,[3,5],8)
    except TypeError as err:
        assert(type(err)==TypeError)
        
        
test_arrhenius_over_under()
test_arrhenius_num()
test_set_params()
test_class_init()


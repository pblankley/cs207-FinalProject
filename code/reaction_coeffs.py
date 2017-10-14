#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 10:07:00 2017

@author: paulblankley
"""

import numpy as np

class ReactionRates:
    """ 
    This class takes in and parses the arguments A, b, E, T in that order.  
    It has methods for the modified and the standard Arrhenius rates.  If you 
    want to change the value of the R constsant you can change it by using the
    'set_params' function.
    
    --------
    Call 'arrhenius' with no arguments for the standard arrhenius rate 
    Call 'mod_arrhenius' with no arguments for the modified arrhenius rate.
    
    --------
    Raises: __init__ can raise ValueError if you do not put in the correct number 
        of arguments, and TypeError if you input a type that cannot be converted 
        to a float.
        
    ========
    
    Examples:
        
    >>> rr=ReactionRates(.00045,1.2,1.7,900)
    >>> rr.mod_arrhenius()
    1.5783556022951033
    
    >>> rr=ReactionRates(.00045,1.2,1.7,900)
    >>> rr.arrhenius()
    0.00044989777442266471
    
    """
    def __init__(self,*args):
        self.R = 8.314
        self.b = None
        
        if len(args)!=4 and len(args)!=3:
            raise ValueError('You must only give 3 or 4 parameters in the list. \
                             You gave {0} parameters. Hint: no lists'.format(len(args)))
            
        if len(args)==3:
            try:
                self.A = float(args[0])
                self.E = float(args[1])
                self.T = float(args[2])
            except (TypeError,ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('You must input a numeric, real number data type for all parameters.')
                raise TypeError('You must input a real number. Hint: you may have put in a list.')
                
        elif len(args)==4:
            try:
                self.A = float(args[0])
                self.b = float(args[1])
                self.E = float(args[2])
                self.T = float(args[3])
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('You must input a numeric, real number data type for all parameters.')
                raise TypeError('You must input a real number. Hint: you may have put in a list.')
        
        if self.A <= 0:
            raise ValueError('Your A value should be strictly positive. It was {0}.'.format(self.A))
            
        if self.T < 0:
            raise ValueError('Your T value should be positive. It was {0}.'.format(self.T))
            
    def set_params(self,A=None,b=None,E=None,T=None,R=None):
        """ This function takes inputs of the parameters you want to set for 
        reaction coefficient calculation 
        -------
        Args: A,b,E,T,R; all floats and optional arguments
        -------
        Returns: None
        -------
        Raises: ValueError when any input given a value other than None cannot 
            be cast to a float
        """
        if type(A) != type(None):
            try:
                self.A = float(A)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for A was not a numeric, real number.')
                raise TypeError('You must input a real number for A. Hint: you may have put in a list.')
        
                
        if type(b) != type(None):
            try:
                self.b = float(b)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for b was not a numeric, real number.')
                raise TypeError('You must input a real number for b. Hint: you may have put in a list.')
        
        if type(E) != type(None):
            try:
                self.E = float(E)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for E was not a numeric, real number.')
                raise TypeError('You must input a real number for E. Hint: you may have put in a list.')
        
        if type(T) != type(None):
            try:
                self.T = float(T)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for T was not a numeric, real number.')
                raise TypeError('You must input a real number for T. Hint: you may have put in a list.')
                
        if type(R) != type(None):
            try:
                self.R = float(R)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for R was not a numeric, real number.')
                raise TypeError('You must input a real number for R. Hint: you may have put in a list.')

    def arrhenius(self):
        """ This function takes in the parameters A, b, E, and T (kelvin temperature)
        from the class attributes, and it will return a value, k, that is the 
        Arrhenius reaction rate coefficient.
        ---------
        Args: None, (gets args from class)
        ---------
        Returns: The float k where k is the reaction rate coefficient.
        ---------
        Raises: OverflowError after constant evaluation
                FloatingPointError after constant evaluation for underflow
        """
        k = self.A*np.exp(-self.E/(self.R*self.T))
        if k == float('inf'):
            raise OverflowError('overflow error in evalutation of constant')
        if k <= np.finfo(float).eps:
            raise FloatingPointError('underflow error in evalutation of constant')
        return k

    def mod_arrhenius(self):
        """ This function takes in the parameters A, b, E, and T (kelvin temperature)
        from the class attributes, and it will return a value, k, that is the 
        modified Arrhenius reaction rate coefficient.
        ---------
        Args: None, (gets args from class)
        ---------
        Returns: The float k where k is the reaction rate coefficient.
        ---------
        Raises: OverflowError after constant evaluation
                FloatingPointError after constant evaluation for underflow
                ValueError if you call this method and do not specify a "b" value
        """
        if self.b is None:
            raise ValueError('You need to specify a "b" variable if you want modified arrhenius')
        k = self.A*(self.T**self.b)*np.exp(-self.E/(self.R*self.T))
        if k == float('inf'):
            raise OverflowError('overflow error in evalutation of constant')
        if k <= np.finfo(float).eps:
            raise FloatingPointError('underflow error in evalutation of constant')
        return k

if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=True)
    
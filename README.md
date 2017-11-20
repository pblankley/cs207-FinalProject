[![Build Status](https://travis-ci.org/cs207-g1/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/cs207-g1/cs207-FinalProject)

[![Coverage Status](https://coveralls.io/repos/github/cs207-g1/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/cs207-g1/cs207-FinalProject?branch=master)

# Chemical Kinetics Library
> Editors: Paul Blankley, Ryan Janssen, Boyuan Sun

> Date started: Oct 13, 2017

> Course: CS 207. System Development for Computational Science

> Organization: Harvard SEAS CS.207 Group 1

> Target User: Users who want to utilize the reation rate coefficients for various purposes


## I. Introduction
### 1.1 Preliminaries
Chemical reactions take place everywhere at any time. Computing the reaction rates of a particular reaction is the first and fundatmental step towards understanding the mechanics of the reaction. Various types of chemical reactions and reaction rates coefficients will be addressed in our library. The *purpose* of this chemical kinetics library is to calculate the reaction rates for species in by accepting users' input sets of chemical reactions in xml with corresponding coefficients. The library will calculate the progress rates, reaction rate coefficients including constant reaction rate coefficients, Arrhenius reaction rate coefficients, and modified Arrhenius reaction rate coefficients, and finally the reaction rates for each specie that the users have specified. Users will then choose how to use the rates given by the library afterwards.
### 1.2 Key Terminology
#### 1.2.1 Elementary reactions
[Elementary reactions](https://en.wikipedia.org/wiki/Elementary_reaction), as indicated by the name, are the most fundamental chemical reactions in chemical kinetics. In short, if there is no intermediates found during the span of a chemical reaction, we define the reation to be elementary.

#### 1.2.2 Irreversible reactions vs. reversible reactions
[Irreversible reactions and reversible reactions](https://chem.libretexts.org/Core/Physical_and_Theoretical_Chemistry/Equilibria/Reversibility_and_Equilibria/Reversible_vs._Irreversible_Reactions) are the reactions our library focus on. Both reactions are commonly found in nature. In short, irreverisble reactions occur when the products of the reactions cannot not be converted to the previous reactants. Reversible reactions are the opposite.

#### 1.2.3 Reaction rate coefficients
Chemical reaction rates are discussed [here](https://en.wikipedia.org/wiki/Reaction_rate_constant). In our chemical kinetics library we support three types of reaction rate coefficients: 
- Constant reaction rate coefficients
  * Defined by the constant reaction rate coefficient k. No additional calculation is needed.
- Arrhenius reaction rate coefficients
  * Detailed description can be found and formula can be found [here](https://en.wikipedia.org/wiki/Arrhenius_equation).
- Modified Arrhenius (a.k.a Kooij) reaction rate coefficients
  * Detailed description can be found and formula can be found [here](https://en.wikipedia.org/wiki/Arrhenius_equation).
  
#### 1.2.4 Progress rate and Reaction rate
[Reaction rate](https://www.britannica.com/science/reaction-rate) in general defines the speed of a chemical reaction. Reaction rates are computed by the users' defined sets of inputs for each specie given its corresponding concentration and reaction rates. The definition of progress rate and reaction rate and formulas for computation can be found [here](https://github.com/IACS-CS-207/cs207-F17/blob/master/lectures/L8/L8.ipynb).

## II. Installation

Run the following command in Terminal on a Mac or in cmd.exe on a Windows machine.

$ pip install chemkin207

After pip finishes installing the package you can run the tests by running the following commands from the command line.

$ python
$ >>> import chemkin207
$ >>> chemkin207.test()

This sequence of commands will run the tests for the module and display the output.

## III. Basic Usage and Examples

### 3.1 General Usage
The ultimate output of the Chemical Kinetics library is to return a set of reaction rates *f* for a given set of reactions, which is calculated by calling the *reaction_rate* method.  Intermediate outputs can be called using the *reaction_coef* method (returning the 'k' reaction coefficients for the system), or the *progress_rate* method (returning the progress rate *omega*).

Data can be input in one of two ways: 
1. From an .xml file via the built-in *get_reactions* xml parser function, on class initiation.  XML must be in the format specified in the attached sample .xml.
2. By inputting parameters directly to the class via the *set_params* method.

All methods are implemented in the Reaction class, which will contain the necessary parameters to calculate outputs for a specified reaction temperature and species concentrations.

### 3.2 Method/Function details – ReactionSet class
Reaction set is intended to be the primary interface for the user.  Using the methods described below, the user can instantiate a set of reactions from an XML and calculate the reaction rates.


#### 3.2.1 ReactionSet(xml_doc) *(class initialization)*
This class represents the reaction tools for a set of elementary reactions.  The class takes in an xml specifying the reaction data on initialization, of form specified in the “xml template” section below.

__*Args*__: 
* param_dict; where param_dict is the output from the parser function.
    
__*Returns*__: 
* None, but instantiates self

__*Raises*__: 
* None
</blockquote>
<br>

#### 3.2.2 reaction_rates(self,x,T):
This function calculates the reaction rates of each reaction in the set of the following form:
                    V'11*A + V'21*B -> V''31*C
                    V'32*C -> V'12*A + V''22*B
It takes in the vectors v', v'' from the Reaction class and x in the order [[A],[B],[C]].
<blockquote>



__*Args*__: 
* x; vector, numpy array (or list) of length equal to the number of reactants in the system of equations.
* T; float, the strictly positive temperature 

__*Returns*__: 
* vector of floats; the reaction rate for each equation

__*Raises*__: 
* None (although reaction classes may raise exceptions - see 3.3 below)


Implementation Example:
```
    >>> rrr = ReactionSet('tests/test_xmls/reaction_rate_1.xml')
    >>> list(rrr.reaction_rates(np.array([[1.],[2.],[1.]]),10))
    [-60.0, -70.0, 70.0]
```
</blockquote>
<br>

        

#### 3.2.3 progress_rates(self, x, T):
This function calculates the progress rates *omega* of the reactions of the following form:

                    V'11*A + V'21*B -> V''31*C
                
                V'12*A + V'32*C -> V''22*B + V''32*C
                
It takes in the concentration vectors and temperature and, and reaction coefficients from its internal reaction database.
<blockquote>



__*Args*__: 
* x; vector of concentrations.  Numpy array (or list of lists) of length equal to the number of reactants in the system of equations. 
* T; temperature of the reaction

__*Returns*__: 
* rates; list of floats; the progress rate of the reaction for each equation

__*Raises*__: 
* None (although reaction classes may raise exceptions - see 3.3 below)


Implementation example:
```
    >>> rrr = ReactionSet('tests/test_xmls/reaction_rate_1.xml')
    >>> list(rrr.progress_rates(np.array([[1.],[2.],[1.]]),10))
    [40.0, 10.0]
```
</blockquote>
<br>
       
#### 3.2.4 reaction_coefs(self, T)
Sets reaction coefficients for each reaction (stored internally and also specified at initialization) for the given float temperature T.  <blockquote>



__*Args*__: 
* T; float; the temperature for all reactions

__*Returns*__: 
* coefs; np array of floats; array containing each reaction coefficient k

__*Raises*__: 
* None (although reaction classes may raise exceptions - see 3.3 below)

Implementation Example:
```
    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> rrr.reaction_coefs(900)[0][0]
    0.00044989777442266471

    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> rrr.reaction_coefs(900)[1][0]
    1.5783556022951033
```
</blockquote>
<br>

#### 3.2.5 get_params(self)
Returns parameter set for all reactions previously specified in the instance (either at init or later via set_params)<blockquote>


__*Args*__: 
* None

__*Returns*__: 
* param_dict; list of dictionaries for each reaction in the instance

__*Raises*__: 
* None

</blockquote>
<br>



#### 3.2.6 set_params(self,idx,A=None,b=None,E=None,R=None, k=None, coeftype=None):
This function takes inputs of the parameters you want to set for reaction coefficient calculations.
<blockquote>



__*Args*__: 
* idx; int; Index of the reaction for which you wish to set parameters
* A,b,E,T,R; all floats and optional arguments

__*Returns*__: 
* None (updates internal class parameters)

__*Raises*__: 
* ValueError ValueError when any input given a value other than None cannot be cast to a float

Implementation example:
```
    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> w = rrr.reaction_coefs(900)
    >>> ww = rrr.set_params(1,k=10, coeftype='Constant')
    >>> rrr.reaction_coefs(900)[1][0]
    10.0
```
</blockquote>
<br>

#### 3.2.8 get_reactions(name):
This function takes in the name of the input xml file, and returns a dictionary of relevant information for a set of chemical reactions.
<blockquote>



__*Args*__: 
* name; name of the input .xml file

__*Returns*__: 
* reaction_dict, dictionary of data for a reaction.  Contains the following keys:
    * reaction_dict['species']; list of strings, species of the reaction
    * reaction_dict['As']; list of floats, corresponding to reaction parameter A for each equation (= NaN for any equations that don't use A.
    * reaction_dict['bs']; list of floats, corresponding to reaction parameter b for each equation (= NaN for any equations that don't use b.
    * reaction_dict['Es']; list of floats, corresponding to reaction parameter E for each equation (= NaN for any equations that don't use E.
    * reaction_dict['ks']; list of floats, corresponding to reaction parameter k for each equation (= NaN for any equations that don't use k (ie, non-constant equations)).
    * reaction_dict['rxn_types']; List of strings. Elements Correspond to same reactions as reaction_parameters.  Each string is one of { 'Arrhenius', 'modifiedArrhenius', 'Constant' }
    * reaction_dict['vprime']; np array, full vprime matrix of all reactions in the xml file
    * reaction_dict['v2prime']; np array, full v2prime matrix of all reactions in the xml file
    
__*Raises*__: 
* FileNotFoundError if name is not a valid .xml path
* ValueError if xml is not in specified data format

Implementation example:
```
    >>> print(ck.get_reactions("demo_xmls/rxns.xml"))
    {'species': array(['H', 'O', 'OH', 'H2', 'H2O', 'O2'], dtype='<U3'), 
     'A': array([ 3.52000000e+10, 5.06000000e-02, nan]), 
     'b': array([ nan,  2.7, nan]), 
     'E': array([ 71400.,  26300., nan]), 
     'k': array([ nan, nan, 1000.]), 
     'coeftype': array(['Arrhenius', 'modifiedArrhenius', 'Constant'], dtype='<U17'), 
     'vprime': array([[ 1.,  0.,  0.],
                       [ 0.,  1.,  0.],
                       [ 0.,  0.,  1.],
                       [ 0.,  1.,  1.],
                       [ 0.,  0.,  0.],
                       [ 1.,  0.,  0.]]), 
       'v2prime': array([[ 0.,  1.,  1.],
                       [ 1.,  0.,  0.],
                       [ 1.,  1.,  0.],
                       [ 0.,  0.,  0.],
                       [ 0.,  0.,  1.],
                       [ 0.,  0.,  0.]])}
```

</blockquote>
<br>

### 3.3 Method/Function details – Reaction/ReversibleReaction/IrreversibleReaction class family

Reaction, ReversibleReaction, and IrreversibleReaction are a family of internal classes use to calculate reaction rates (via the Reaction class wrappers).  Reaction is the parent class of ReversibleReaction and Irreversible reaction, although generally ReversibleReaction and IrreversibleReaction will be instantiated.

#### 3.3.1 Reaction/ReversibleReaction/IrreversibleReaction(self, reactionDict, species) ReactionSet(xml_doc) *(class initialization)*:
Instantiates the respective reaction class.
<blockquote>


__*Args*__: 
* reactiondict; dict, A single entry that fully specifies the reaction.  Of the same form as a single entry used in ReactionSet.get_reactions() in 3.2.8.
* species; string, Name of species

__*Returns*__: 
* None (but updates internal parameters)

__*Raises*__: 
* ValueError if dictionary is not in standard format per 3.2.8
</blockquote>
<br>

    
#### 3.3.2 _arrhenius(self, T):
This internal function takes in the parameter T (kelvin temperature) from the class attributes, and it will return a value, k, that is the Arrhenius reaction rate coefficient.
<blockquote>


__*Args*__: 
* T, float; temperature, (gets args from class).

__*Returns*__: 
* The float k where k is the reaction rate coefficient.

__*Raises*__: 
* OverflowError after constant evaluation
* FloatingPointError after constant evaluation for underflow
</blockquote>
<br>

#### 3.3.3 _mod_arrhenius(self, T):
This internal function takes in the parameter T (kelvin temperature) from the class attributes, and it will return a value, k, that is the modified Arrhenius reaction rate coefficient.
<blockquote>


__*Args*__: 
* T, float; temperature (gets args from class).

__*Returns*__: 
* The float k where k is the reaction rate coefficient.

__*Raises*__: 
* OverflowError after constant evaluation
* FloatingPointError after constant evaluation for underflow
</blockquote>
<br>

#### 3.3.4 reaction_coef_forward(self, T):
Set reaction coefficients for the given float T.  Assigned reaction rate as Arrhennius, Modified Arrhennius, or Constant based on instance args.
<blockquote>


__*Args*__: 
* T, float; temperature (gets args from class).

__*Returns*__: 
* None

__*Raises*__: 
* ValueError when T cannot be cast to a float or T is negative
</blockquote>
<br>

#### 3.3.5 reaction_rate(self, x_in, T):
Set reaction coefficients for the given float T.  Assigned reaction rate as Arrhennius, Modified Arrhennius, or Constant based on instance args.
<blockquote>


__*Args*__: 
* x_in; vector, numpy array (or list) of length equal to the number of reactants in the system of equations.
* T; float, the strictly positive temperature in Kelvin

__*Returns*__: 
* f; vector of floats, the reaction rate for the equation

__*Raises*__: 
* ValueError ValueError when temp is less than 0 or x is not of shape (mx1)
</blockquote>
<br>

#### 3.3.6 progress_rate(self, x_in, T):
Function only available for the ReversibleReaction and IrreversibleReaction subclass.<br><br>
This function calculates the progress rates *omega* of the reactions of the following form:

                    V'11*A + V'21*B -> V''31*C
                
                V'12*A + V'32*C -> V''22*B + V''32*C
                
It takes in the concentration vectors and temperature and, and reaction coefficients from its internal reaction database.
<blockquote>


__*Args*__: 
* v',v''; matrices, numpy arrays of form mxn where m is the number of reactants and n is number of equations.
* x; vector, numpy array (or list of lists) of length equal to the number of reactants in the system of equations.
* k; float or list of length n (number of equations), the k constant in the reaction of elementary equations.
* T; float, the strictly positive temperature in Kelvin

__*Returns*__: 
* w; list of floats; the progress rate of the reversible or irreversible reaction for each equation

__*Raises*__: 
* ValueError ValueError if the shapes of the v matrices are not equal or if the x vector is not mx1 or if the value for T cannot be cast to a float.
* NotImplementedError if called by parent class Reaction()
</blockquote>
<br>


#### 3.3.7 get_nasa_coefs(self, T)
Function only available for the ReversibleReaction subclass.<br><br>
This function gets the NASA coefficients for a specific temperature from the internal SQL database COEF.sqlite.
<blockquote>


__*Args*__: 
* T; float, the strictly positive temperature in Kelvin

__*Returns*__: 
* out; numpy array mx7, where m is the number of species in the reaction system.

__*Raises*__: 
* ValueError ValueError if query returns nothing (may be due to improperly structured database COEF.sqlite.
* NotImplementedError if called by parent class Reaction() or IrreversibleReaction
</blockquote>
<br>


#### 3.3.8 get_query(self, cursor, T)
Function only available for the ReversibleReaction subclass.<br><br>
This function gets the proper query to use to query the NASA coefficient SQLite database. It also checks for invalid temoeratures in the given value.
<blockquote>


__*Args*__: 
* cursor; cursor for the database that holds the NASA coefficients
* T; float, the strictly positive temperature in Kelvin

__*Returns*__: 
* query; string, response to database query

__*Raises*__: 
* ValueError ValueError if the temperature is either above the allowable max value or below the min allowable value for the NASA coefficient database.
* NotImplementedError if called by parent class Reaction() or IrreversibleReaction
</blockquote>
<br>


#### 3.3.9 reaction_coef_backward(self, T)
Function only available for the ReversibleReaction subclass.<br><br>
This function gets the backward coefficients for a reversible reaction at the given temperature.
<blockquote>


__*Args*__: 
* T; float, the strictly positive temperature in Kelvin

__*Returns*__: 
* kb; float, the backwards reaction coefficient.

__*Raises*__: 
* NotImplementedError if called by parent class Reaction() or IrreversibleReaction
</blockquote>
<br>


## 4.0 Sample .xml format
All .xml reaction files should follow the sample format used below.  Source and Designer of this format is David Sondak, Harvard University CS207:

```
<?xml version="1.0"?>

<ctml>

    <phase>
        <speciesArray> H O OH H2 H2O O2 </speciesArray>
    </phase>

    <reactionData id="test_mechanism">

        <!-- reaction 01  -->
        <reaction reversible="no" type="Elementary" id="reaction01">
            <equation>H + O2 =] OH + O</equation>
            <rateCoeff>
                <Arrhenius>
                    <A>3.52e+10</A>
                    <E>7.14e+04</E>
                </Arrhenius>
            </rateCoeff>
            <reactants>H:1 O2:1</reactants>
            <products>OH:1 O:1</products>
        </reaction>

        <!-- reaction 02 -->
        <reaction reversible="no" type="Elementary" id="reaction02">
            <equation>H2 + O =] OH + H</equation>
            <rateCoeff>
                <modifiedArrhenius>
                    <A>5.06e-2</A>
                    <b>2.7</b>
                    <E>2.63e+04</E>
                </modifiedArrhenius>
            </rateCoeff>
            <reactants>H2:1 O:1</reactants>
            <products>OH:1 H:1</products>
        </reaction>

        <!-- reaction 03 -->
        <reaction reversible="no" type="Elementary" id="reaction03">
            <equation>H2 + OH =] H2O + H</equation>
            <rateCoeff>
                <Constant>
                    <k>1.0e+03</k>
                </Constant>
            </rateCoeff>
            <reactants>H2:1 OH:1</reactants>
            <products>H2O:1 H:1</products>
        </reaction>

    </reactionData>

</ctml>
```

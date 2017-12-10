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

Run the below command on the command line to install the package

$ pip install chemkin207

You can run the tests for the package by running the below commands on the command line.

$ python

$ >>> import chemkin207

$ >>> chemkin207.test()

You will see the output with the results of the tests.

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
* ValueError when any input given a value other than None cannot be cast to a float

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
Set reaction coefficients in the class for the given float T.  Assigned reaction rate as Arrhennius, Modified Arrhennius, or Constant based on instance args.
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
This function calculates the reaction rate of a reaction of the following form:

                V'11*A + V'21*B -> V''31*C

    It takes in the vectors v', v'' from the class and the x_in argument in the order [[A],[B],[C]].
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

It takes in the concentration vectors and temperature as arguments, and reaction coefficients from its internal reaction database.
<blockquote>


__*Args*__:
* x_in; vector, numpy array (or list of lists) of length equal to the number of reactants in the system of equations.
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
## 5. Additional Features
### 5.1 Motivation and Description
Currently the user can use chemkin to calculate reaction rates and produce final numerical output for a given temperature.  However, we expect that the user will often need to translate the reaction rates into a form that can be more easily distributed and dissimilated.  
For example, one of the common uses of this package will be to publish findings in journals.  For each iteration of the journal writing, the user will need to invest time in producing results, pasting them into the appropriate output, and visualizing them to a high quality standard.
We propose an additional chemkin feature that would automate these outputs.  Other anticipated “use cases” that we would prepare solution for include:
* The user may wish to export the results to more portable output format, such as a .csv, .txt, .tex or HDF5 (.hdf5).
* The user may be interested in tabulating their data in a repeatable format
* The user may need to visualize outputs at a range of temperatures rather than a single temperature, and repeatably across a number of reactions
* The user may be interested in finding local or global maxima/minima across the output temperature range

Our package would support three new output methodologies:
1. Automated graphing,
2. Multiple common output formats, and
3. Tabulation and “pretty print” presentation of numerical findings

### 5.2 ReactionSet class - Graphic and Tables
To support our users to visualize the output reaction rates and translate the reaction rates into a form that can be more easily distributed and dissimilated, we first add the following three functions to our ReactionSet class:

#### 5.2.1 plot_rates_against_temperature(self, query_species, concs, temps)
This method plots the reaction rates for the user-specified query specie(s), concentration, and temperature.
<blockquote>

__*Args*__:   
* query_species, str or list of species which are being queried (str)
* concs, np.array, concentration of ALL the species
* temps, list or np array - all temperatures that will be queried

__*Returns*__:
* plot of reaction rates against the temperature for each query specie

__*Raises*__:
* TypeError if query_species is not a list of strings
* ValueError if query_species contains an invalid specie
* TypeError if invalid value is found in temperature array
        """

</blockquote>
<br>

#### 5.2.2 to_table(self, query_species, concs, temps, out_file, out_type = 'csv', save_output = True)
This method outputs the reaction data to a table. The default output type of the function is csv and the user can specify the format of the output. Also the user can choose not to save the output file.
<blockquote>

__*Args*__:   
* query_species, list of species which are being queried (str)
* concs, np.array, concentration of ALL the species
* temps, list or np array - all temperatures that will be queried
* out_file, filename of table to output to
* out_type, one of ['csv', 'txt', 'latex', 'hdf5']
* save_output, boolean - if true, saves table, if false, simply returns output table

__*Returns*__:
* formatted output table

__*Raises*__:
* TypeError if query_species is not a list of strings
* ValueError if query_species contains an invalid specie
* TypeError if invalid value is found in temperature array

</blockquote>
<br>

#### 5.2.3 find_rates(self, query_species, concs, T_range, rtype)
This function finds the minimum or maximum reaction rate for the query specie in order passed in given the temperature range
<blockquote>

__*Args*__:
* query_species: str or list of str that wants to query
* concs: np.array, concentration of ALL the species
* tmin: float, query temperature minimum
* tmax: float, query temperature maximum
* precision: int, points that np.linspace will use; larger value means more precise plots

__*Return*__:
* tuple or list of tuples, minimum reaction rate for the query specie in the temperature range: tuple form: (min/max rate, temperature when the rate occurs)

__*Raises*__:
* TypeError if query_species is not a string of specie or a list of string of specie.
* TypeError if query_species contains invalid data type.
* ValueError if a specie in query_species is not in the input file
* TypeError if T_range is not a list or there is a invalid type in T_range

</blockquote>
<br>

### 5.3 MultiReactionOutput Class - Wrapper class for ReactionSet
This class is a wrapper class for parsing multiple reaction outputs at one time. Results are saved into the specified output directory, in two types of tables:
1. One cross-tabulated table that shows the reaction rates of each specie side-by-side, versus temperature. This table will be stored in the user-specified directory
2. One set of individual reaction tables that output each indvidual reaction versus temperature. This set of tables is stored in /support

#### 5.3.1 to_table_multi(self, query_species, concs, temps, output_dir, out_type = 'csv', include_supporting = True)
This method outputs all of the reactions in the MultiReactionOutput instantiation into a single table
<blockquote>

__*Args*__:
* query_species, list of species which are being queried (str)
* concs, list of np.arrays, one concentration array for each reaction
* temps, list or np array - all temperatures that will be queried
* output_dir, direct to output to - saves a file 'multireaction.*' in this directory
* out_type, one of ['csv', 'txt', 'latex', 'hdf5']
* include_supporting, boolean - if true, saves tables for each individual reaction in output_dir/supporting

__*Returns*__:
* None (but outputs table)

__*Raises*__:
* KeyError if queried species are not in ALL reactions
* TypeError if the list of concentrations does not match the number of reactions

</blockquote>
<br>

#### 5.3.2 _table_output(out_table, query_species, out_file, out_type = 'csv', multi_output = False)
This function outputs the table into one of four desired file formats.  Internal function.
<blockquote>

__*Args*__:
* out_table, the table to be output to file.  Must have column headers corresponding to each specie, and row 0 must contain temperature data.
* query_species, list of species which are being queried (str), in the same order as the table headers
* out_file, filename to output to
* out_type, one of ['csv', 'txt', 'latex', 'hdf5']
* multi_output, boolean which defines whether this is multi-reaction output or not

__*Returns*__:
* none, but saves table in out_file

__*Raises*__:
* TypeError if invalid output type is specified
* TypeError if non-str output filename is provided

</blockquote>
<br>

### 5.4 Anticipated Usage of New Feature
If users want to find the min/max reaction rates for certain specie(s), they would call ReactionSet.find_rates with corresponding inputs and the function would yield the min/max reaction rates for the species given the temperature range.

If users want to plot the progress of reaction rates for certain specie(s) in a temperature range, they would call ReactionSet.plot_rates_against_temperature with corresponding inputs and the function will plot the graph illustrating how the reaction rates with regard to the input temperature.

If users desired formatted outputs, they would declare an arbitrary number of reactions using the existing ReactionSet class. They would then instantiate a MultiReactionOutput class instance with the reaction module as an argument. At that point, the users would call all outputs directly from the MultiReactionOutput class by MultiReactionOutput.to_table_multi, which would write all the reaction rates into a single table with the desired output format.

### 5.5 External Dependencies
We will build the plotting functionality on top of MatplotLib.  The HDF5 outputs will use H5py.  The other important dependencies of this package are sqlite3 and NumPy. Each of these libraries is open source, well documented, and accepted as a de facto standard for Python.
The latex, txt, and CSV outputs will all use native functions from python 3.5.  

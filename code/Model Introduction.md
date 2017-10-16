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
Chemical reaction rates are dicussed [here](https://en.wikipedia.org/wiki/Reaction_rate_constant). In our chemical kinetics library we support three types of reaction rate coefficients: 
- Constant reaction rate coefficients

  * Defined by the constant reaction rate coefficient k. No additional calculation is needed.

- Arrhenius reaction rate coefficients

  * Detailed description can be found and formula can be found [here](https://en.wikipedia.org/wiki/Arrhenius_equation).
  
- Modified Arrhenius (a.k.a Kooij) reaction rate coefficients
  
  * Detailed description can be found and formula can be found [here](https://en.wikipedia.org/wiki/Arrhenius_equation).
  
#### 1.2.4 Progress rate and Reaction rate
[Reaction rate](https://www.britannica.com/science/reaction-rate) in general defines the speed of a chemical reaction. Reaction rates are computed by the users' defined sets of inputs for each specie given its corresponding concentration and reation rates. The definition of progress rate and reaction rate and formulas for computation can be found [here](https://github.com/IACS-CS-207/cs207-F17/blob/master/lectures/L8/L8.ipynb).

## II. Installation

We plan to migrate the project to the Anaconda cloud with PyPI for future easy install.  For a beta version of the software package, download the chemkin.py file and place the file in your working directory. You can also run the following command to clone the git repo and then move the chemkin module to your working directory.

$ git clone https://github.com/cs207-g1/cs207-FinalProject.git

Once you move chemkin.py to your working directory you can just run:

>>>import chemkin 

After that command you will have full access to the module.

## III. Basic Usage and Examples

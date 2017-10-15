# Chemical Kinetics Library
> Editors: Paul Blankley, Ryan Janssen, Boyuan Sun

> Course: CS 207. System Development for Computational Science

> Organization: Harvard SEAS CS.207 Group 1

> Target User: Users who want to utilize the reation rate coefficients for various purposes


## I. Introduction
### 1.1 Preliminaries
Chemical reactions take place everywhere at any time. Computing the reaction rates of a particular reaction is the first and fundatmental step towards understanding the mechanis of the reaction. Various types of chemical reactions and reaction rates coefficients will be addressed in our library. The *purpose* of this chemical kinetics library is to calculate the reaction rates for species in by accepting users' input sets of chemical reactions in xml with corresponding coefficients. The library will calculate the progress rates, reaction rate coefficients including constant reaction rate coefficients, Arrhenius reaction rate coefficients, and modified Arrhenius reaction rate coefficients, and finally the reaction rates for each specie that the users have specified. Users will then choose how to use the rates given by the library afterwards.
### 1.2 Key Terminology
#### 1.2.1 Elementary reactions
A detailed explanation of elementary reactions is provided [here](https://en.wikipedia.org/wiki/Elementary_reaction). In short, if there is no intermediates found during the span of a chemical reaction, we define the reation to be elementary.
#### 1.2.2 Elementary reactions


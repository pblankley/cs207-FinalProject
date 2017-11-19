
import numpy as np
from functools import reduce
import os
import xml.etree.ElementTree as ET
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ReactionSet:
    """
    This class represents the entire reaction for a set of elementary reactions.
    The class takes in a dictionary of parameters generated by the parser function.

    This dictionary contains a matrix vprime and a matrix v2prime corresponding to
    the usual v' and v'' matrices in systems of elementary reactions, v' being reactants
    and v'' being reactants.

    The dictionary also contains lists (length corresponding to the columns of v' and v'')
    with the values for A,b,E,k and coeftype for each elementary reaction in the system. NOTE: If one
    or more of these parameters is rendered useless or NA for a reaction it is given the
    value NaN. Coeftype is a list of strings containing the type of reaction.

    ----------
    Args: xml_doc; where xml_doc is the reaction definition xml.

    ----------
    Methods:
        reaction_rates(self,x,T): where x is the vector of concentrations of the system and
                            T is the temperature the system of reactions occurs at.
                            Gets reaction rates from reaction classes

        reaction_coef(Temperature); where Temperature is the specified temperature.
                            Returns the 'k' reaction coefficients for each reaction
                            in the system
                            (wrapper)

        progress_rates(x, T); where x is the vector of concentrations of the system and
                            T is the temperature the system of reactions occurs at. Gets
                            progress rates from reaction classes for each reaction in
                            the system
                            (wrapper)

        reaction_coefs(T); where T is the temperature the system of reactions occurs at.
                            Gets reaction coefficients from Reactions class
                            (wrapper)

        get_params(); Returns the current parameters of the reaction (in dict)

        set_params(idx, **kwargs); where you specify idx to be the index of the reaction
                            you want to change the parameters for and the keyword
                            indicates the parameter you want to change.
                            Options to change are: {A,b,E,R,k,coeftype}

        get_reactions(idx, name); where name is the name of the input xml.
                            Parses the input xml and returns the reaction data in the
                            form of a dictionary.
    =========
    Examples:
    # Example with the reaction rate

    >>> rrr = ReactionSet('tests/test_xmls/reaction_rate_1.xml')
    >>> list(rrr.reaction_rates(np.array([[1.],[2.],[1.]]),10))
    [-60.0, -70.0, 70.0]

    # Example with the progress rate

    >>> rrr = ReactionSet('tests/test_xmls/reaction_rate_1.xml')
    >>> list(rrr.progress_rates(np.array([[1.],[2.],[1.]]),10))
    [40.0, 10.0]

    # Example with reaction coef

    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> rrr.reaction_coefs(900)[0][0]
    0.00044989777442266471

    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> rrr.reaction_coefs(900)[1][0]
    1.5783556022951033


    # Example with set params

    >>> rrr = ReactionSet('tests/test_xmls/reaction_coef_1.xml')
    >>> w = rrr.reaction_coefs(900)
    >>> ww = rrr.set_params(1,k=10, coeftype='Constant')
    >>> rrr.reaction_coefs(900)[1][0]
    10.0

    """

    def __init__(self, xml_doc):
        self.param_dict = self.get_reactions(xml_doc)
        self.species = self.param_dict['species']
        self.reactions = []
        self.number_reverse = 0
        for r in self.param_dict['reactions']:
            if r['reversible']:
                self.number_reverse+=1
                self.reactions.append(ReversibleReaction(r,self.species))
            else:
                self.reactions.append(IrreversibleReaction(r,self.species))

    def reaction_rates(self,x,T):
        # gets reaction rates from reaction classes
        rates = np.zeros((1,len(self.species)))
        for react in self.reactions:
            rates += react.reaction_rate(x,T)
        return rates[0]

    def progress_rates(self,x,T):
        # gets progress rates from reaction classes
        rates = []
        for react in self.reactions:
            rates.append(react.progress_rate(x,T))
        return np.array(rates)

    def reaction_coefs(self,T):
        # naive implementations for irreversible
        coefs = []
        for react in self.reactions:
            coefs.append(react.reaction_coef(T))
        return coefs

    def __str__(self):
        return "species: {0}, with {1} Reversible reaction(s) and {2} Irreversible reaction(s)".format( \
                         self.species, self.number_reverse, len(self.reactions)-self.number_reverse)

    def get_params(self):
        return self.param_dict

    def set_params(self,react_idx,A=None,b=None,E=None,R=None, k=None, coeftype=None):
        """ This function takes inputs of the parameters you want to set for
        reaction coefficient calculation and the location in the reaction array
        (stored in order of input) that you want to modify.
        -------
        Args: react_idx int, (location of reaction to modify), and A,b,E,T,R; all
                                                        floats and optional arguments
        -------
        Returns: None
        -------
        Raises: ValueError when any input given a value other than None cannot
            be cast to a float
        """
        if type(A) != type(None):
            try:
                self.reactions[react_idx].A = float(A)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for A was not a numeric, real number.')
                raise TypeError('You must input a real number for A. Hint: you may have put in a list.')

        if type(b) != type(None):
            try:
                self.reactions[react_idx].b = float(b)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for b was not a numeric, real number.')
                raise TypeError('You must input a real number for b. Hint: you may have put in a list.')

        if type(E) != type(None):
            try:
                self.reactions[react_idx].E = float(E)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for E was not a numeric, real number.')
                raise TypeError('You must input a real number for E. Hint: you may have put in a list.')

        if type(R) != type(None):
            try:
                self.reactions[react_idx].R = float(R)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for R was not a numeric, real number.')
                raise TypeError('You must input a real number for R. Hint: you may have put in a list.')

        if type(k) != type(None):
            try:
                self.reactions[react_idx].k = float(k)
            except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('Your input  for R was not a numeric, real number.')
                raise TypeError('You must input a real number for R. Hint: you may have put in a list.')

        if type(coeftype) != type(None):
            if coeftype in ['modifiedArrhenius','Arrhenius','Constant']:
                self.reactions[react_idx].coeftype = coeftype
            else:
                raise ValueError('Your input for coeftype was {coeftype}, not an available option')


    def get_reactions(self,name):
        """ This function takes in the name of the input xml file, and returns a dictionary of relevant information for
            a set of chemical reactions
        ------
        Args: name: name of the input xml file
        ------
        Returns: reaction_dict, dictionary of data for a reaction.  Contains the following keys:
                 reaction_dict['species'] : list of strings, species of the reaction
                 reaction_dict['As']: list of floats, corresponding to reaction parameter A for each equation
                                               = 0 for any equations that don't use A.
                 reaction_dict['bs']: list of floats, corresponding to reaction parameter b for each equation
                                               = 0 for any equations that don't use b.
                 reaction_dict['Es']: list of floats, corresponding to reaction parameter E for each equation
                                               = 0 for any equations that don't use E.
                 reaction_dict['ks']: list of floats, corresponding to reaction parameter k for each equation
                                               = 0 for any equations that don't use k (ie, non-constant equations).
                 reaction_dict['rxn_types']: List of strings. Elements Correspond to same reactions as reaction_parameters.
                                               Each string is one of { 'Arrhenius', 'modifiedArrhenius', 'Constant' }
                 reaction_dict['vprime'] : np array, full vprime matrix of all reactions in the xml file
                 reaction_dict['v2prime'] : np array, full v2prime matrix of all reactions in the xml file
                 reaction_dict['reversible'] : List of True or False, indicating if the type of each reaction in order
        """
        if os.stat(name).st_size == 0:
            raise FileNotFoundError("File is empty.  Hint: Double-check xml file contents")

        reaction_dict = {'reactions':[]}
        tree = ET.parse(name)
        chemical_reactions = tree.getroot()
        if chemical_reactions == []:
            raise ValueError('Unable to locate reaction data in xml')

        # Get the list and number of species
        species_list = []
        for ele in chemical_reactions.iter('phase'):
            for e in ele.find('speciesArray').text.split():
                species_list.append(e)
        reaction_dict['species'] = np.array(species_list)
        if species_list == []:
            raise ValueError('Invalid species list in xml')

        # Check if the reaction is reversible
        valid_atrribs = set(['yes', 'no'])

        # Check for empty reactions
        reactions_list = chemical_reactions.find('reactionData').findall('reaction')
        if reactions_list == []:
            raise ValueError('Invalid reactions list in xml')

        for reaction_data in reactions_list:
            react = {}
            reversible_attrib = reaction_data.get('reversible')
            type_attrib = reaction_data.get('type')

            # Check if there exists a tag for reversible and type
            if reversible_attrib == None:
                raise ValueError('Unspecified reversible type: missing reversible tag. Hint: check if you include a \
                                reversible tag for every reaction.')
            if type_attrib == None:
                raise ValueError('Unspecified Elementary type: missing type tag. Hint: check if you include a tag type \
                                indicating if the reaction is elementary or not.')

            # Check if the reversible tag is yes or no
            if reversible_attrib not in valid_atrribs:
                raise ValueError('Attributes of reversible tag invalid. Hint: check the content of the reversible tag.\
                                 Must be "yes" or "no".')

            # Append the list indicating reversible reactions or not
            if reversible_attrib == 'yes':
                react['reversible'] = True
            else:
                react['reversible'] = False

            # Check the type tag, only support Elementary type at this point
            if type_attrib != 'Elementary':
                raise NotImplementedError('Module can only support elementary reaction at this point. Hint: input type \
                                        for reactions maybe invalid.')

            valid_rc = ['Arrhenius','modifiedArrhenius','Constant']

            for coeff_set in reaction_data.find('rateCoeff'):
                if coeff_set.tag not in valid_rc:
                    raise ValueError('There is no valid tag called'.format(coeff_set.tag))
                react['coeftype'] = coeff_set.tag

                if coeff_set.tag == 'Arrhenius':
                    # Check if received unwanted value for a Arrhenius reaction coefficient
                    b = coeff_set.find('b')
                    k = coeff_set.find('k')
                    if b != None:
                        print('warning: received a b value for Arrhenius reaction rate coefficient. Replace with 0.')
                    if k != None:
                        print('warning: received a k value for Arrhenius reaction rate coefficient. Replace with 0.')
                    react['b'] = 0
                    react['k'] = 0

                    react['A'] = float(coeff_set.find('A').text)
                    react['E'] = float(coeff_set.find('E').text)

                elif coeff_set.tag == 'modifiedArrhenius':
                    # Check if received unwanted value for a modified Arrhenius reaction coefficient
                    k = coeff_set.find('k')
                    if k != None:
                        print('warning: received a k value for modified Arrhenius reaction rate coefficient. Replace with 0.')
                    react['k'] = 0

                    react['A'] = float(coeff_set.find('A').text)
                    react['b'] = float(coeff_set.find('b').text)
                    react['E'] = float(coeff_set.find('E').text)
                elif coeff_set.tag == 'Constant':
                    # Check if received unwanted value for a constant reaction coefficient
                    A = coeff_set.find('A')
                    b = coeff_set.find('b')
                    E = coeff_set.find('E')
                    if A != None:
                        print('warning: received a A value for a constant reaction rate coefficient. Replace with 0.')
                    if b != None:
                        print('warning: received a b value for constant reaction rate coefficient. Replace with 0.')
                    if E != None:
                        print('warning: recieved a E value for constant reaction rate coefficient. Replace with 0.')
                    react['A'] = 0
                    react['b'] = 0
                    react['E'] = 0

                    react['k'] = float(coeff_set.find('k').text)


            # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
            vprime = np.zeros((len(species_list),1))


            # Find the reactants data
            reactants_text = reaction_data.find('reactants').text

            # Split the data
            for specie_concentration in reactants_text.split(' '):

                # Get the name of the specie and its concentration
                specie = specie_concentration.split(':')[0]
                concentration = float(specie_concentration.split(':')[1])
                vprime[species_list.index(specie)] = concentration # Update at the index


            react['vprime'] = np.array(vprime)

            # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
            v2prime = np.zeros((len(species_list),1))


            # Find the reactants data
            products_text = reaction_data.find('products').text

            # Split the data
            for specie_concentration in products_text.split(' '):

                # Get the name of the specie and its concentration
                specie = specie_concentration.split(':')[0]
                concentration = float(specie_concentration.split(':')[1])
                v2prime[species_list.index(specie)] = concentration  # Update at the index



            react['v2prime'] = np.array(v2prime)
            reaction_dict['reactions'].append(react)

        return reaction_dict


# Elementary Reaction
class Reaction:
    """This class represents the abstract class for all Elementary reactions.
    It is used as the base class for both irreversible and reversible reactions.
    The class holds the related information to one reaction in a set of reactions,
    and has functions to calculate the reaction coefficients, progress rate, and
    overall reaction rate.
    =========
    Methods:
        reaction_coef(T): returns the reaction coefficients in the form (forward coef, backward coef).
                        NOTE: if the reaction is irreversible and there is no backward coef, this function
                        will return (forward coef, None)
        progress_rate(x,T): will return the progress rate for the reaction
        reaction_rate(x,T): will return the reaction rate for the reaction
    ---------
    NOTE: This is the base class and will raise NotImplementedError in several methods if used like the subclasses.
    """
    def __init__(self, react_dict, species):
        self.species = species
        self.react_dict = react_dict
        self.vprime = self.react_dict['vprime']
        self.v2prime = self.react_dict['v2prime']
        self.rev = self.react_dict['reversible']

        # Check for equal shapes in v' and v''
        if self.vprime.shape!=self.v2prime.shape:
            raise ValueError('The vprime and v2prime vectors must be the same size.')

        # Make sure every parameter for A,b,E,k comes in as a float
        try:
            self.A = float(self.react_dict['A'])
            self.b = float(self.react_dict['b'])
            self.E = float(self.react_dict['E'])
            self.k = float(self.react_dict['k'])
            self.R = 8.314
        except (TypeError, ValueError) as err:
                if type(err) == ValueError:
                    raise ValueError('You must input a numeric, real number data type for all parameters.')
                raise TypeError('You must input a real number. Hint: you may have put in a list.')

        # Validate input model types
        valid_types = ['modifiedArrhenius','Arrhenius','Constant']
        if self.react_dict['coeftype'] in valid_types:
            self.coeftype = self.react_dict['coeftype']
        else:
            raise ValueError("Your input file gave, {}, not valid reaction coefficients type.".format( \
                                                                         self.react_dict['coeftype']))

        # Check A values only for Arrhenius and modified Arrhenius reactions
        arrhenius_types = ['modifiedArrhenius','Arrhenius']
        if self.coeftype in arrhenius_types:
            if self.A <= 0:
                raise ValueError('Your A value should be strictly positive. Hint: an A value is less than 0')

    def __str__(self):
        return "vprime: {1}, v2prime: {2}, A: {3}, b: {4}, E: {5}, k: {6}, coeftypes: {7}".format( \
                 self.vprime, self.v2prime, self.A, self.b, self.E, self.k, self.coeftype)

    def _arrhenius(self, T):
        """ This function takes in the parameter T (kelvin temperature)
        from the class attributes, and it will return a value, k (the forward k), that is the
        Arrhenius reaction rate coefficient.
        ---------
        Args: T, float; temperature, (gets args from class)
        ---------
        Returns: The float k where k is the reaction rate coefficient.
        ---------
        Raises: OverflowError after constant evaluation
                FloatingPointError after constant evaluation for underflow
        """
        k = self.A*np.exp(-self.E/(self.R*T))
        if k == float('inf'):
            raise OverflowError('overflow error in evaluation of constant')
        if k <= np.finfo(float).eps:
            raise FloatingPointError('underflow error in evaluation of constant')
        return k

    def _mod_arrhenius(self, T):
        """ This function takes in the parameter T (kelvin temperature)
        from the class attributes, and it will return a value, k (the forward k), that is the
        modified Arrhenius reaction rate coefficient.
        ---------
        Args: T, float; temperature (gets args from class)
        ---------
        Returns: The float k where k is the reaction rate coefficient.
        ---------
        Raises: OverflowError after constant evaluation
                FloatingPointError after constant evaluation for underflow
        """
        if self.b==0:
            print('Warning: You are using modified arrhenius with b=0')
        k = self.A*(T**self.b)*np.exp(-self.E/(self.R*T))
        if k == float('inf'):
            raise OverflowError('overflow error in evaluation of constant')
        if k <= np.finfo(float).eps:
            raise FloatingPointError('underflow error in evaluation of constant')
        return k

    def reaction_coef(self,T):
        # wrapper for reaction coef forward and backward
        return self.reaction_coef_forward(T), self.reaction_coef_backward(T)

    def reaction_coef_forward(self, T):
        """Set reaction coefficients for the given float T.
        -------
        Args: T; float; the temperature for all reactions
        -------
        Returns: None
        -------
        Raises: ValueError when T cannot be cast to a float or T is negative
        """
        try:
            temp = float(T)
        except (TypeError, ValueError) as err:
            raise err('Your value for temp must be a float, not {}'.format(T))

        if temp < 0:
            raise ValueError('Your T value should be positive. It was {}.'.format(temp))

        if self.coeftype == 'Constant':
            if self.k == 0:
                print('warning. you are using a constant k with k=0')
            pass
        elif self.coeftype == 'Arrhenius':
            self.k = self._arrhenius(temp)
        else:
            self.k = self._mod_arrhenius(temp)
        return self.k

    def reaction_coef_backward(self, T):
        raise NotImplementedError()

    def progress_rate(self, x, T):
        raise NotImplementedError()


    def reaction_rate(self,x_in,T):
        """ This function calculates the reaction rate of a reaction of the following form:
                    V'11*A + V'21*B -> V''31*C
        It taken in the vectors v', v'' from the class and x in the order [[A],[B],[C]].
        -------
        Args: x; vector, numpy array (or list) of length equal to the number of
                    reactants in the system of equations.
              T; float, the strictly positive temperature
        -------
        Returns: vector of floats; the reaction rate for the equation
        -------
        Raises: ValueError when temp is less than 0 or x is not of shape (mx1)
        =======

        Doctests for this method in ReactionSet class

        """
        try:
            x = np.copy(np.array(x_in).reshape(-1,1))
        except:
            raise ValueError('You need to input a numpy array or a list for your x vector')

        m,n = self.vprime.shape

        if x.shape != (m,1):
            raise ValueError('The x vector must be the same height as your v matrices, but it was {}'.format(x.shape[0]))

        try:
            temp = float(T)
        except (TypeError, ValueError) as err:
            raise ValueError('Your value for temp must be a float, not {}'.format(T))

        if temp < 0:
            raise ValueError('Your T value should be positive. It was {}.'.format(temp))

        w = self.progress_rate(x,T)
        v = self.v2prime - self.vprime
        f = np.array([v[i][0]*w for i in range(m)])
        return f

class IrreversibleReaction(Reaction):
    """ This class represents irreversible reactions.  It inherits from the base Reaction class, and implements
    the method progress rate in the manner needed for this type of reaction.
    """
    def __init__(self, react_dict, species):
        super().__init__(react_dict, species)

        if self.rev:
            raise ValueError('You put a reversible reaction in the irreversible reaction class.')


    def reaction_coef_backward(self, T):
        """Function not implemented for anything more than consistent pronting for this class"""
        return

    def progress_rate(self, x_in, T):
        """ This function calculates the progress rate of a irreversible reaction of the following form:
                    V'11*A + V'21*B -> V''31*C
                V'12*A + V'32*C -> V''22*B + V''32*C
        It taken in the vectors v', v'' and x in the order [[A],[B],[C]].
        -------
        Args: v',v'', matrices, numpy arrays of form mxn where m is the number of reactants and n is number of equations.
              x; vector, numpy array (or list of lists) of length equal to the number of reactants in the system of equations.
              k; float or list of length n (number of equations), the k constant in the reaction of elementary equations.
        -------
        Returns: list of floats; the progress rate of the irreversible reaction for each equation
        -------
        Raises: ValueError if the shapes of the v matrices are not equal or if the x vector is not mx1
                    or if the value for T cannot be cast to a float.
        =======

        Doctest for this method in class

        """
        try:
            x = np.copy(np.array(x_in).reshape(-1,1))
        except:
            raise ValueError('You need to input a numpy array or a list for your x vector')

        m,n = self.vprime.shape
        if x.shape != (m,1):
            raise ValueError('The x vector must be the same height as your v vector, but it was {}'.format(x.shape[0]))

        try:
            temp = float(T)
        except (TypeError, ValueError) as err:
            raise type(err)('Your value for temp must be a float, not {}'.format(T))

        if temp < 0:
            raise ValueError('Your T value should be positive. It was {}.'.format(temp))

        k = self.reaction_coef_forward(temp)
        self.w = k*reduce((lambda x,y: x*y),np.power(x.T[0],self.vprime.T[0]))
        return self.w

class ReversibleReaction(Reaction):
    """ This class represents reversible reactions.  It inherits from the base Reaction class, and implements
    the methods for the progress rate, and backward reaction coefficient in the manner needed for this type
    of reaction. This class also queries the NASA coefficients for the backward reaction coefficients.
    =========
    NOTE: If the temperature you enter is equal to the split point for the NASA coefficient range,
            you will get the LOWER of the possible ranges.
    """
    def __init__(self, react_dict, species):
        super().__init__(react_dict, species)
        self.p0 = 1.0e+05
        self.kb = 0

        if not self.rev:
            raise ValueError('You put an irreversible reaction in the reversible reaction class.')

    def __str__(self):
        return "vprime: {1}, v2prime: {2}, A: {3}, b: {4}, E: {5}, k: {6}, kb: {7}, coeftypes: {8}".format( \
                 self.vprime, self.v2prime, self.A, self.b, self.E, self.k, self.kb, self.coeftype)

    def get_nasa_coefs(self, T):
        """This function getsthe NASA coefficients for a specific temperature.
        --------
        Args: T; float, temperature.
        --------
        Returns: numpy array mx7 where m is the number of species in the reaction system.
        --------
        Raises: ValueError if the query returns nothing.
         """
        db_loc = os.path.join(BASE_DIR, "supporting/COEF.sqlite")
        db = sqlite3.connect(db_loc)
        cursor = db.cursor()
        species_sql = ''

        query = self.get_query(cursor, T)
        q_result = cursor.execute(query).fetchall()
        if q_result == []:
            raise ValueError('Invalid temperature range for a species type.')
        out = []

        # Sort the SQL output by species
        for s in self.species:
            for row in q_result:
                if row[0]==s:
                    out.append(row[1:])

        out = np.array(out)

        return out

    def get_query(self, cursor, T):
        """This function gets the proper query to use to query the NASA coefficient
        SQLite database. It also checks for invalid temoeratures in the given value.
        --------
        Args: cursor; cursor for the database that holds the NASA coefficients.
              T; float, temperature.
        --------
        Returns: query, string
        --------
        Raises: ValueError if the temperature is either above the allowable max
                    value or below the min allowable value for the NASA coefficient
                    database.
        """
        # Get the species in a usable format
        species_sql = ''
        for s in self.species:
            species_sql+=str('"%s",'%s)

        # The purpose of the :-1 slice below is to drop the final , in the string
        qq = ''' SELECT MIN(TLOW), MAX(THIGH), SPECIES_NAME FROM COEF_SQL
            WHERE SPECIES_NAME in ('''+species_sql[:-1]+''')
            GROUP BY SPECIES_NAME '''
        ranges = cursor.execute(qq).fetchall()
        for r in ranges:
            if T <r[0]:
                raise ValueError('Your temperature {0} was less or equal to the \
                                 min possible, {1} for specie {2}'.format(T,r[0],r[2]))
            if T > r[1]:
                raise ValueError('Your temperature {0} was greater than the \
                                 max possible, {1} for specie {2}'.format(T,r[1],r[2]))
        temp = np.copy(T)
        if any([temp==r[0] for r in ranges]):
            temp+=1

        query = ''' SELECT SPECIES_NAME, COEFF_1, COEFF_2, COEFF_3, COEFF_4, COEFF_5, COEFF_6, COEFF_7
                    FROM COEF_SQL
                    WHERE SPECIES_NAME in ('''+species_sql[:-1]+''') AND '''+str(temp)+''' >
                    TLOW AND '''+str(temp)+''' <=THIGH '''
        return query

    def reaction_coef_backward(self, T):
        """ This function gets the backward coefficients for the given temperature.
        ---------
        Args: T; float, temperature.
        ---------
        Returns: float; the backwards reaction coefficient.
        """
        a = self.get_nasa_coefs(T)
        v = self.v2prime - self.vprime
        gamma = np.sum(v)

        # Not used, but present for completeness
        # Cp_R = (a[:,0] + a[:,1] * T + a[:,2] * T**2.0 + a[:,3] * T**3.0 + a[:,4] * T**4.0)

        H_RT = (a[:,0] + a[:,1] * T / 2.0 + a[:,2] * T**2.0 / 3.0 + a[:,3] * T**3.0 / 4.0 \
                                                               + a[:,4] * T**4.0 / 5.0 + a[:,5] / T)

        S_R = (a[:,0] * np.log(T) + a[:,1] * T + a[:,2] * T**2.0 / 2.0 + a[:,3] * T**3.0 / 3.0 \
                                                                   + a[:,4] * T**4.0 / 4.0 + a[:,6])

        # Change in enthalpy and entropy for each reaction
        delta_H_over_RT = np.dot(v.T, H_RT)#/(self.R*T)
        delta_S_over_R = np.dot(v.T, S_R)#/T

        # Negative of change in Gibbs free energy for each reaction
        delta_G_over_RT = delta_S_over_R - delta_H_over_RT

        # Prefactor in Ke
        fact = self.p0 / self.R / T

        # Ke
        ke = fact**gamma * np.exp(delta_G_over_RT)
        kf = self.reaction_coef_forward(T)
        self.kb = float(kf / ke)

        return self.kb

    def progress_rate(self, x_in, T):
        """ This function calculates the progress rate of a reversible reaction of the following form:
                    V'11*A + V'21*B -> V''31*C
                V'12*A + V'32*C -> V''22*B + V''32*C
        It taken in the vectors v', v'' and x in the order [[A],[B],[C]].
        -------
        Args: v',v'', matrices, numpy arrays of form mxn where m is the number of reactants and n is number of equations.
              x; vector, numpy array (or list of lists) of length equal to the number of reactants in the system of equations.
              k; float or list of length n (number of equations), the k constant in the reaction of elementary equations.
        -------
        Returns: list of floats; the progress rate of the reversible reaction for each equation
        -------
        Raises: ValueError if the shapes of the v matrices are not equal or if the x vector is not mx1
                    or if the value for T cannot be cast to a float.
        =======

        Doctest for this method in class

        """
        try:
            x = np.copy(np.array(x_in).reshape(-1,1))
        except:
            raise ValueError('You need to input a numpy array or a list for your x vector')

        m,n = self.vprime.shape

        if x.shape != (m,1):
            raise ValueError('The x vector must be the same height as your v vector, but it was {}'.format(x.shape[0]))

        try:
            temp = float(T)
        except (TypeError, ValueError) as err:
            raise type(err)('Your value for temp must be a float, not {}'.format(T))

        if temp < 0:
            raise ValueError('Your T value should be positive. It was {}.'.format(temp))

        k = self.reaction_coef_forward(temp)
        kb = self.reaction_coef_backward(temp)
        self.w = k*reduce((lambda x,y: x*y),np.power(x.T[0],self.vprime.T[0])) \
                           - kb*reduce((lambda x,y: x*y),np.power(x.T[0],self.v2prime.T[0]))
        return self.w

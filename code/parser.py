import xml.etree.ElementTree as ET
import numpy as np

def parser(name):
    """ This function takes in the name of the input xml file and returns a dictionary of relevant information regarind
        a set if chemical reactions
    ------
    Args: name, name of the input xml file
    ------
    Returns: reaction_dict, dictionary of data for a reaction
             reaction_dict['species'] : list, species of the reaction
             reaction_dict['num_species'] : int, number of species in the reaction
             reaction_dict['index_of_specie'] : dictionary, stores the index of a reactant, can be accessed by:
                                               reaction_dict['index_of_specie']['H2']
             reaction_dict['num_equations'] : int, number of equations in the reaction
             reaction_dict['reaction_parameters'] : list of list, stores the correspond parameters for a equation,
                                                    for example, want to access the parameters for reaction1:
                                                    reaction_dict['reaction_parameters'][0]
                                                    for example, want to access the parameters for reaction2:
                                                    reaction_dict['reaction_parameters'][1]
             reaction_dict['vprime'] : np array, vprime
             reaction_dict['v2prime'] : np array, v2prime
    """
    reaction_dict = {}
    tree = ET.parse(name)
    chemical_reactions = tree.getroot()

    # Get the list and number of species
    species_list = []
    for ele in chemical_reactions.iter('phase'):
        for e in ele.find('speciesArray').text.split():
            species_list.append(e)
    reaction_dict['species'] = species_list
    reaction_dict['num_species'] = len(species_list)
    reaction_dict['index_of_specie'] = dict(zip(species_list,list(range(len(species_list)))))

    # Get the number of equations
    reaction_dict['num_equations'] = len(chemical_reactions.find('reactionData').findall('reaction'))

    # Get the reaction rate parameters for each reaction
    reaction_parameters = []
    for reaction_data in chemical_reactions.find('reactionData').findall('reaction'):
        reaction_data = reaction_data.find('rateCoeff').find('Arrhenius')
        A = float(reaction_data.find('A').text)
        b = float(reaction_data.find('b').text)
        E = float(reaction_data.find('E').text)
        reaction_parameters.append([A,b,E])
    reaction_dict['reaction_parameters'] = reaction_parameters

    # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
    vprime = np.zeros((reaction_dict['num_species'], reaction_dict['num_equations']))
    num_reaction_count = 0
    for reaction_data in chemical_reactions.find('reactionData').findall('reaction'):

        # Find the reactants data
        reactants_text = reaction_data.find('reactants').text

        # Split the data
        for specie_concentration in reactants_text.split(' '):

            # Get the name of the specie and its concentration
            specie = specie_concentration.split(':')[0]
            concentration = float(specie_concentration.split(':')[1])
            vprime[reaction_dict['index_of_specie'][specie]][num_reaction_count] = concentration # Update at the index

        # Move to the next equation
        num_reaction_count += 1

    reaction_dict['vprime'] = vprime

    # Get the reactants for the 'vprime' matrix and arrange the vprime matrix
    v2prime = np.zeros((reaction_dict['num_species'], reaction_dict['num_equations']))
    num_reaction_count = 0
    for reaction_data in chemical_reactions.find('reactionData').findall('reaction'):

        # Find the reactants data
        products_text = reaction_data.find('products').text

        # Split the data
        for specie_concentration in products_text.split(' '):
            # Get the name of the specie and its concentration
            specie = specie_concentration.split(':')[0]
            concentration = float(specie_concentration.split(':')[1])
            v2prime[reaction_dict['index_of_specie'][specie]][num_reaction_count] = concentration  # Update at the index

        # Move to the next equation
        num_reaction_count += 1

    reaction_dict['v2prime'] = v2prime

    return reaction_dict

name = 'sample_input.xml'
dict = parser(name)
print(dict)
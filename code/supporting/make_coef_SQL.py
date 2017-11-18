import sqlite3
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def drop_empty(this_list):
    """
    # SOURCE: ADAPTED FROM HCS207 HOMEWORK 9 SOLUTION - RYAN JANSSEN
    Helper function to remove empty items from a list.
    Used in parsing the string lists from the text file.
    """
    return list(filter(None, this_list))

def get_line_floats(this_line):
    """
    # SOURCE: ADAPTED FROM HCS207 HOMEWORK 9 SOLUTION - RYAN JANSSEN
    Helper function to drop the non-coefficient characters in a string
    and turn the remaining string into a list of coefficients (in float).
    Used by get_species_list to convert each line of coefficients
    to float.
    """
    # Drop trailing line number and zeroes
    this_line = this_line[:-1].rstrip()

    # Create list where each element is 15 consecutive characters of this_line
    n = 15  # Number of digits for each float in this_line
    return [float(this_line[i:i + n]) for i in range(0, len(this_line), n)]


def get_species_list(filename):
    """
    # SOURCE: ADAPTED FROM HCS207 HOMEWORK 9 SOLUTION - RYAN JANSSEN
    Pulls the species data from the specified file location (in string).
    Works with any number of species, but the species must be formatted
    into four lines indicated by trailing (1, 2, 3, 4) and two
    temperature ranges.
    --------
    Args: filename: String containing
    --------
    Returns: species_list: A list of dictionaries for each species.
                Dictionary format is:
                    this_specie['specie_name'] = Species name
                    this_specie['mid_temp'] = Mid-range temperature point
                    this_specie['high_temp'] = Upper temperature bound
                    this_specie['low_temp'] = Lower temperature bound
                    this_specie['P0'] = Pressure (assumed to be 100000.0)
                    this_specie['high_range_poly'] = List of 7 floats
                        corresponding to range [mid_temp, high_temp]
                    this_specie['low_range_poly'] = List of 7 floats
                        corresponding to range [low_temp, mid_temp]
    --------
    Raises: ValueError if file is not truncated with END in final line
            ValueError if file is not truncated with 4 in penultimate line
    """
    # Open and parse text file into lines
    thermo_loc = os.path.join(BASE_DIR, filename)
    with open(thermo_loc, "r") as file:
        th = file.read()
        lines = drop_empty(th.split('\n'))

    # Input error checking
    if lines[-1] != 'END' or lines[-2][-1] != '4':
        raise ValueError('Error: Invalid text input')

    species_list = []  # List of dictionaries (one for each species)
    for i in range(len(lines)):

        if lines[i][-1] == '1':  # Starting a new specie
            # Each line must be parsed separately because NASA decided
            # to take away the bloody space for negative coefficients
            this_specie = dict()

            # Add first line information into dictionary
            header_line = drop_empty(lines[i].split(' '))
            this_specie['specie_name'] = header_line[0]
            this_specie['mid_temp'] = header_line[-2]
            this_specie['high_temp'] = header_line[-3]
            this_specie['low_temp'] = header_line[-4]
            # Assuming all species are P0 = 100000.0 since there's no record in the .txt
            this_specie['P0'] = '100000.0'

            # Add high range polynomials
            poly_coefs = get_line_floats(lines[i + 1]) + get_line_floats(lines[i + 2]) + get_line_floats(lines[i + 3])
            this_specie['high_range_poly'] = poly_coefs[0:7]
            this_specie['low_range_poly'] = poly_coefs[7:14]

            species_list.append(this_specie)

    return species_list

def coef_sql(species_list):
    """
        # SOURCE: ADAPTED FROM HCS207 HOMEWORK 9 SOLUTION - RYAN JANSSEN
        !!!
    """
    # Instantiate SQLite database
    db_loc = os.path.join(BASE_DIR, "../COEF.sqlite")
    db = sqlite3.connect(db_loc)

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS COEF_SQL")

    # Create COEF_SQL table
    cursor.execute('''CREATE TABLE COEF_SQL (
              ID INT PRIMARY KEY NOT NULL,
              SPECIES_NAME TEXT,
              TLOW FLOAT,
              THIGH FLOAT,
              COEFF_1 FLOAT,
              COEFF_2 FLOAT,
              COEFF_3 FLOAT,
              COEFF_4 FLOAT,
              COEFF_5 FLOAT,
              COEFF_6 FLOAT,
              COEFF_7 FLOAT)''')
    db.commit()

    # Output each species information to table COEF_SQL
    id = 0
    for specie in species_list:  # Iterate over species in dictionary
        # Add low_range coefficient set to COEF_SQL for given species
        vals_to_insert = ((id,
                          specie['specie_name'],
                          specie['low_temp'],
                          specie['mid_temp']) +
                          tuple(specie['low_range_poly']))
        cursor.execute('''INSERT INTO COEF_SQL (ID, SPECIES_NAME, TLOW, THIGH,
                               COEFF_1, COEFF_2, COEFF_3, COEFF_4, COEFF_5, COEFF_6, COEFF_7)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', vals_to_insert)

        # Add high_range coefficient set to COEF_SQL for given species
        vals_to_insert = ((id+1,
                           specie['specie_name'],
                           specie['mid_temp'],
                           specie['high_temp']) +
                          tuple(specie['high_range_poly']))
        cursor.execute('''INSERT INTO COEF_SQL (ID, SPECIES_NAME, TLOW, THIGH,
                                   COEFF_1, COEFF_2, COEFF_3, COEFF_4, COEFF_5, COEFF_6, COEFF_7)
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', vals_to_insert)
        id += 2

    db.commit()
    db.close()


# Parse thermo.txt and import into COEF.SQLITE
coef_sql(get_species_list('thermo.txt'))

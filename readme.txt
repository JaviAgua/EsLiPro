"""
# =============================================================================
# Readme
# =============================================================================
"""
This script works with two text files. Each text file must consist of a series
Of items separated by an underscore sign "_"
An acceptable example of a valid file with tokens is reproduced below:
a_x
b_x
c_x
a_y
computer_x
keyboard_x
a_earth
b_wind
c_fire
a_x

All items located before the underscore sign are considered *prefixes*.
All items located after the underscore sign are considered *suffixes*.



The script runs the following operations:
1) An estimation of creativity (CRE) is made for the two text files
(e.g. "a" is used with three different suffixes: x, y and earth)
2) An estimation of triteness (TRI) is made for the two text files
(e.g. "y" has a value of 1 because it is only used with one prefix)
3) Since two files are read, a series of random samples are extracted from the
largest one (maximum number of iterations is 1000)
4) A new compute of CRE and TRI is made for the series of random samples
5) A table is produced with the values of CRE and TRI for all three samples
6) A feedback file is also created with a summary of the main results
7) Other datasets for potential further analyses are also created 
(as described in the feedback file)
"""

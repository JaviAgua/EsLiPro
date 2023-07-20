
# =============================================================================
# Readme
# =============================================================================

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
Characters different than letters MUST be avoided, particularly the pipe sign "|", but also ":" and "-"
#In this version (v2) all non-letters are replaced by the txt "xx"



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


# =============================================================================
# Contents
# =============================================================================

# {0} Modules and data reading
# {00.a} Modules
# {00.b} Data reading

# {01}  Count the number of tokens and types in one sample (Sample 1)
# {01.a} Create a table with four columns Sample','Position','Morpheme','CRE' for preffixes
# {01.b} Create a table with four columns Sample','Position','Morpheme','CRE' for suffixes
# {01.c} Make a first compute of overall productivity for the first file

# {02} Count the number of tokens and types in a second file (Sample 2)
# {02.a} Create a table with four columns Sample','Position','Morpheme','CRE' for preffixes
# {02.b} Create a table with four columns Sample','Position','Morpheme','CRE' for suffixes
# {02.c} Make a first compute of overall productivity for the second file

# {03} First control: check for the vocabulary of prefixes and suffixes across samples
# {03.a} Filter cases from Sample 2 with the types existing in Sample 1
# {03.b} Filter cases from Sample 1 with the types existing in Sample 2
# {03.c} recalculate the amount of tokens after the first control
# {03.d} Create a new table with the new values of creativity for the filtered version of Sample 1
# {03.e} Create a new table with the new values of creativity for the filtered version of Sample 2
# {03.f} Global computes of creativity after the first comntrol (vocabulary)

# {04} Extract a series of random samples from the largest one

# {05} Analysis of TRI before controlling for vocabulary and sample size
# {05.a} Analysis of TRI before controlling for vocabulary and sample size
# {05.b} Analyses after controlling for vocabulary
# {05.c} Analyses after controlling for vocabulary and sample size

# {6} Histograms for CRE

# {7} Feedback files


"""






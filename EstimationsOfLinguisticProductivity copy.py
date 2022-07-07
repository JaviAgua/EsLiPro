#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 22:00:21 2022

@author: javier aguado-orea
Sheffield Hallam University

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
(e.g. "a" is used with four three different suffixes: x, y and earth)
2) An estimation of triteness (TRI) is made for the two text files
(e.g. "y" has a value of 1 because it is only used with one prefix)
3) Since two files are read, a series of random samples are extracted from the
largest one (maximum number of iterations is 1000)
4) A new compute of CRE and TRI is made for the series of random samples
5) A table is produced the values of CRE and TRI for all three samples
6) A feedback file is also created with a summary of the main results
7) Other datasets for potential further analyses are also created 
(as described in the feedback file(
"""


# =============================================================================
# Contents
# =============================================================================

# {0} Modules and data reading
# {00.a} Modules
# {00.b} Data reading

# {01}  Count the number of tokens and types in one sample (Sample 1)
# {01.a} Create a table with four columns Sample','Position','Morpheme','CRE' for preffixes
# {01.b} Create a table with four columns Sample','Position','Morpheme','CRE' for suffixes
# {01.c} Maje a first compute of overall productivity

# {02} Count the number of tokens and types in a second file (Sample 2)
# {02.a} Create a table with four columns Sample','Position','Morpheme','CRE' for preffixes
# {02.b} Create a table with four columns Sample','Position','Morpheme','CRE' for suffixes
# {02.c} Maje a first compute of overall productivity

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























# =============================================================================
# {0} Modules and data reading
# =============================================================================


# {00.a} Modules
# Import os.path to check if files extis
# https://docs.python.org/3/library/os.path.html
import os.path
# import RegEX to extract random samples
# https://docs.python.org/3/howto/regex.html
import re
# import Pandas to work with dataframes
# https://pandas.pydata.org/docs/index.html
import pandas as pd
# import Numpy to compute and compare values
# https://numpy.org/doc/stable/
import numpy as np
# import Sys to exit if both samples are identical
# https://docs.python.org/3/library/sys.html
import sys


# {00.b} Data reading

#A few of lines to ask for the first filename to read and check that it is typed correctly
#Get current working directory
cwd = os.getcwd()
#Print list of files in current working directory
from typing import List
path_dir: str = cwd
content_dir: List[str] = os.listdir(path_dir)
print(content_dir)
#Ask for the name of the first file
txtfile1 = input('Enter name of FIRST file:')
#Check if it exists, and a second (last) option otherwise
filecheck = os.path.isfile(txtfile1)
if filecheck == True:
    print ("File for Sample 1 found. ")
else:
    print ("File for Sample 1 could not be found. Try again: ")
    txtfile1 = input('Enter name of FIRST file:')

# Same procedure for the second file    
txtfile2 = input('Enter name of SECOND file:')
filecheck = os.path.isfile(txtfile2)
if filecheck == True:
    print ("File for Sample 2 found. ")
else:
    print ("File for Sample 2 wasn't found. Try again: ")
    txtfile2 = input('Enter name of SECOND file:')


#the txt files are now read as datasets with two columns
data1 = pd.read_csv(txtfile1, sep="_", header = None)
data2 = pd.read_csv(txtfile2, sep="_", header = None)

#the columns are named as prefix and suffix variables
data1.columns = ["prefix", "suffix"]
data2.columns = ["prefix", "suffix"]

#Add a thrid column with both, so data1 is now a dataframe with three colums: "prefix, suffix, construction"
data1["construction"] = data1[["prefix", "suffix"]].apply("_".join, axis=1)
data2["construction"] = data2[["prefix", "suffix"]].apply("_".join, axis=1)


#the frequencies of prefix and suffix are computed now
prefix_table1 = data1["prefix"].value_counts()
suffix_table1 = data1["suffix"].value_counts()
prefix_table2 = data2["prefix"].value_counts()
suffix_table2 = data2["suffix"].value_counts()

#number of tokens per file
ntokens1 = len(data1)
ntokens2 = len(data2)

#number of types per file and colum
ntypes_prefix1 = len(prefix_table1)
ntypes_prefix2 = len(prefix_table2)
ntypes_suffix1 = len(suffix_table1)
ntypes_suffix2 = len(suffix_table2)


#Lists of types per file and column too
types_pref_1 = set(data1["prefix"])
types_suff_1 = set(data1["suffix"])
types_cons_1 = set(data1["construction"])
types_pref_2 = set(data2["prefix"])
types_suff_2 = set(data2["suffix"])
types_cons_2 = set(data2["construction"])


































# =============================================================================
# {01} Analysis of Sample 1
# =============================================================================

# {01.a} A first compute of Creativity [CRE] is made for Sample 1, before controlling for vocabulary and sample size

# I create a new dataframe with four colums, the preffix and the number of types for Sample 1
CRE_Pre_Table_1 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in types_pref_1:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch = str(item) + '_'
    # STILL IMPORTANT: the boundary marker \b has to be added at the beginning, otherwise, when searching for "he" it would also find "sHE"
    searchitem=re.compile(r"\b"+safesearch)
    CRE_Pre_1 = re.findall(searchitem, str(types_cons_1))
    # it counts the number of types found (how creatively it was used)
    nCRE_Pre_1 = len(CRE_Pre_1)
    # it adds them to the dataframe, with the name of the type under "morpheme" and the creativity under "CRE"
    CRE_Pre_Table_1.loc[len(CRE_Pre_Table_1)] = [1,'Prefix',item,nCRE_Pre_1]


# {01.b} And now for suffixes
CRE_Suf_Table_1 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in types_suff_1:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch =  '_' + str(item)
    searchitem = re.compile(r'%s\b' % safesearch)
    CRE_Suf_1 = re.findall(searchitem, str(types_cons_1))
    # it counts the number of types found (how creatively it was used)
    nCRE_Suf_1 = len(CRE_Suf_1)
    # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
    CRE_Suf_Table_1.loc[len(CRE_Suf_Table_1)] = [1,'Suffix',item,nCRE_Suf_1]

# {01.c} And now an overall level of creativity is computed
# Creativity for Prefixes
CRE_Pre_Value_1 = CRE_Pre_Table_1['CRE'].mean()
CRE_Pre_Value_1_sd= CRE_Pre_Table_1['CRE'].std()
# Creativity for Suffixes
CRE_Suf_Value_1 = CRE_Suf_Table_1['CRE'].mean()
CRE_Suf_Value_1_sd = CRE_Suf_Table_1['CRE'].std()

#Values sorted by Morpheme too for the final table
CRE_Pre_Table_1 = CRE_Pre_Table_1.sort_values(by=['Morpheme'])
CRE_Suf_Table_1 = CRE_Suf_Table_1.sort_values(by=['Morpheme'])




























# =============================================================================
# {02} Analysis of Sample 2
# =============================================================================

# {02.a} A first compute of Creativity [CRE] is also made for Sample 2, before controlling for vocabulary and sample size

# I create a new dataframe with two colums, the preffix and the number of types for Sample 2
CRE_Pre_Table_2 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 2 starts here
for item in types_pref_2:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch = str(item) + '_'
    searchitem=re.compile(r"\b"+safesearch)
    CRE_Pre_2 = re.findall(searchitem, str(types_cons_2))
    # it counts the number of types found (how creatively it was used)
    nCRE_Pre_2 = len(CRE_Pre_2)
    # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
    CRE_Pre_Table_2.loc[len(CRE_Pre_Table_2)] = [2,'Prefix',item,nCRE_Pre_2]

# {02.b} And now for suffixes
CRE_Suf_Table_2 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in types_suff_2:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch =  '_' + str(item)
    searchitem = re.compile(r'%s\b' % safesearch)
    CRE_Suf_2 = re.findall(searchitem, str(types_cons_2))
    # it counts the number of types found (how creatively it was used)
    nCRE_Suf_2 = len(CRE_Suf_2)
    # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
    CRE_Suf_Table_2.loc[len(CRE_Suf_Table_2)] = [2,'Suffix',item,nCRE_Suf_2]

# {02.c} And now an overall level of creativity is computed
#Compute of the average level of creativity for prefixes
CRE_Pre_Value_2 = CRE_Pre_Table_2['CRE'].mean()
CRE_Pre_Value_2_sd= CRE_Pre_Table_2['CRE'].std()
#Compute of the average level of creativity for suffixes
CRE_Suf_Value_2 = CRE_Suf_Table_2['CRE'].mean()
CRE_Suf_Value_2_sd = CRE_Suf_Table_2['CRE'].std()


#Values sorted by Morpheme too for the final table
CRE_Pre_Table_2 = CRE_Pre_Table_2.sort_values(by=['Morpheme'])
CRE_Suf_Table_2 = CRE_Suf_Table_2.sort_values(by=['Morpheme'])






CRE_Pre_Value_1 = CRE_Pre_Table_1['CRE'].mean()
# Creativity for Suffixes
CRE_Suf_Value_1 = CRE_Suf_Table_1['CRE'].mean()
CRE_Suf_Value_1_sd = CRE_Suf_Table_1['CRE'].std()














# =============================================================================
# {03} Vocabulary match check
# =============================================================================

#Extract lists of types from the tables
Pre_Types_List1 = CRE_Pre_Table_1['Morpheme'].tolist()
Suf_Types_List1 = CRE_Suf_Table_1['Morpheme'].tolist()
Pre_Types_List2 = CRE_Pre_Table_2['Morpheme'].tolist()
Suf_Types_List2 = CRE_Suf_Table_2['Morpheme'].tolist()

#Order the lists
Pre_1 = sorted(Pre_Types_List1)
Suf_1 = sorted(Suf_Types_List1)
Pre_2 = sorted(Pre_Types_List2)
Suf_2 = sorted(Suf_Types_List2)


#Shared morphemes across samples 1 and 2, to include in the results doc
Shared_Prefix_Types = list(set(Pre_1) & set(Pre_2))
Shared_Prefix_Types_sorted = sorted(Shared_Prefix_Types)
nShared_Prefix_Types = len(Shared_Prefix_Types)


Shared_Suffix_Types = list(set(Suf_1) & set(Suf_2))
Shared_Suffix_Types_sorted = sorted(Shared_Suffix_Types)
nShared_Suffix_Types = len(Shared_Suffix_Types)


# {03.a} Filter cases from Sample 2 with the types existing in Sample 1
#First, filer cases from Sample 2 with prefixes existing in Sample 1
FILT_Pre = []
FILT_Pre_2 = pd.DataFrame(data= FILT_Pre)

for typepre1 in Pre_1:
    FILT_Pre_2_i = data2.query("prefix == @typepre1")
    FILT_Pre_2 = pd.concat([FILT_Pre_2_i, FILT_Pre_2])

#Then, filter cases from the already FILTERED Sample 2 with suffixes existing in Sample 1
FILT_Suf = []
FILT_2 = pd.DataFrame(data= FILT_Suf)

for typesuf1 in Suf_1:
    #Instead of data2, I am now using the filtered sample from data2
    FILT_2_i = FILT_Pre_2.query("suffix == @typesuf1")
    FILT_2 = pd.concat([FILT_2_i, FILT_2])



# {03.b} Filter cases from Sample 1 with the types existing in Sample 2
#First, filer cases from Sample 1 with prefixes existing in Sample 2
FILT_PrePre = []
FILT_Pre_1 = pd.DataFrame(data= FILT_PrePre)

for typepre2 in Pre_2:
    FILT_Pre_1_i = data1.query("prefix == @typepre2")
    FILT_Pre_1 = pd.concat([FILT_Pre_1_i, FILT_Pre_1])

#Then, filter cases from the already FILTERED Sample 2 with suffixes existing in Sample 1
FILT_SufSuf = []
FILT_1 = pd.DataFrame(data= FILT_SufSuf)

for typesuf2 in Suf_2:
    #Instead of data2, I am now using the filtered sample from data2
    FILT_1_i = FILT_Pre_1.query("suffix == @typesuf2")
    FILT_1 = pd.concat([FILT_1_i, FILT_1])


# {03.c} After checking for vocabulary, the amount of tokens is reduced, so it has to be recomputed
#number of tokens per file
ntokens1f = len(FILT_1)
ntokens2f = len(FILT_2)


#Piece of code not required follows, but kept just in case


#Extract constructions from sample1 into a list of tokens
#tokenscons1 = data1["construction"].tolist()
#tokenscons1 = sorted(tokenscons1)
#Extract constructions from sample2 into a list of tokens
#tokenscons2 = data2["construction"].tolist()
#tokenscons2 = sorted(tokenscons2)

#Lists of types per file and column too
FILT_types_pref_1 = set(FILT_1["prefix"])
FILT_types_suff_1 = set(FILT_1["suffix"])
FILT_types_cons_1 = set(FILT_1["construction"])
FILT_types_pref_2 = set(FILT_2["prefix"])
FILT_types_suff_2 = set(FILT_2["suffix"])
FILT_types_cons_2 = set(FILT_2["construction"])

# {03.d} Create a new table with the new values of creativity for the filtered version of Sample 1

# I create a new dataframe with four colums, the preffix and the number of types for the filtered version of Sample 1
CRE_Pre_FILT_1 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in FILT_types_pref_1:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch = str(item) + '_'
    searchitem=re.compile(r"\b"+safesearch)
    FILT_CRE_Pre_1 = re.findall(searchitem, str(FILT_types_cons_1))
    # it counts the number of types found (how creatively it was used)
    FILT_nCRE_Pre_1 = len(FILT_CRE_Pre_1)
    # it adds them to the dataframe, with the name of the type under "morpheme" and the creativity under "CRE"
    CRE_Pre_FILT_1.loc[len(CRE_Pre_FILT_1)] = [1,'Prefix',item,FILT_nCRE_Pre_1]



# And now for suffixes
CRE_Suf_FILT_1 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in FILT_types_suff_1:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch =  '_' + str(item)
    searchitem = re.compile(r'%s\b' % safesearch)
    FILT_CRE_Suf_1 = re.findall(searchitem, str(FILT_types_cons_1))
    # it counts the number of types found (how creatively it was used)
    FILT_nCRE_Suf_1 = len(FILT_CRE_Suf_1)
    # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
    CRE_Suf_FILT_1.loc[len(CRE_Suf_FILT_1)] = [1,'Suffix',item,FILT_nCRE_Suf_1]

# {03.e} Create a new table with the new values of creativity for the filtered version of Sample 2
# I create a new dataframe with four colums, the preffix and the number of types for the filtered version of Sample 2
CRE_Pre_FILT_2 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in FILT_types_pref_2:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch = str(item) + '_'
    searchitem=re.compile(r"\b"+safesearch)
    FILT_CRE_Pre_2 = re.findall(searchitem, str(FILT_types_cons_2))
    # it counts the number of types found (how creatively it was used)
    FILT_nCRE_Pre_2 = len(FILT_CRE_Pre_2)
    # it adds them to the dataframe, with the name of the type under "morpheme" and the creativity under "CRE"
    CRE_Pre_FILT_2.loc[len(CRE_Pre_FILT_2)] = [2,'Prefix',item,FILT_nCRE_Pre_2]


# And now for suffixes
CRE_Suf_FILT_2 = pd.DataFrame(columns=['Sample','Position','Morpheme','CRE'])
# A new loop with the size of the numbner of preffix types in Sample 1 starts here
for item in FILT_types_suff_2:
    # the most important line follows, using regular expressions
    # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
    # since it is in the loop, it goes item by item (e.g. verb by verb)
    # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
    safesearch =  '_' + str(item)
    searchitem = re.compile(r'%s\b' % safesearch)
    FILT_CRE_Suf_2 = re.findall(searchitem, str(FILT_types_cons_2))
    # it counts the number of types found (how creatively it was used)
    FILT_nCRE_Suf_2 = len(FILT_CRE_Suf_2)
    # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
    CRE_Suf_FILT_2.loc[len(CRE_Suf_FILT_2)] = [2,'Suffix',item,FILT_nCRE_Suf_2]


# {03.f} Global computes of creativity after the first comntrol (vocabulary)
#Compute of the average level of creativity after controlling for vocabulary
CRE_Pre_FILT_Value_1 = CRE_Pre_FILT_1['CRE'].mean()
CRE_Pre_FILT_Value_1_sd = CRE_Pre_FILT_1['CRE'].std()
#Compute of the average level of creativity after controlling for vocabulary
CRE_Suf_FILT_Value_1 = CRE_Suf_FILT_1['CRE'].mean()
CRE_Suf_FILT_Value_1_sd = CRE_Suf_FILT_1['CRE'].std()
#Compute of the average level of creativity after controlling for vocabulary
CRE_Pre_FILT_Value_2 = CRE_Pre_FILT_2['CRE'].mean()
CRE_Pre_FILT_Value_2_sd = CRE_Pre_FILT_2['CRE'].std()
#Compute of the average level of creativity after controlling for vocabulary
CRE_Suf_FILT_Value_2 = CRE_Suf_FILT_2['CRE'].mean()
CRE_Suf_FILT_Value_2_sd = CRE_Suf_FILT_2['CRE'].std()


#Values sorted by Morpheme too for the final table
CRE_Pre_FILT_1 = CRE_Pre_FILT_1.sort_values(by=['Morpheme'])
CRE_Suf_FILT_1 = CRE_Suf_FILT_1.sort_values(by=['Morpheme'])
CRE_Pre_FILT_2 = CRE_Pre_FILT_2.sort_values(by=['Morpheme'])
CRE_Suf_FILT_2 = CRE_Suf_FILT_2.sort_values(by=['Morpheme'])


























# =============================================================================
# {04} Extract a series of random samples from the largest one
# =============================================================================

#Compare the two files
#First, compare tokens
tokendiff = ntokens2f - ntokens1f


# Iterations start here

numiter = int(input("number of iterations to run (1000 maximum): "))
if numiter > 1000:
    numiter = 1000

#The long dataframes (now empty) where all iterations will be stored are created
CRE_Pre_Table_iter_Long = pd.DataFrame(columns = ["Iteration","Morpheme","CRE"])
CRE_Suf_Table_iter_Long = pd.DataFrame(columns = ["Iteration","Morpheme","CRE"])

#I start the
for iteration in range(numiter):
    #feedback about the progression of the iterationions
    print('iteration: ' + str(iteration+1) + ' of ' +str(numiter))
    if tokendiff == 0:
        #create a message
        msgtkn1 = 'Both files have the same size of tokens.'
        msgtkn2 = 'Nothing is done and the code stops here because both samples had the same size.'
        msgequalsamples = msgtkn1 + "\r\n" + msgtkn2
        print(msgequalsamples)
        sys.exit()

    elif tokendiff > 0:
        #create a message
        msgtkn1 = 'SECOND file is ' + str(tokendiff) + ' tokens LARGER'
        msgtkn2 = ' second file'
        msgtkn3 = str(ntokens1)
        #extract a sample from the second file+
        #the next line would be used without lexical control
        #txtfilesample = data2['construction'].sample(n=abs(ntokens1))
        #Alternatively, by default analyses are run over the filtered sample
        txtfilesample = FILT_2['construction'].sample(n=abs(ntokens1f))

    elif tokendiff < 0:
        #create a message
        msgtkn1 = 'SECOND file is ' + str(abs(tokendiff)) + ' tokens SMALLER'
        msgtkn2 = ' first file'
        msgtkn3 = str(ntokens2)
        #extract a sample from the first file
        #the next line would be used without lexical control
        #txtfilesample = data1['construction'].sample(n=abs(ntokens2))
        #Alternatively, by default analyses are run over the filtered sample
        txtfilesample = FILT_1['construction'].sample(n=abs(ntokens2f))


    #sort the output
    txtfilesample = txtfilesample.sort_values()
    #I give a name to a potential text file, although I am not using it
    #But it would be useful in case that I want to store somewhere
    txtfilesamplename = txtfile2[:-4]+'_sample.txt'
    #I convert the series to a csv (still not dataframe) so it is prepared to be read
    txtfilesample.to_csv(txtfilesamplename, header=False, index=False)
    #I read the random sample, sorted, as a series with two columns (still unnamed, but they will be prefix and suffix)
    dataiter = pd.read_csv(txtfilesamplename, sep="_", header = None)
    #the txt files are now read as a dataframe with two columns still unnamed
    dataiter = pd.DataFrame(dataiter)
    #the columns are named as prefix and suffix variables
    dataiter.columns = ["prefix", "suffix"]

    #Add a third column with both columns joined into one called 'construction' is created
    dataiter["construction"] = dataiter[["prefix", "suffix"]].apply("_".join, axis=1)

    # The count of types and tokens for the random sample starts here
    #the frequencies of prefix and suffix are computed now
    prefix_tableiter = dataiter["prefix"].value_counts()
    suffix_tableiter = dataiter["suffix"].value_counts()

    #number of tokens per file
    ntokensiter = len(dataiter)
    #number of types per file and colum
    ntypes_prefixiter = len(prefix_tableiter)
    ntypes_suffixiter = len(suffix_tableiter)

    #Lists of types per file and column too
    types_pref_iter = set(dataiter["prefix"])
    types_suff_iter = set(dataiter["suffix"])
    types_cons_iter = set(dataiter["construction"])


    # The corresponding compute of Creativity [CRE] is made for the extracted random sample, now called Sample 3


    # An empty dataframe with three colums, the preffix and the number of types for Sample 3 is created
    CRE_Pre_Table_iter = pd.DataFrame(columns=['Iteration','Morpheme','CRE'])
    # A new loop with the size of the numbner of prefix types in Sample 2 starts here
    for item in types_pref_iter:
        # the most important line follows, using regular expressions
        # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
        # since it is in the loop, it goes item by item (e.g. verb by verb)
        # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
        safesearch = str(item) + '_'
        searchitem=re.compile(r"\b"+safesearch)
        CRE_Pre_iter = re.findall(searchitem, str(types_cons_iter))
        # it counts the number of types found (how creatively it was used)
        nCRE_Pre_iter = len(CRE_Pre_iter)
        # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
        CRE_Pre_Table_iter.loc[len(CRE_Pre_Table_iter)] = [iteration,item,nCRE_Pre_iter]


    CRE_Pre_Table_iter_Long = pd.concat([CRE_Pre_Table_iter_Long,CRE_Pre_Table_iter], axis=0)


    # And now for suffixes
    # An empty dataframe with four colums, the preffix and the number of types for Sample 3 is created
    CRE_Suf_Table_iter = pd.DataFrame(columns=['Iteration','Morpheme','CRE'])
    # A new loop with the size of the numbner of suffix types in Sample 3 starts here
    for item in types_suff_iter:
        # the most important line follows, using regular expressions
        # it finds all the items in the column "construction" (e.g. com-o and com-es include com-)
        # since it is in the loop, it goes item by item (e.g. verb by verb)
        # IMPORTANT: the _ marker has to be added to item, otherwise, when searching for "he" it would also find "sHE" and "tHEy"
        safesearch =  '_' + str(item)
        searchitem = re.compile(r'%s\b' % safesearch)
        CRE_Suf_iter = re.findall(searchitem, str(types_cons_iter))
        # it counts the number of types found (how creatively it was used)
        nCRE_Suf_iter = len(CRE_Suf_iter)
        # it adds them to the dataframe, with the name of the type under "Morpheme" and the creativity under "CRE"
        CRE_Suf_Table_iter.loc[len(CRE_Suf_Table_iter)] = [iteration,item,nCRE_Suf_iter]


    CRE_Suf_Table_iter_Long = pd.concat([CRE_Suf_Table_iter_Long,CRE_Suf_Table_iter], axis=0)


# Iterations ended here
# Now the CRE values are summarised
CRE_Pre_Table_3 = CRE_Pre_Table_iter_Long.groupby(['Morpheme'], as_index=False).mean()
CRE_Suf_Table_3 = CRE_Suf_Table_iter_Long.groupby(['Morpheme'], as_index=False).mean()

#And the new Sample 3 is created, so it can now be compared with either Sample 1 or 2
CRE_Pre_Table_3['Sample'] = 3
CRE_Pre_Table_3['Position'] = 'Prefix'
CRE_Pre_Table_3 = CRE_Pre_Table_3[['Sample', 'Position', 'Morpheme', 'CRE']]

#Compute of the average level of creativity
CRE_Pre_Value_3 = CRE_Pre_Table_3['CRE'].mean()
CRE_Pre_Value_3_sd = CRE_Pre_Table_3['CRE'].std()


CRE_Suf_Table_3['Sample'] = 3
CRE_Suf_Table_3['Position'] = 'Suffix'
CRE_Suf_Table_3 = CRE_Suf_Table_3[['Sample', 'Position', 'Morpheme', 'CRE']]

#Compute of the average level of creativity
CRE_Suf_Value_3 = CRE_Suf_Table_3['CRE'].mean()
CRE_Suf_Value_3_sd = CRE_Suf_Table_3['CRE'].std()


#number of types per file and colum
# Important to consider: prefix_table3 is not directly comparable to prefix_table1 and prefix_table2
# The reason is that the tables computed for samples 1 and 2 are directly created from the list of tokens
# In sample 3,  it is not extracted from a list of tokens but the creativity observed in all iterations
prefix_table3 = CRE_Pre_Table_3["Morpheme"].value_counts()
suffix_table3 = CRE_Suf_Table_3["Morpheme"].value_counts()
ntokens3 = tokendiff

ntypes_prefix3 = len(prefix_table3)
ntypes_suffix3 = len(suffix_table3)






















# =============================================================================
# {05} Analysis of TRI
# =============================================================================

# {05.a} Analysis of TRI before controlling for vocabulary and sample size
# Number of prefixes with only one type in sample 1 before filtering vocabulary and controlling for sample size
count_Tri_Pre_1 = CRE_Pre_Table_1[CRE_Pre_Table_1.CRE == 1].shape[0]
TRI_Pre_1 = count_Tri_Pre_1/ntypes_prefix1
TRI_Pre_1_percent = TRI_Pre_1*100
# Number of suffixes with only one type in sample 1  before filtering vocabulary and controlling for sample size
count_Tri_Suf_1 = CRE_Suf_Table_1[CRE_Suf_Table_1.CRE == 1].shape[0]
TRI_Suf_1 = count_Tri_Suf_1/ntypes_suffix1
TRI_Suf_1_percent = TRI_Suf_1*100
# Number of prefixes with only one type in sample 2  before filtering vocabulary and controlling for sample size
count_Tri_Pre_2 = CRE_Pre_Table_2[CRE_Pre_Table_2.CRE == 1].shape[0]
TRI_Pre_2 = count_Tri_Pre_2/ntypes_prefix2
TRI_Pre_2_percent = TRI_Pre_2*100
# Number of suffixes with only one type in sample 2 before filtering vocabulary and controlling for sample size
count_Tri_Suf_2 = CRE_Suf_Table_2[CRE_Suf_Table_2.CRE == 1].shape[0]
TRI_Suf_2 = count_Tri_Suf_2/ntypes_suffix2
TRI_Suf_2_percent = TRI_Suf_2*100

# {05.b} Analyses after controlling for vocabulary
# Number of prefixes with only one type in sample 1 after filtering vocabulary
count_Tri_Pre_1b = CRE_Pre_FILT_1[CRE_Pre_FILT_1.CRE == 1].shape[0]
TRI_Pre_1b = count_Tri_Pre_1b/len(FILT_types_pref_1)
TRI_Pre_1b_percent = TRI_Pre_1b*100
# Number of suffixes with only one type in sample 1  after filtering vocabulary
count_Tri_Suf_1b = CRE_Suf_FILT_1[CRE_Suf_FILT_1.CRE == 1].shape[0]
TRI_Suf_1b = count_Tri_Suf_1b/len(FILT_types_suff_1)
TRI_Suf_1b_percent = TRI_Suf_1b*100
# Number of prefixes with only one type in sample 2  after filtering vocabulary
count_Tri_Pre_2b = CRE_Pre_FILT_2[CRE_Pre_FILT_2.CRE == 1].shape[0]
TRI_Pre_2b = count_Tri_Pre_2b/len(FILT_types_pref_2)
TRI_Pre_2b_percent = TRI_Pre_2b*100
# Number of suffixes with only one type in sample 2 after filtering vocabulary
count_Tri_Suf_2b = CRE_Suf_FILT_2[CRE_Suf_FILT_2.CRE == 1].shape[0]
TRI_Suf_2b = count_Tri_Suf_2b/len(FILT_types_suff_2)
TRI_Suf_2b_percent = TRI_Suf_2b*100

# {05.c} Analyses after controlling for vocabulary and sample size
# Number of prefixes with only one type in sample 3 after filtering vocabulary and controlling for sample size
count_Tri_Pre_3 = CRE_Pre_Table_3[CRE_Pre_Table_3.CRE == 1].shape[0]
TRI_Pre_3 = count_Tri_Pre_3/ntypes_prefix3
TRI_Pre_3_percent = TRI_Pre_3*100
# Number of suffixes with only one type in sample 3 after filtering vocabulary and controlling for sample size
count_Tri_Suf_3 = CRE_Suf_Table_3[CRE_Suf_Table_3.CRE == 1].shape[0]
TRI_Suf_3 = count_Tri_Suf_3/ntypes_suffix3
TRI_Suf_3_percent = TRI_Suf_3*100

















# =============================================================================
# {6} Histograms for CRE
# =============================================================================

# Histograms for creativity start here

#Plot Prefixes in Sample 1 and 2 side by side
y1pre = np.array(CRE_Pre_FILT_1.CRE)
y2pre = np.array(CRE_Pre_FILT_2.CRE)

y1preVSy2pre = pd.DataFrame(
    dict(value=np.r_[y1pre, y2pre], group=np.r_[["CRE Prefixes Sample 1"] * len(CRE_Pre_FILT_1.CRE), ["CRE Prefixes Sample 2"] * len(CRE_Pre_FILT_2.CRE)])
)
h1 = y1preVSy2pre.hist("value", by="group", figsize=(12,4))


#Now, if there were more tokens in the second sample
#Plot Prefixes in Sample 1 and 3 side by side
if tokendiff > 0:
    y1pre = np.array(CRE_Pre_FILT_1.CRE)
    y3pre = np.array(CRE_Pre_Table_3.CRE)
    histo2 = pd.DataFrame(
        dict(value=np.r_[y1pre, y3pre], group=np.r_[["CRE Prefixes Sample 1"] * len(CRE_Pre_FILT_1.CRE), ["CRE Prefixes Sample 3"] * len(CRE_Pre_Table_3.CRE)])
    )
    histo2.hist("value", by="group", figsize=(12,4))

#Now, if there were more tokens in the first sample
#Plot Prefixes in Sample 1 and 3 side by side
elif tokendiff < 0:
    y1pre = np.array(CRE_Pre_FILT_2.CRE)
    y3pre = np.array(CRE_Pre_Table_3.CRE)
    histo3 = pd.DataFrame(
        dict(value=np.r_[y1pre, y3pre], group=np.r_[["CRE Prefixes Sample 2"] * len(CRE_Pre_FILT_1.CRE), ["CRE Prefixes Sample 3"] * len(CRE_Pre_Table_3.CRE)])
    )
    histo3.hist("value", by="group", figsize=(12,4))

#Plot Suffixes in Sample 1 and 2 side by side
y1suf = np.array(CRE_Suf_FILT_1.CRE)
y2suf = np.array(CRE_Suf_FILT_2.CRE)

histo1 = pd.DataFrame(
    dict(value=np.r_[y1suf, y2suf], group=np.r_[["CRE Suffixes Sample 1"] * len(CRE_Suf_FILT_1.CRE), ["CRE Suffixes Sample 2"] * len(CRE_Suf_FILT_2.CRE)])
)
histo1.hist("value", by="group", figsize=(12,4))

#Now, if there were more tokens in the second sample
#Plot Suffixes in Sample 1 and 3 side by side
if tokendiff > 0:
    y1suf = np.array(CRE_Suf_FILT_1.CRE)
    y3suf = np.array(CRE_Suf_Table_3.CRE)

    histo2 = pd.DataFrame(
        dict(value=np.r_[y1suf, y3suf], group=np.r_[["CRE Suffixes Sample 1"] * len(CRE_Suf_FILT_1.CRE), ["CRE Suffixes Sample 3"] * len(CRE_Suf_Table_3.CRE)])
    )
    histo2.hist("value", by="group", figsize=(12,4))

#Now, if there were more tokens in the first sample
#Plot Suffixes in Sample 1 and 3 side by side
elif tokendiff < 0:
    y2suf = np.array(CRE_Suf_FILT_2.CRE)
    y3suf = np.array(CRE_Suf_Table_3.CRE)

    histo3 = pd.DataFrame(
        dict(value=np.r_[y2suf, y3suf], group=np.r_[["CRE Suffixes Sample 2"] * len(CRE_Suf_FILT_2.CRE), ["CRE Suffixes Sample 3"] * len(CRE_Suf_Table_3.CRE)])
    )
    histo3.hist("value", by="group", figsize=(12,4))















# =============================================================================
# {7} Feedback files
# =============================================================================




#Main results table with the values of CRE and TRI and sample sizes, equivalent to Table 3 from Aguado-Orea & Pine (2015)
ResultsTable = pd.DataFrame(columns=['Control','Sample','Analysis','CRE','sd','Tokens','Types','TRI', 'TRI%'])
Row1 = ['None',1,'Prefix/Suffix',CRE_Pre_Value_1,CRE_Pre_Value_1_sd,ntokens1,ntypes_suffix1,TRI_Pre_1,TRI_Pre_1_percent]
ResultsTable.loc[len(ResultsTable)] = Row1
Row2 = ['None',1,'Suffix/Prefix',CRE_Suf_Value_1,CRE_Suf_Value_1_sd,ntokens1,ntypes_prefix1,TRI_Suf_1,TRI_Suf_1_percent]
ResultsTable.loc[len(ResultsTable)] = Row2
Row3 = ['None',2,'Prefix/Suffix',CRE_Pre_Value_2,CRE_Pre_Value_2_sd,ntokens2,ntypes_suffix2,TRI_Pre_2,TRI_Pre_2_percent]
ResultsTable.loc[len(ResultsTable)] = Row3
Row4 = ['None',2,'Suffix/Prefix',CRE_Suf_Value_2,CRE_Suf_Value_2_sd,ntokens2,ntypes_prefix2,TRI_Suf_2,TRI_Suf_2_percent]
ResultsTable.loc[len(ResultsTable)] = Row4
Row5 = ['Lexical',1,'Prefix/Suffix',CRE_Pre_FILT_Value_1,CRE_Pre_FILT_Value_1_sd,ntokens1f,nShared_Prefix_Types,TRI_Pre_1b,TRI_Pre_1b_percent]
ResultsTable.loc[len(ResultsTable)] = Row5
Row6 = ['Lexical',1,'Suffix/Prefix',CRE_Suf_FILT_Value_1,CRE_Suf_FILT_Value_1_sd,ntokens1f,nShared_Prefix_Types,TRI_Suf_1b,TRI_Suf_1b_percent]
ResultsTable.loc[len(ResultsTable)] = Row6
Row7 = ['Lexical',2,'Prefix/Suffix',CRE_Pre_FILT_Value_2,CRE_Pre_FILT_Value_2_sd,ntokens2f,nShared_Suffix_Types,TRI_Pre_2b,TRI_Pre_2b_percent]
ResultsTable.loc[len(ResultsTable)] = Row7
Row8 = ['Lexical',2,'Suffix/Prefix',CRE_Suf_FILT_Value_2,CRE_Suf_FILT_Value_2_sd,ntokens2f,nShared_Suffix_Types,TRI_Suf_2b,TRI_Suf_2b_percent]
ResultsTable.loc[len(ResultsTable)] = Row8
Row9 = ['Both',1,'Prefix/Suffix',CRE_Pre_Value_3,CRE_Pre_Value_3_sd,ntokens1,ntypes_suffix3,TRI_Pre_3,TRI_Pre_3_percent]
ResultsTable.loc[len(ResultsTable)] = Row9
Row10 = ['Both',1,'Suffix/Prefix',CRE_Suf_Value_3,CRE_Suf_Value_3_sd,ntokens1,ntypes_prefix3,TRI_Suf_3,TRI_Suf_3_percent]
ResultsTable.loc[len(ResultsTable)] = Row10





#A couple of lines to ask for the first filename to read

msg_sep = "—————————————————————————————————————————————————————————————————————————————————————————————————————" + "\r\n"

msg_intro_01 = "Sample 1 is "+txtfile1 + "\r\n"
msg_intro_02 = "Sample 2 is "+txtfile2 + "\r\n"
msg_intro_03 = 'Number of tokens in FIRST text file :' + str(ntokens1) + "\r\n"
msg_intro_04 = 'Number of tokens in SECOND text file :' + str(ntokens2) + "\r\n"
msg_intro_05= '[A] Number of prefix types in FIRST text file :' + str(ntypes_prefix1) + "\r\n"
msg_intro_06= '[B] Number of prefix types in SECOND text file :' + str(ntypes_prefix2) + "\r\n"
msg_intro_07= '[C] Number of suffix types in FIRST text file :' + str(ntypes_suffix1) + "\r\n"
msg_intro_08= '[D] Number of suffix types in SECOND text file :' + str(ntypes_suffix2) + "\r\n"

msg_intro_10= 'Shared prefixes between samples 1 and 2: ' + "\r\n" + str(Shared_Prefix_Types_sorted) + "\r\n"
msg_intro_11= 'Shared sufffixes between samples 1 and 2: '  + "\r\n" + str(Shared_Suffix_Types_sorted) + "\r\n"

msg_intro_12 = "After filtering Sample 1 with the lexical items of Sample 2, the number of tokens of Sample 1 is now " + str(ntokens1f) + "\r\n"
msg_intro_13 = "After filtering Sample 2 with the lexical items of Sample 1, the number of tokens of Sample 2 is now " + str(ntokens2f) + "\r\n"
msg_intro_14 = 'Number of tokens in sample extracted from ' + msgtkn2 + ': ' + msgtkn3 + "\r\n"

msg_intro_15= '[E] Number of prefix types in sample extracted from ' + msgtkn2 + ': ' + str(ntypes_prefix3) + "\r\n"
msg_intro_16= '[F] Number of suffix types in sample extracted from ' + msgtkn2 + ': ' + str(ntypes_suffix3) + "\r\n"

msg_intro = msg_sep + msg_intro_01 + msg_intro_02 + msg_intro_03 + msg_intro_04 + msg_intro_05 + msg_intro_06 + msg_intro_07 + msg_intro_08 + msg_intro_10 + msg_intro_11 + msg_intro_12 + msg_intro_13 + msg_intro_14 + msg_intro_15 + msg_intro_16 + msg_sep + "\r\n" + "\r\n" 


msg_TRI_01= 'These are the values of Triteness [TRI] before controlling for anything:'
msg_TRI_02='(1a) TRI Prefixes in Sample 1= ' + str(TRI_Pre_1) + "\r\n"
msg_TRI_03='     Number of Prefixes in Sample 1 used with just one Suffix = ' + str(count_Tri_Pre_1) + ' out of ' + str(ntypes_prefix1) + "\r\n"
msg_TRI_04='     Percentage of Prefixes in Sample 1 used with just one Suffix = ' + str("{:.2f}".format(TRI_Pre_1_percent)) + "\r\n"
msg_TRI_05='(1b) TRI Suffixes in Sample 1= ' + str(TRI_Suf_1) + "\r\n"
msg_TRI_06='     Number of Suffixes in Sample 1 used with just one Prefix = ' + str(count_Tri_Suf_1) + ' out of ' + str(ntypes_suffix1) + "\r\n"
msg_TRI_07='     Percentage of Suffixes in Sample 1 used with just one Prefix = ' + str("{:.2f}".format(TRI_Suf_1_percent)) + "\r\n"
msg_TRI_08='(2a) TRI Prefixes in Sample 2= ' + str(TRI_Pre_2) + "\r\n"
msg_TRI_09='     Number of Prefixes in Sample 2 used with just one Suffix = ' + str(count_Tri_Pre_2) + ' out of ' + str(ntypes_prefix2) + "\r\n"
msg_TRI_10='     Percentage of Prefixes in Sample 2 used with just one Suffix = ' + str("{:.2f}".format(TRI_Pre_2_percent)) + "\r\n"
msg_TRI_11='(2b) TRI Suffixes in Sample 2= ' + str(TRI_Suf_2) + "\r\n"
msg_TRI_12='     Number of Suffixes in Sample 2 used with just one Prefix = ' + str(count_Tri_Suf_2) + ' out of ' + str(ntypes_suffix2) + "\r\n"
msg_TRI_13='     Percentage of Suffixes in Sample 2 used with just one Prefix = ' + str("{:.2f}".format(TRI_Suf_2_percent)) + "\r\n"
msg_TRI_14= 'These are the values of Triteness [TRI] after controlling for vocabulary:' + "\r\n"
msg_TRI_15='(1a) TRI Prefixes in Sample 1= ' + str(TRI_Pre_1b) + "\r\n"
msg_TRI_16='     Number of Prefixes in Sample 1 used with just one Suffix = ' + str(count_Tri_Pre_1b) + ' out of ' + str(len(FILT_types_pref_1)) + "\r\n"
msg_TRI_17='     Percentage of Prefixes in Sample 1 used with just one Suffix = ' + str("{:.2f}".format(TRI_Pre_1b_percent)) + "\r\n"
msg_TRI_18='(1b) TRI Suffixes in Sample 1= ' + str(TRI_Suf_1b) + "\r\n"
msg_TRI_19='     Number of Suffixes in Sample 1 used with just one Prefix = ' + str(count_Tri_Suf_1b) + ' out of ' + str(len(FILT_types_suff_1)) + "\r\n"
msg_TRI_20='     Percentage of Suffixes in Sample 1 used with just one Prefix = ' + str("{:.2f}".format(TRI_Suf_1b_percent)) + "\r\n"
msg_TRI_21='(2a) TRI Prefixes in Sample 2= ' + str(TRI_Pre_2b) + "\r\n"
msg_TRI_22='     Number of Prefixes in Sample 1 used with just one Suffix = ' + str(count_Tri_Pre_2b) + ' out of ' + str(len(FILT_types_pref_2)) + "\r\n"
msg_TRI_23='     Percentage of Prefixes in Sample 2 used with just one Suffix = ' + str("{:.2f}".format(TRI_Pre_2b_percent)) + "\r\n"
msg_TRI_24='(2b) TRI Suffixes in Sample 2= ' + str(TRI_Suf_2b) + "\r\n"
msg_TRI_25='     Number of Suffixes in Sample 2 used with just one Prefix = ' + str(count_Tri_Suf_2b) + ' out of ' + str(len(FILT_types_suff_2)) + "\r\n"
msg_TRI_26='     Percentage of Suffixes in Sample 2 used with just one Prefix = ' + str("{:.2f}".format(TRI_Suf_2b_percent)) + "\r\n"
msg_TRI_27= 'These are the values of Triteness [TRI] after controlling for vocabulary:' + "\r\n"
msg_TRI_28= 'These are the values of Triteness [TRI] after controlling for vocabulary and sample size:' + "\r\n"
msg_TRI_29='(3a) TRI Prefixes in Sample 3= ' + str(TRI_Pre_3) + "\r\n"
msg_TRI_30='     Number of Prefixes in Sample 3 used with just one Suffix = ' + str(count_Tri_Pre_3) + ' out of ' + str(ntypes_prefix3) + "\r\n"
msg_TRI_31='     Percentage of Prefixes in Sample 3 used with just one Suffix = ' + str("{:.2f}".format(TRI_Pre_3_percent)) + "\r\n"
msg_TRI_32='(3b) TRI Suffixes in Sample 3= ' + str(TRI_Suf_3) + "\r\n"
msg_TRI_33='     Number of Suffixes in Sample 3 used with just one Prefix = ' + str(count_Tri_Suf_3) + ' out of ' + str(ntypes_suffix3) + "\r\n"
msg_TRI_34='     Percentage of Suffixes in Sample 3 used with just one Prefix = ' + str("{:.2f}".format(TRI_Suf_3_percent)) + "\r\n"

msg_TRI = msg_sep + msg_TRI_01 + msg_TRI_02 + msg_TRI_03 + msg_TRI_04 + msg_TRI_05 + msg_TRI_06 + msg_TRI_07 + msg_TRI_08 + msg_TRI_10 + msg_TRI_11 + msg_TRI_12 + msg_TRI_13 + msg_TRI_14 + msg_TRI_15 + msg_TRI_16 + msg_TRI_17 + msg_TRI_18 + msg_TRI_19 + msg_TRI_20 + msg_TRI_21 + msg_TRI_22 + msg_TRI_23 + msg_TRI_24 + msg_TRI_25 + msg_TRI_26 + msg_TRI_27 + msg_TRI_28 + msg_TRI_29 + msg_TRI_30 + msg_TRI_31 + msg_TRI_32 + msg_TRI_33 + msg_TRI_34 + msg_sep + "\r\n" + "\r\n" 


msg_CRE_01= 'These are the values of Creativity [CRE] before controlling for anything:' + "\r\n"
msg_CRE_02='(1a) CRE Prefixes in Sample 1= ' + str(CRE_Pre_Value_1) + "\r\n"
msg_CRE_03='(1b) CRE Suffixes in Sample 1= ' + str(CRE_Suf_Value_1) + "\r\n"
msg_CRE_04='(2a) CRE Prefixes in Sample 2= ' + str(CRE_Pre_Value_2) + "\r\n"
msg_CRE_05='(2b) CRE Suffixes in Sample 2= ' + str(CRE_Suf_Value_2) + "\r\n"
msg_CRE_06= 'These are the values of Creativity [CRE] after controlling for vocabulary:' + "\r\n"
msg_CRE_07='(1a) CRE Prefixes in Sample 1= ' + str(CRE_Pre_FILT_Value_1) + "\r\n"
msg_CRE_08='(1b) CRE Suffixes in Sample 1= ' + str(CRE_Suf_FILT_Value_1) + "\r\n"
msg_CRE_09='(2a) CRE Prefixes in Sample 2= ' + str(CRE_Pre_FILT_Value_2) + "\r\n"
msg_CRE_10='(2b) CRE Suffixes in Sample 2= ' + str(CRE_Suf_FILT_Value_2) + "\r\n"
msg_CRE_11= 'These are the values of Creativity [CRE] after controlling for sample size and vocabulary:' + "\r\n"
msg_CRE_12='(3a) CRE Prefixes in Sample 3= ' + str(CRE_Pre_Value_3) + "\r\n"
msg_CRE_13='(3b) CRE Suffixes in Sample 3= ' + str(CRE_Suf_Value_3) + "\r\n"

msg_CRE = msg_sep + msg_CRE_01 + msg_CRE_02 + msg_CRE_03 + msg_CRE_04 + msg_CRE_05 + msg_CRE_06 + msg_CRE_07 + msg_CRE_08 +  msg_CRE_09 + msg_CRE_10 + msg_CRE_11 + msg_CRE_12 + msg_CRE_13 + msg_sep + "\r\n" + "\r\n" 

msg_OUT_01= "The sample use in the last iteration is included in the output directory as a text file in the format [name_of_sample1]_sample.txt" + "\r\n"
msg_OUT_02= "The file results_creativity.csv includes the data required for runing BEST." + "\r\n"
msg_OUT_03= "The wholse set of data generated during the randon sampling is included in two more files: one for preffixes (iterations_Prefixes.csv), and one for suffixes (iterations_Suffixes.csv)." + "\r\n"
msg_OUT_04= "A file with the summary of results (summary_table.csv) has also been created." + "\r\n"

msg_OUT = msg_sep + msg_OUT_01 + msg_OUT_02 + msg_OUT_03 + msg_OUT_04

# =============================================================================
# Appendices: List of types and Creativity values
# =============================================================================

msg_APPEND_01 = 'List of prefix types in the FIRST file with values of CRE: ' + "\r\n" + str(CRE_Pre_Table_1) + "\r\n"
msg_APPEND_02 = 'List of suffix types in the FIRST file with values of CRE: ' + "\r\n" + str(CRE_Suf_Table_1) + "\r\n"
msg_APPEND_03 = 'List of prefix types in the SECOND file with values of CRE: ' + "\r\n" + str(CRE_Pre_Table_2) + "\r\n"
msg_APPEND_04 = 'List of suffix types in the SECOND file with values of CRE: ' + "\r\n" + str(CRE_Suf_Table_2) + "\r\n"
msg_APPEND_05 = 'List of prefix types in the SET OF RANDOM SAMPLES with MEAN values of CRE: ' + "\r\n" + str(CRE_Pre_Table_3) + "\r\n"
msg_APPEND_06 = 'List of suffix types in the SET OF RANDOM SAMPLES with MEAN values of CRE: ' + "\r\n" + str(CRE_Suf_Table_3) + "\r\n"

msg_APPEND = "\r\n" + msg_sep + msg_APPEND_01 + "\r\n" + msg_sep + "\r\n" + msg_APPEND_02 + "\r\n" + msg_sep + "\r\n"  + msg_APPEND_03 + "\r\n" + msg_sep + "\r\n"  + msg_APPEND_04 + "\r\n" + msg_sep + "\r\n"  + msg_APPEND_05 + "\r\n" + msg_sep + "\r\n"  + msg_APPEND_06 + "\r\n" + msg_sep + "\r\n" 


results_msg = msg_intro + msg_TRI + msg_CRE + msg_APPEND
with open('feedback_file.txt', 'w') as f:
    f.write(results_msg)



Creativity = pd.concat([CRE_Pre_Table_1,CRE_Suf_Table_1,CRE_Pre_Table_2,CRE_Suf_Table_2,CRE_Pre_Table_3,CRE_Suf_Table_3], axis=0)
Creativity.to_csv('results_creativity.csv', header=True, index=False)
CRE_Pre_Table_iter_Long.to_csv('iterations_Prefixes.csv', header=True, index=False)
CRE_Suf_Table_iter_Long.to_csv('iterations_Suffixes.csv', header=True, index=False)
ResultsTable.to_csv('summary_table.csv')



print('End of code reached.')


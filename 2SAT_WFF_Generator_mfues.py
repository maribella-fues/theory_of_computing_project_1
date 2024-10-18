#!/usr/bin/env python3

# Acknowledgements: This code was edited from the original DumbSAT.py code file provided by Professor Kogge!

import random

def build_wff(Nvars,Nclauses,LitsPerClause):
    '''
    Return randomly-generated wff according to the number of variables, clauses, and literals per clause (always 2)
    '''
    wff=[]
    # iterate for number of clauses
    for i in range(1,Nclauses+1):
        clause=[]
        # randomly generate two literals per clause
        for j in range(1,LitsPerClause+1):
            var=random.randint(1,Nvars)
            if random.randint(0,1)==0: var=-var
            clause.append(var)
        # append new clause to wff
        wff.append(clause)
    # return new wff
    return wff

def generate_cases(TestCases):
    '''
    Write the randomly generated 2 literal wffs to a data file to be used as input for the 2SAT Solver
    '''
    # open new data file to write to
    f1=open("data_generated_2SAT_mfues.csv", 'w')
    # iterate through each test case
    for i in range(0,len(TestCases)):
        TestCase=TestCases[i]
        Nvars=TestCase[0] # get number of variables in the wff
        NClauses=TestCase[1] # get number of clauses in the wff
        LitsPerClause=TestCase[2] # get number of literals in each clause (always 2)
        Ntrials=TestCase[3] # get number of trials for this type of wff
        # iterate for number of trials
        for j in range(0,Ntrials):
            # generate new wff
            wff = build_wff(Nvars,NClauses,LitsPerClause)
            # write wff as a new line in the data file
            z = str(Nvars)+','+str(NClauses) + ',[' + str(wff[0])
            for clause in wff[1:]:
                z=z+','+str(clause)
            f1.write(z+']\n')
    # close the data file
    f1.close()

# Following generates several hundred test cases of 10 different wffs at each size
# and from 4 to 22 variables, 10 to 240 clauses, and 2 literals per clause 
SAT2=[
    [4,9,2,10],
    [8,18,2,10],
    [12,20,2,10],
    [16,30,2,10],
    [18,32,2,10],
    [20,33,2,10],
    [22,38,2,10],
    [24,43,2,10],
    [26,45,2,10],
    [28,47,2,10],
    [30,49,2,10],
    [32,51,2,10],
    [34,53,2,10],
    [36,55,2,10],
    [38,57,2,10],
    [40,59,2,10],
    [42,61,2,10],
    [44,63,2,10],
    [46,65,2,10],
    [48,67,2,10],
    [50,69,2,10],
    [52,71,2,10],
    [54,73,2,10],
    [56,75,2,10],
    [58,77,2,10],
    [60,79,2,10],
    [62,82,2,10],
    [64,83,2,10],
    [66,85,2,10],
    [68,87,2,2],
    [70,89,2,2],
    [72,91,2,2],
    [74,93,2,2],
    [76,95,2,2],
    [78,97,2,2],
    [80,99,2,2],
    [82,101,2,2],
    [84,103,2,2],
    [86,105,2,2],
    [88,107,2,2],
    [90,109,2,2]
    ]


generate_cases(SAT2)

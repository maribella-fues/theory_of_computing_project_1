#!/usr/bin/env python3
# Acknowledgements: This is an altered version of Professor Kogge's DumbSAT.py
# All logic and functions are his, changes were just made to generate output to check the 2SAT Solver against


#                    Brute Force SAT
# This file generates a set of random wffs and tests each for satisfiability.
#   The test returns "Satisfiable" or not, and the time it took to determine that.
# A wff is expressed as a list of lists where each internal list is a clause.
#    and each integer within a clause list is a literal
#    A positive integer such as "3" means that clause is true if variable 3 is true
#    A negative integer such as "-3" means that clause is true if variable 3 is false
#  A clause is satisfiable if at least one literal is true
#  A wff is satisfiable if all clauses are satisfiable
# An assignment to n variables is a list of n 0s or 1s (0=>False, 1=>True)
#    where assignment[i] is value for variable i+1 (there is no variable 0)
#
# build_wff builds a random wff with specified # of clauses, variables,
#   and literals/clause
# check takes a wff, generates all possible assignments,
#   and determines if any assignment satisfies it.
#   If so it stops and returns the time ans assignment
# test_wff builds a random wff with certain structure
#
# run_cases takes a list of 4-tuples and for each one generates a number of wffs
#    with the same specified characteristices, and test each one.
#    It outputs to a file (in current directory) each wff in cnf format,
#    and also for each case it dumps a row to a .csv file that contains
#       the test conditions and the satisfying assignment if it exists

import time
import random

def check(Wff,Nvars,Nclauses,Assignment):
# Run thru all possibilities for assignments to wff
# Starting at a given Assignment (typically array of Nvars+1 0's)
# At each iteration the assignment is "incremented" to next possible
# At the 2^Nvars+1'st iteration, stop - tried all assignments
    Satisfiable=False
    while (Assignment[Nvars+1]==0):
        # Iterate thru clauses, quit if not satisfiable
        for i in range(0,Nclauses): #Check i'th clause
            Clause=Wff[i]
            Satisfiable=False
            for j in range(0,len(Clause)): # check each literal
                Literal=Clause[j]
                if Literal>0: Lit=1
                else: Lit=0
                VarValue=Assignment[abs(Literal)] # look up literal's value
                if Lit==VarValue:
                    Satisfiable=True
                    break
            if Satisfiable==False: break
        if Satisfiable==True: break # exit if found a satisfying assignment
        # Last try did not satisfy; generate next assignment)
        for i in range(1,Nvars+2):
            if Assignment[i]==0:
                Assignment[i]=1
                break
            else: Assignment[i]=0
    return Satisfiable
    
def build_wff(Nvars,Nclauses,LitsPerClause):
    wff=[]
    for i in range(1,Nclauses+1):
        clause=[]
        for j in range(1,LitsPerClause+1):
            var=random.randint(1,Nvars)
            if random.randint(0,1)==0: var=-var
            clause.append(var)
        wff.append(clause)
    return wff

def test_wff(wff,Nvars,Nclauses):
    Assignment=list((0 for x in range(Nvars+2)))
    start = time.time() # Start timer
    SatFlag=check(wff,Nvars,Nclauses,Assignment)
    end = time.time() # End timer
    exec_time=int((end-start)*1e6)
    return [wff,Assignment,SatFlag,exec_time]

def run_cases(TestCases,ProbNum,resultsfile,tracefile):
    # TestCases: list of 4tuples describing problem
    #   0: Nvars = number of variables
    #   1: NClauses = number of clauses
    #   2: LitsPerClause = Literals per clause
    #   3: Ntrials = number of trials
    # ProbNum: Starting nunber to be given to 1st output run
    # resultsfile: path to file to hold output
    # tracefile: path to file to hold output
    # cnffile: path to file to hold output
    # For each randomly built wff, print out the following list
    #   Problem Number
    #   Number of variables
    #   Number of clauses
    #   Literals per clause
    #   Result: S or U for satisfiable or unsatisfiable
    #   A "1"
    #   Execution time
    #   If satisfiable, a binary string of assignments
# Each case = Nvars,NClauses,LitsPerClause,Ntrials
    f1=open(resultsfile+".csv",'w')
    f2=open(tracefile+".csv",'w')
    #initialize counters for final line of output
    Nwffs=0
    Nsat=0
    Nunsat=0
#    f1.write('ProbNum,Nvars,NClauses,LitsPerClause,Result,ExecTime(us)\n')
    for i in range(0,len(TestCases)):
        TestCase=TestCases[i]
        Nvars=TestCase[0]
        NClauses=TestCase[1]
        LitsPerClause=TestCase[2]
        Ntrials=TestCase[3]
        #Now run the number of trials for this wff configuration
        Scount=Ucount=0
        AveStime=AveUtime=0
        MaxStime=MaxUtime=0
        for j in range(0,Ntrials):
            #generate next trial case for this configuration
            Nwffs=Nwffs+1
            random.seed(ProbNum)
            wff = build_wff(Nvars,NClauses,LitsPerClause)
            results=test_wff(wff,Nvars,NClauses)
            wff=results[0]
            Assignment=results[1]
            Exec_Time=results[3]
            if results[2]:
                y='S'
                Scount=Scount+1
                AveStime=AveStime+Exec_Time
                MaxStime=max(MaxStime,Exec_Time)
                Nsat=Nsat+1
            else:
                y='U'
                Ucount=Ucount+1
                AveUtime=AveUtime+Exec_Time
                MaxUtime=max(MaxUtime,Exec_Time)
                Nunsat=Nunsat+1
            x=str(ProbNum)+','+str(Nvars)+','+str(NClauses)+','+str(LitsPerClause)
            x=x+str(NClauses*LitsPerClause)+','+y+',1,'+str(Exec_Time)
            if results[2]:
                for k in range(1,Nvars+1):
                    x=x+','+str(Assignment[k])
                    y=y+','+str(Assignment[k])
            print(x)
            f1.write(y+'\n')
            f2.write(x+'\n')
            #Increment problem number for next iteration
            ProbNum=ProbNum+1
        counts='# Satisfied = '+str(Scount)+'. # Unsatisfied = '+str(Ucount)
        maxs='Max Sat Time = '+str(MaxStime)+'. Max Unsat Time = '+str(MaxUtime)
        aves='Ave Sat Time = '+str(AveStime/Ntrials)+'. Ave UnSat Time = '+str(AveUtime/Ntrials)
        print(counts)
        print(maxs)
        print(aves)
        f2.write(counts+'\n')
        f2.write(maxs+'\n')
        f2.write(aves+'\n')
    f1.write(x)
    f1.close()
    f2.close()

# Following generates several hundred test cases of 10 different wffs at each size
# and from 4 to 22 variables, 10 to 240 clauses, and 2 to 10 literals per clause 
# Following generates a bunch of 2 literal wffs
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
    [28,47,2,10]
    ]

trace=True
ProbNum = 3
resultsfile = r'check_2SAT_output_mfues'
tracefile = r'check_DumbSAT_2SAT_trace_mfues'

run_cases(SAT2,ProbNum,resultsfile,tracefile)
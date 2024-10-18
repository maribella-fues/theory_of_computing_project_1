#!/usr/bin/env python3

import time
import copy
import matplotlib.pyplot as plt

def set_assignment(lit, assignments):
    '''
    Sets a literal's assignment depending on its polarity.
    '''
    if lit > 0:
        # if the literal is positive, assign its value to 1
        assignments[abs(lit)-1] = [1,1] 
    else:
        # if the literal is negative, assign its value to 0
        assignments[abs(lit)-1] = [0,1] 

def unit_propagate(lit, wff, nclauses, assignments):
    '''
    Returns an altered wff and assignment lists.
    Deletes any clauses that contain the literal in the unit clause.
    These clauses are now True and don't need to be tested anymore to determine assignments.
    '''
    i = 0
    # if found unit clause, set assignment
    set_assignment(lit, assignments)
    # iterate through all the clauses
    while i < nclauses:
        # if the literal is in a clause, remove the entire clause because one literal is now definitely true
        if lit in wff[i]:
            wff.pop(i)
            nclauses -= 1
        # if the negation of the literal is in the clause, remove that literal because it can never be true
        elif -lit in wff[i]:
            while -lit in wff[i]:
                wff[i].remove(-lit)
            i += 1
        else:
            i += 1
    # return the altered wff and new assignments
    return wff, assignments

def pure_literal(lit, wff):
    '''
    Returns True if the literal has only one polarity in the wff, which would make it pure.
    Returns False if its negation is present, making it not pure.
    '''
    found = False # set a found flag first to false
    # iterate through every clause in the wff
    for clause in wff:
        # if the literal is in the clause, set the flag to true
        if lit in clause:
            found = True
        # if the negation of the literal is in the clause, return false because it is not pure in all clauses
        if -lit in clause:
            return False
    # return whether the pure literal was found or not
    return found
    
def remove_pure_literal(lit, wff, nclauses, assignments):
    '''
    If a literal occurs with only one polarity in the wff, it is called pure. 
    A pure literal can always be assigned in a way that makes all clauses containing it true. 
    Thus, when it is assigned in such a way, these clauses can be deleted because they do not need to be tested anymore.
    This function deletes any clauses containing a pure literal.
    It returns the altered wff and assignment lists.
    '''
    i = 0
    # if found pure literal, set assignment
    set_assignment(lit, assignments)
    # iterate through all the clauses
    while i < nclauses:
        # if the pure literal is in the clause, remove the entire clause because the one literal makes the entire clause true
        if lit in wff[i]:
            wff.pop(i)
            nclauses -= 1
        else: i += 1
    # return the altered wff and new assignments
    return wff, assignments

def backtrack(wff, nvars, assignments):
    '''
    Recursively tests different assignments to determine if the wff is Satisfiable.
    If it determines that the wff is Satisfiable, the function returns True and the assignment list.
    If the wff is Unsatisfiable, the function returns False and an empty list.
    '''
    # the wff is empty if all clauses are satisfied
    if not wff: 
        return True, assignments
    # if an empty clause exists, the wff is unsatisfiable
    if [] in wff: 
        return False, []

    # iterate through all the variables to try to find an unassigned variable
    for var in range(1, nvars + 1):
        if assignments[var-1][1] == 0: break # break loop if the variable is unassigned
    else: return True, assignments  # if no unassigned variables are found, the wff has been satisfied

    # first try assigning True to the variable
    assignments[var-1] = [1, 1]
    # alter the wff using unit_propagate under the assumption that the variable is True
    new_wff, new_assignments = unit_propagate(var, copy.deepcopy(wff), len(wff), copy.deepcopy(assignments))
    
    # recursively check if this assignment leads to a solution
    satisfiable, final_assignments = backtrack(new_wff, nvars, new_assignments)
    if satisfiable:
        return True, final_assignments
    
    # if assigning True failed, try assigning False
    assignments[var-1] = [0, 1]
    # alter the wff using unit_propagate under the assumption that the variable is False 
    new_wff, new_assignments = unit_propagate(-var, copy.deepcopy(wff), len(wff), copy.deepcopy(assignments))
    
    # recursively check if this assignment leads to a solution
    return backtrack(new_wff, nvars, new_assignments) 

def findUnitClause(wff):
    '''
    Returns True if a unit clause exists in the wff.
    Returns False if all clauses contain more than 1 literal.
    '''
    # sort the wff by length
    wff = sorted(wff, key=lambda x: len(x))
    # check if a unit clause (length of 1) exists in the wff
    if len(wff[0]) == 1:
        return True
    return False

def DPLL(wff, nvars, nclauses):
    '''
    Implements many methods to solve 2-SAT problems in the most efficient manner possible.
    These methods include Unit Propagation, Pure Literal Elimination, and Backtracking.
    The function determines if the wff is Satisfiable, and if so, generates a list of assignments for the literals.
    If it determines that the wff is Satisfiable, the function returns True and the assignment list.
    If the wff is Unsatisfiable, the function returns False and an empty list.
    '''
    # create list of assignments for each variable
    assignments = [[0,0]]*(nvars+1) # first element is value, second is whether it has been assigned yet

    # iterate while a unit clause exists in the wff
    while findUnitClause(wff):
        # iterate through all the variables
        for lit in range(1, nvars+1):
            # if the variable exists as a unit clause, it must be True so call unit_propagate to alter rest of wff
            if [lit] in wff:
                wff, assignments = unit_propagate(lit, wff, nclauses, assignments)
            # if the negation of the variable exists as unit clause, it must be False so call unit_propagate to alter rest of wff 
            elif[-lit] in wff:
                wff, assignments = unit_propagate(-lit, wff, nclauses, assignments)
            # unit_propagate alters the wff list so must recheck number of clauses
            nclauses = len(wff)

    changed = True 
    while changed:
        changed = False # flag to break out of loop early if nothing has been changed
        # iterate through all the variables
        for lit in range(1, nvars+1): 
            # check if the variable exists as a pure literal
            # if so, it must be True so remove all clauses containing it because they are now True
            if pure_literal(lit, wff): 
                wff, assignments = remove_pure_literal(lit, wff, nclauses, assignments)
                changed = True
            # check if the negation of the variable exists as a pure literal
            # if so, it must be False so remove all clauses containing it because they are now True
            elif pure_literal(-lit, wff):
                wff, assignments = remove_pure_literal(-lit, wff, nclauses, assignments)
                changed = True
            nclauses = len(wff)
        # the wff is empty if all clauses are satisfied
        if not wff:
            return True, assignments
        # if an empty clause exists, the wff is unsatisfiable 
        if [] in wff:
            return False, []
    # finish solving the wff using backtracking
    return backtrack(wff, nvars, assignments)

def test_wff(wff,Nvars,Nclauses):
    '''
    Calculates the total time taken to solve the 2-SAT using the DPLL method.
    Returns the wff, assignment list, if the wff is Satisfiable or not, and total execution time.
    '''
    start = time.time() # start timer
    newwff = copy.deepcopy(wff)
    SatFlag, assignment = DPLL(newwff, Nvars, Nclauses) # solve the wff
    end = time.time() # end timer
    exec_time=int((end-start)*1e6) # get total time passed in microseconds
    return [wff, assignment,SatFlag,exec_time]

def convert_to_int(data):
    '''
    Recursively converts all the literals in the input from strings to integers to be used to solve the wff.
    '''
    if isinstance(data, list):  # If it's a list, recursively process each element
        return [convert_to_int(item) for item in data]
    else:  # Convert the element to int if it's not a list
        return int(data)

def build_wff(file_name):
    """
    Parses the input file to extract WFFs.
    Each line is a new WFF, each clause in the WFF is separated by commas, 
    and each clause is a list of two literals.
    Each line is structured as: Numvars, Numclauses,[[clause1],[clause2],...]
    Returns three lists: one to hold number of variables of each wff, one to hold number of clauses of each wff, and one to hold each wff
    """
    wffs = []
    nvarlist = []
    nclauselist = []
    # open the input file
    with open(file_name, mode ='r')as file:
        # for each line in the file, extract the number of variables, number of clauses, and the wff
        # append each to its respective list so that indexes of are the same
        for line in file:
            line = line.rstrip()
            line = line.split(",", 2)
            nvar = int(line[0])
            nclause = int(line[1])
            # convert the string to a list of lists
            wff = eval(line[2].strip())
            # convert all the literals in the wff to integers and append to list of wffs
            wffs.append(convert_to_int(wff))
            nvarlist.append(nvar)
            nclauselist.append(nclause)
    return nvarlist, nclauselist, wffs

def generate_scatter_plot(file_name):
    """
    Processes the list of WFFs, runs the test_wff function, and generates a scatter plot.
    """
    nvarlist, nclauselist, wffs = build_wff(file_name)

    variables = []
    times = []
    colors = []
    
    # iterate through each wff
    for i in range(len(wffs)):
        Nvars = nvarlist[i]  # number of variables in the wff
        Nclauses = nclauselist[i] # number of clauses in the wff
        wff = wffs[i] # the wff itslef
        
        # test the WFF and collect data
        result = test_wff(wff, Nvars, Nclauses)
        # append data to lists used for graphing
        variables.append(Nvars)
        times.append(result[3])
        if result[2]: colors.append('green')
        else: colors.append('red')
        

    # generate scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(variables, times, c=colors, s=50)

    # add labels and title
    plt.title('2-SAT Solver: Variables vs Execution Time', fontsize=14)
    plt.xlabel('Number of Variables', fontsize=12)
    plt.ylabel('Execution Time (microseconds)', fontsize=12)

    # display the plot
    plt.grid(True)
    plt.show()


def test_execution(file_name):
    '''
    Runs the 2-SAT solver on input data file and generates results to be verified for correctness.
    Prints the results & writes them to a new csv file.
    Displays whether the wff is Unsatisfiable (U) or Satisfiable (S) and the assignments if Satisfiable
    '''
    # open file to write results to
    f1=open("output_2SAT_Solver_mfues.csv",'w')
    # generate the wffs from the input data file
    Nvars, Nclauses, wffs = build_wff(file_name)
    # iterate through each wff
    for i in range(len(wffs)):
        # test the WFF and collect data
        results = test_wff(wffs[i], Nvars[i], Nclauses[i])
        Assignment=results[1]

        # generate string to print/write to the results file
        if results[2]:
            y='S' # the wff is Satisfiable
        else:
            y='U' # the wff is Unsatisfiable
        # if the wff is Satisfiable, print the variable assignments
        if results[2]: 
            for k in range(Nvars[i]):
                y=y+','+str(Assignment[k][0])
        print(y)
        y = y +'\n'
        f1.write(y)
    # close the results file 
    f1.close()

def trace_execution(file_name):
    '''
    Acknowledgements: This code was adapated from the trace code in the DumbSAT.py file provided by Professor Kogge.
    Trace the results of the 2SAT solver, printing the results & every 10 wffs, printing statistics for those 10 wffs.
    The statistics include:
    - number of Satisfiable and Unsatisfiable wffs
    - average and max time to solve Satisfiable wffs
    - average and max time to solve Unsatisfiable wffs
    This trace output is saved in a file to be compared with the execution time of the DumbSAT solver.
    '''
    # open a new file to write output to
    f1=open("output_2SAT_Solver_trace_mfues.csv",'w')
    f1.write('ProbNum,Nvars,NClauses,LitsPerClause,Result,ExecTime(us)\n') 

    ProbNum = 3
    # read input file and build nvars, nclauses, and wffs lists
    Nvars, NClauses, wffs = build_wff(file_name)

    # initialize values to track statistics
    Scount=Ucount=0
    AveStime=AveUtime=0
    MaxStime=MaxUtime=0
    # iterate through every wff
    for i in range(len(wffs)):
        # get current wff and its corresponding number of variables and number of clauses
        wff = wffs[i]
        Nvar = Nvars[i]
        NClause = NClauses[i]

        # generate results of trying to solve the 2-SAT wff
        results=test_wff(wff,Nvar,NClause)
        wff=results[0]
        Assignment=results[1]
        Exec_Time=results[3]

        # if the wff is Satisfiable, add 'S' to the string to be printed & change Satisfiable statistics accordingly
        if results[2]:
            y='S'
            Scount=Scount+1
            AveStime=AveStime+Exec_Time
            MaxStime=max(MaxStime,Exec_Time)
        # if the wff is Unsatisfiable, add 'U' to the string to be printed & change Unsatisfiable statistics accordingly
        else:
            y='U'
            Ucount=Ucount+1
            AveUtime=AveUtime+Exec_Time
            MaxUtime=max(MaxUtime,Exec_Time)

        # assemble trace string
        x=str(ProbNum)+','+str(Nvar)+','+str(NClause)+','+str(2)
        x=x+str(NClause*2)+','+y+',1,'+str(Exec_Time)
        # if the wff is Satisfiable, add assignments to the string
        if results[2]:
            for k in range(1,Nvar+1):
                x=x+','+str(Assignment[k][0])
        # write the string to the output file
        f1.write(x+'\n') 
        # increment problem number for next iteration
        ProbNum=ProbNum+1
        # if there has been 10 test cases (meaning the number of variables will change), calculate and write statistics to the output file
        if i == len(Nvars)-1 or Nvar != Nvars[i+1]:
            counts='# Satisfied = '+str(Scount)+'. # Unsatisfied = '+str(Ucount)
            maxs='Max Sat Time = '+str(MaxStime)+'. Max Unsat Time = '+str(MaxUtime)
            aves='Ave Sat Time = '+str(AveStime/10)+'. Ave UnSat Time = '+str(AveUtime/10)
            f1.write(counts+'\n')
            f1.write(maxs+'\n')
            f1.write(aves+'\n')

            # recent statistics for next 10 cases
            Scount=Ucount=0
            AveStime=AveUtime=0
            MaxStime=MaxUtime=0
    # close the output file
    f1.close()


#test_execution("check_2SAT_input_mfues.csv")
trace_execution("check_2SAT_input_mfues.csv")
#test_execution("data_generated_2SAT_mfues.csv")
#generate_scatter_plot("data_generated_2SAT_mfues.csv")
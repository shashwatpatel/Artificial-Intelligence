## Task:

Write an AI to generate crossword puzzles, using a constraint satisfaction problem model with node consistency, arc consistency and backtracking search.


## Background:

Given the structure of a crossword puzzle:
* which squares of the grid are to be filled with letters
* which sequence of squares belong to which word to be filled in
* the direction of each word - across or down - in the puzzle
and a list of words to use, the problem of generating a crossword pizzle is choosing which words should go in each sequence of squares.

Each sequence of squares can be is one variable, the value of which needs to be decided from a domain of possible words that will fill the sequence.

These variables have both unary and binary constraints:
* The unary constraint on a variable is its length, i.e. a variable with 4 spaces to be filled in can only accept 4-letter words as values. Any values that do not satisfy a variable's unary constraints can be removed from the variable's domain immediately (enforcing node consistency).
* The binary constraints on a variable are given if its squares overlap with another variable. For example if variable 1 and variable 2 are both consist of four blank spaces and overlap such that variable 1's second space is variable 2's first space, the second character of variable 1's value is constrained to be the same as the 1st character of variable 2's value. Enforcing arc consistency on these variables would result in removing any options from one variable that would not have a corresponding option in one of its constrained variables.
* A further constraint for this specific problem is that all words in the puzzle must be different. This can be formalised as an additional set of binary constraints between every pair of variables such that no two variables can be the same value.


### Node Consistency

* Node Consistency - when all the values in a viarbles domain satisfy the variable's unary constraints.

### Arc Consistency

* Arc Consistency - when all the values in a variable's domain satisfy the variable's binary constraints.
* To make X arc-consistent with respect to Y, remove elements from X's domain until every choice for X has a possible choice for Y.
### Backtracking Search

* Backtracking Search is a recursive algorithm often employed to solve constraint satisfaction problems. Here values are assigned to each variable from the variable's domain, one at a time.
  * If the assignment is consistent with the conditions of the problem being solved, Backtracking Search is recursively called on the csp until all variables are assigned. If all variable are successfully assigned, the problem has been solved and the solution is returned.
  * If a variable is unable to be assigned consistently, the algorithm then returns to a previous variable and changes its assignment to another from its domain, until all options are exhausted. If all options for all variables are exhausted and no solution found, there is no solution to the csp.
## Specification:

Complete the implementation of enforce_node_consistency, revise, ac3, assignment_complete, consistent, order_domain_values, selected_unassigned_variable, and backtrack in generate.py so that your AI generates complete crossword puzzles if it is possible to do so.

The enforce_node_consistency function should update self.domains such that each variable is node consistent.

* Recall that node consistency is achieved when, for every variable, each value in its domain is consistent with the variable’s unary constraints. In the case of a crossword puzzle, this means making sure that every value in a variable’s domain has the same number of letters as the variable’s length.
* To remove a value x from the domain of a variable v, since self.domains is a dictionary mapping variables to sets of values, you can call self.domains[v].remove(x).
* No return value is necessary for this function.

The revise function should make the variable x arc consistent with the variable y.

* x and y will both be Variable objects representing variables in the puzzle.
* Recall that x is arc consistent with y when every value in the domain of x has a possible value in the domain of y that does not cause a conflict. (A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)
* To make x arc consistent with y, you’ll want to remove any value from the domain of x that does not have a corresponding possible value in the domain of y.
* Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
* The domain of y should be left unmodified.
* The function should return True if a revision was made to the domain of x; it should return False if no revision was made.

The ac3 function should, using the AC3 algorithm, enforce arc consistency on the problem. Recall that arc consistency is achieved when all the values in each variable’s domain satisfy that variable’s binary constraints.

* Recall that the AC3 algorithm maintains a queue of arcs to process. This function takes an optional argument called arcs, representing an initial list of arcs to process. If arcs is None, your function should start with an initial queue of all of the arcs in the problem. Otherwise, your algorithm should begin with an initial queue of only the arcs that are in the list arcs (where each arc is a tuple (x, y) of a variable x and a different variable y).
* Recall that to implement AC3, you’ll revise each arc in the queue one at a time. Any time you make a change to a domain, though, you may need to add additional arcs to your queue to ensure that other arcs stay consistent.
* You may find it helpful to call on the revise function in your implementation of ac3.
* If, in the process of enforcing arc consistency, you remove all of the remaining values from a domain, return False (this means it’s impossible to solve the problem, since there are no more possible values for the variable). Otherwise, return True.

The assignment_complete function should (as the name suggests) check to see if a given assignment is complete.

* An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on.
* An assignment is complete if every crossword variable is assigned to a value (regardless of what that value is).
* The function should return True if the assignment is complete and return False otherwise.

The consistent function should check to see if a given assignment is consistent.

* An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. Note that the assignment may not be complete: not all variables will necessarily be present in the assignment.
* An assignment is consistent if it satisfies all of the constraints of the problem: that is to say, all values are distinct, every value is the correct length, and there are no conflicts between neighboring variables.
* The function should return True if the assignment is consistent and return False otherwise.

The order_domain_values function should return a list of all of the values in the domain of var, ordered according to the least-constraining values heuristic.

* var will be a Variable object, representing a variable in the puzzle.
* Recall that the least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. That is to say, if assigning var to a particular value results in eliminating n possible choices for neighboring variables, you should order your results in ascending order of n.
* Note that any variable present in assignment already has a value, and therefore shouldn’t be counted when computing the number of values ruled out for neighboring unassigned variables.
* For domain values that eliminate the same number of possible choices for neighboring variables, any ordering is acceptable.
* Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
* It may be helpful to first implement this function by returning a list of values in any arbitrary order (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that the values are returned in the correct order.
* You may find it helpful to sort a list according to a particular key: Python contains some helpful functions for achieving this.

The select_unassigned_variable function should return a single variable in the crossword puzzle that is not yet assigned by assignment, according to the minimum remaining value heuristic and then the degree heuristic.

* An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. You may assume that the assignment will not be complete: not all variables will be present in the assignment.
* Your function should return a Variable object. You should return the variable with the fewest number of remaining values in its domain. If there is a tie between variables, you should choose among whichever among those variables has the largest degree (has the most neighbors). If there is a tie in both cases, you may choose arbitrarily among tied variables.
* It may be helpful to first implement this function by returning any arbitrary unassigned variable (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that you are returning a variable according to the heuristics.
* You may find it helpful to sort a list according to a particular key: Python contains some helpful functions for achieving this.

The backtrack function should accept a partial assignment assignment as input and, using backtracking search, return a complete satisfactory assignment of variables to values if it is possible to do so.

* An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on. The input assignment may not be complete (not all variables will necessarily have values).
* If it is possible to generate a satisfactory crossword puzzle, your function should reutrn the complete assignment: a dictionary where each variable is a key and the value is the word that the variable should take on. If no satisfying assignment is possible, the function should return None.
* If you would like, you may find that your algorithm is more efficient if you interleave search with inference (as by maintaining arc consistency every time you make a new assignment). You are not required to do this, but you are permitted to, so long as your function still produces correct results. (It is for this reason that the ac3 function allows an arcs argument, in case you’d like to start with a different queue of arcs.)

## Introduction

This file is to help you recreate the graphs in the paper: "Power rivalry and failures in international co-operation" 
by Anwesha Banerjee, Ottmar Edenhofer and Ulrike Kornek. 

Packages needed: matplotlib, scipy, numpy. 

The variables follow the nomenclature in the paper:

w1, w2 are absolute asset levels of country 1 and 2.
pi_1 , pi_2 are their payoffs.
a, c, alpha, beta are as defined in the paper. n denotes the number of countries. 
Note that n = 2 cannot change (the code works only for the 2 country case.)

### [Figure 1](./Fig1.py)
Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.

### [Figure 2](./Fig2.py)

Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.

### [Figure 3 Left Panel](./Fig3a.py)
### [Figure 3 Right Panel](./Fig3b.py)
Insert the wealth levels you want to test for in the first line of the main function: for the example in the paper, 
we use the levels of wealth: [5000,500]. 

Insert the parameters a, c, alpha and beta in the first line of the function "function_looper_endog" in 
[functionsFig3a.py](./functionsFig3a.py). 

### [Figure 4,6](./Fig4Fig6.py) 
### [Figure 5,7](./Fig5Fig7.py)
### [Figure 10,11](./Fig10Fig11.py)
### [Figure 12,13](./Fig12Fig13.py)

Absolute wealth and parameters "a, alpha, beta" and the marginal returns from the public good for the two countries "c1 and c2"
(c1 for country 1.) are the same as in the paper.
These are inserted in the first lines of the main function.

### [Figure 8](./Fig8.py)

Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.

### [Figure 9](./Fig9.py)

Figure 9 of the paper can be generated through the main function. Wealth and parameters a, c, alpha, beta are changed in 
the first lines of the main function. The number of iterations is changed through the variable "num_deltas".


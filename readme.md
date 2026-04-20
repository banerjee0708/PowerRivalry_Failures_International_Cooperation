## Introduction

This file is to help you recreate the graphs in the paper: "Power rivalry and failures in international co-operation" 
by Anwesha Banerjee, Ottmar Edenhofer and Ulrike Kornek. 

Packages needed: matplotlib, scipy, numpy. 

The variables follow the nomenclature in the paper:

w1, w2 are absolute asset levels of country 1 and 2.
pi_1 , pi_2 are their payoffs.
a, c, alpha, beta are as defined in the paper. n denotes the number of countries. 
Note that n = 2 cannot change (the code works only for the 2 country case.)

### [Figure 1, Figure 9](./Fig1Fig9.py)
Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.

Figure 1 of the paper can be generated through figure 1 of the script by setting wealth to [5000,500] and then 
to [5000,5000].


Figure 9 of the paper can be generated through figure 2 of the script by setting wealth to [5000,500] and then 
changing the number of iterations "num_deltas" to 10000.

### [Figure 2](./Fig2.py)

Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.

### [Figure 3](Fig3.py)
Insert the wealth levels you want to test for in the first line of the main function: for the example in the paper, 
we use two levels of wealth: [5000,500] and [4000,3500]

Insert the parameters a, c, alpha and beta in the first line of the function "function_looper_endog" in 
[functionsFig3.py](functionsFig3.py). 

```shell
python Fig3.py
```

### [Figure 4-7, Figure 10-13](./Fig4-7Fig10-13.py)

Wealth and parameters a, alpha, beta and the marginal returns from the public good for the two countries c1 and c2 
(c1 for country 1.) 
These are inserted in the first lines of the main function.

### [Figure 8](./Fig8.py)

Wealth and parameters a, c, alpha, beta are changed in the first lines of the main function.



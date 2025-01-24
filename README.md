# Circle Packing

## Problem Statement
This project seeks finding the maximum radius for the packing of n circles in a square box. It is based on the paper from 1997 by Numerla and Östergård: 'Packing up to 50 Equal Circles in a Square'.
As pointed out by the paper, the solution of this problems implies the solution of the problem of packing the most circles with a given radius in a box (by just scaling the dimensions and comparing configurations).

## Results
This piece of code succesfully aproaches the results from the paper. Some plots for the obtained configurations are shown as follows:

Case n = 25, radius = 0.2499999999455803 (in the paper, radius =  0.250000000 ) 
![packing_n25](https://github.com/user-attachments/assets/979013d2-ae55-4928-9c28-a650d71bb9eb)

Case n = 45, radius = 0.17277096895323163 (in the paper, radius = 0.175515450)
![packing_n45](https://github.com/user-attachments/assets/ec8ae9c8-a717-4459-b6a7-addc7e93cbd8)

Case n = 81, radius = 0.12499950076451175 (in the best known configuration (listed in http://www.packomania.com/), radius = 0.12833685597387634419 )
![packing_n81](https://github.com/user-attachments/assets/33dd954a-a944-4a55-9f13-6efc8efe8f09)

It is interesting to compare the cases n = 25 and n = 81 and see how the latter loses the symmetry one would expect for a square number, actually, this symmetry is first broken for the case n = 49, where the configuration including hexagonal packing is proven to be better.

## Further actions
Some improvements that can be done are:
 - Implementation of system of nonlinear equations (modeling the contact of the circles to other circles and the boundary) to further improve a found optimum configuration, as suggested by Numerla et al.
 - Proper scaling of the system, i. e. set the square box to have side lenght 2.

## Credits
Ian Rincón (from Universidad de Colima) provided valuable insights during the course of this project.

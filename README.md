# Circle Packing

## Problem Statement
This project seeks finding the best configuration that packs n circles in a square box and it is bases on the paper from 1997 by Numerla and Östergård: 'Packing up to 50 Equal Circles in a Square'.


## Results
The known value for the volume of the largest 8-vertex polyhedra (V = 1.81570) is succesfully reached to at least 3 decimal places.
The result for the area problem with n = 8 was a value around 8.12, a bit far from a theoretical result (as seen by Donahue et al. in https://arxiv.org/pdf/2005.13660)
Trials for grater values of n also appear relatively close to other results (for example for n = 10, the code yields as maximum area 8.96, whereas the paper by Danahue lists it as 9.02)

## Further doings
Some improvements that can be done are:
 - Fixing one point so the search becomes faster (only n-1 points will be being perturbated)

## Credits
Ian Rincón (from Universidad de Colima) provided helpful insights during the doing of this project.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
+ Empty MultiIndex:
mi= ()
+ Dimension 4 MultiIndex:
mi= (1, 0, 5, 7)
max_dim =  4
sum= 13
Convert to tuple =  <class 'tuple'>
index =  0 , value =  1
index =  2 , value =  5
index =  3 , value =  7
+ Combination rule
(4,)
(5,)
(3, 1)
(4, 1)
(2, 2)
(3, 2)
(1, 3)
(2, 3)
(0, 4)
(1, 4)
(0, 5)
+ Rectangle
(4, 4, 4, 4, 4)
+ Simplex
(2,)
(3,)
(4,)
(5,)
(1, 1)
(2, 1)
(3, 1)
(4, 1)
(0, 2)
(1, 2)
(2, 2)
(3, 2)
(0, 3)
(1, 3)
(2, 3)
(0, 4)
(1, 4)
(0, 5)
(1, 0, 1)
(2, 0, 1)
(3, 0, 1)
(4, 0, 1)
(0, 1, 1)
(1, 1, 1)
(2, 1, 1)
(3, 1, 1)
(0, 2, 1)
(1, 2, 1)
(2, 2, 1)
(0, 3, 1)
(1, 3, 1)
(0, 4, 1)
(0, 0, 2)
(1, 0, 2)
(2, 0, 2)
(3, 0, 2)
(0, 1, 2)
(1, 1, 2)
(2, 1, 2)
(0, 2, 2)
(1, 2, 2)
(0, 3, 2)
(0, 0, 3)
(1, 0, 3)
(2, 0, 3)
(0, 1, 3)
(1, 1, 3)
(0, 2, 3)
(0, 0, 4)
(1, 0, 4)
(0, 1, 4)
(0, 0, 5)
(1, 0, 0, 1)
(2, 0, 0, 1)
(3, 0, 0, 1)
(4, 0, 0, 1)
(0, 1, 0, 1)
(1, 1, 0, 1)
[etc.]
(1, 0, 1, 3)
(0, 1, 1, 3)
(0, 0, 2, 3)
(0, 0, 0, 4)
(1, 0, 0, 4)
(0, 1, 0, 4)
(0, 0, 1, 4)
(0, 0, 0, 5)
"""
import indices

# Experiment with MultiIndex class
mi = indices.MultiIndex() # Empty
print("+ Empty MultiIndex:")
print("mi=", mi)
print("+ Dimension 4 MultiIndex:")
mi = indices.MultiIndex([1, 0, 5, 7]) # Dim 4
print("mi=", mi)
print("max_dim = ", mi.max_dim())
print("sum=", mi.sum())
print("Convert to tuple = ", type(mi.full_tuple()))
# Print non-zero values
for index, value in mi:
    print("index = ", index, ", value = ", value)

#
print("+ Combination rule")
d = 2
L = 5

def admissible(mi):
    return mi.sum() <= L

mis = indices.get_admissible_indices(admissible, dim=d)
cr = indices.combination_rule(mis)
for mi in cr:
    print(mi)

#
print("+ Rectangle")
d = 5
L = 5
sparseindices = indices.cartesian_product([range(L)] * d)
cr = indices.combination_rule(sparseindices)
for mi in cr:
    print(mi)

#
print("+ Simplex")
L = 5
dimension = 4
mis = indices.simplex(L=L, n=dimension)
cr = indices.combination_rule(mis)
for mi in cr:
    print(mi)


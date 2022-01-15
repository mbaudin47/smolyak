#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 16:23:13 2022

@author: devel
"""
import indices

mi = indices.MultiIndex()
print(mi)

d = 2
L = 5


def admissible(mi):
    T = [value for __, value in mi]
    return sum(T) <= L


mis = indices.get_admissible_indices(admissible, dim=d)
CR = indices.combination_rule(mis)
for mi in CR:
    print(mi)

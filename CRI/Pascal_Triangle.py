# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:26:14 2020

Please write a function to return a Pascal Triangle

@author: rmileng
"""
import numpy as np

def generate_Pascal_Triangle(n):
    if n==1:
        return [1]
    else:
        tri = [1,1] 
        i = 3
        while i <= n:
            result = np.zeros(i)  
            result[0] = result[-1] = 1
            for j in range(1,int(np.floor(i/2))+1):           
                result[j] = result[-j-1] = tri[j-1]+tri[j]
            i += 1
            tri = result        
        return tri

def pascals_triangle(n_rows):
    results = [] # a container to collect the rows
    for _ in range(n_rows): 
        row = [1] # a starter 1 in the row
        if results: # then we're in the second row or beyond
            last_row = results[-1] # reference the previous row
            # this is the complicated part, it relies on the fact that zip
            # stops at the shortest iterable, so for the second row, we have
            # nothing in this list comprension, but the third row sums 1 and 1
            # and the fourth row sums in pairs. It's a sliding window.
            row.extend([sum(pair) for pair in zip(last_row, last_row[1:])])
            # finally append the final 1 to the outside
            row.append(1)
        results.append(row) # add the row to the results.
    return results

# generator
def triangles(n,r=[]): # iterate based on r
    for x in range(n):
        l = len(r)
        r = [1 if i == 0 or i == l else r[i-1]+r[i] for i in range(l+1)]
        yield r
print(list(triangles(5)))

        
        
        
        
        
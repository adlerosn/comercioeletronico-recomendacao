#!/usr/bin/env python3
# -*- encoding: utf-8 *-*

from typing import Callable, List

def similaridade(
        a:List[float],
        b:List[float]
    )->float:
    rabar = sum(a)/len(a)
    rbbar = sum(b)/len(b)
    num = 0
    dn1 = 0
    dn2 = 0
    for p in range(len(a)):
        num+= (a[p]-rabar)*(b[p]-rbbar)
    for p in range(len(a)):
        dn1+= (a[p]-rabar)**2
    for p in range(len(a)):
        dn2+= (b[p]-rbbar)**2
    try:
        return num/((dn1**0.5)*(dn2**0.5))
    except:
        return 0

def predicao(
        a:List[float],
        n:List[List[float]],
        p:int,
        sim:Callable[[list,list], float] = similaridade
    )->float:
    rabar = sum(a)/len(a)
    num = 0
    den = 0
    for b in n:
        rbbar = sum(b)/len(b)
        num+= sim(a,b)*(b[p]-rbbar)
    for b in n:
        den+= sim(a,b)
    try:
        return rabar+(num/den)
    except:
        return 0

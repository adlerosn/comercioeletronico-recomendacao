#!/usr/bin/env python3
# -*- encoding: utf-8 *-*

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

def filtrarNonesFora(a,b):
    while len(a) > len(b):
        del a[-1]
    while len(a) < len(b):
        del b[-1]
    i = len(a) - 1
    while i >= 0:
        if a[i] is None or b[i] is None:
            del a[i]
            del b[i]
        i-=1
    return a,b

def similaridade(
        a,
        b,
        fail = 0,
    ):
    a,b = filtrarNonesFora(a[:], b[:])
    if (len(a) == 0) or (len(b) == 0):
        return fail
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
        return fail

def predicao(
        a,
        n,
        p,
        sim = similaridade,
    ):
    nonesOut = (lambda nn: list(filter((lambda a: a is not None), nn)))
    rabar = sum(nonesOut(a))/len(nonesOut(a))
    num = 0
    den = 0
    for b in n:
        if b[p] is None:
            continue
        simAB = sim(a,b)
        if simAB is None:
            continue
        rbbar = sum(nonesOut(b))/len(nonesOut(b))
        num+= simAB*(b[p]-rbbar)
        den+= simAB
    try:
        return rabar+(num/den)
    except:
        return 0

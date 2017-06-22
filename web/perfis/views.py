# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
#!/usr/bin/env python3

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import cli
import sqlite3
import random

def index(request):
    return render(request, 'bemvindo.html')

def recomendacaofilmeusuario(request):
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')

    max = cli.pickTotalFilmes(db)
    return render(request, 'recomendacaofilmeusuario.html',{"maximo":max})

def recomendacaofilmeusuarioresposta(request, perfil_id):
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')
    max = cli.menuRecomendacaoFilmeParaUsuario(db,perfil_id)

    if "não" in max:
        return render(request, 'recomendacaofilmeusuarioresposta.html',{"retorno":max,"ATIVADO": "block"})
    else:
        return render(request, 'recomendacaofilmeusuarioresposta.html',{"retornomax":max,"ATIVADO": "none"})
def usuariofilme(request):
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')

    max = cli.pickTotalFilmes(db)
    return render(request, 'usuariofilme.html')

def perfilusufilme(request):
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')

    lista = cli.getFilmes(db)
    return render(request, 'perfilusufilme.html', { "listaFilmes" : lista})


def perfilusufilmeresposta(request, perfil_id):
    
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')

    lista = cli.menuRecomendacaoPerfilUsuarioParaFilme(db,perfil_id)
    return render(request, 'perfilusufilmeresposta.html', { "pessoas" : lista.y0 ,"generos":lista.y1 ,"media":lista.y2})
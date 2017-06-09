#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import libRecomendacao
import sqlite3
import random

def clearScr():
    for i in range(10):
        print()

def pressEnterToReturn(msg:str = 'Pressione ENTER para voltar.')->str:
    return input(msg)

def avg(iter):
    return sum(iter)/len(iter)

def pickTotalFilmes(db):
    cursor = db.cursor()
    cursor.execute('select movieId from movies order by movieId desc limit 1')
    totalFilmes = cursor.fetchone()[0]
    cursor.close()
    return totalFilmes

def pickRatingsUsuario(db,usuario):
    cursor = db.cursor()
    cursor.execute('select userId, movieId, rating from ratings where userId = ?',(usuario,))
    ratingsUsuario = list(cursor.fetchall())
    cursor.close()
    return ratingsUsuario

def pickRatingsFilme(db,filme):
    cursor = db.cursor()
    cursor.execute('select userId, movieId, rating from ratings where movieId = ?',(filme,))
    ratingsFilme = list(cursor.fetchall())
    cursor.close()
    return ratingsFilme

def pickFilme(db,filme):
    cursor = db.cursor()
    cursor.execute('select movieId, title, year from movies where movieId = ?',(filme,))
    filme = cursor.fetchone()
    cursor.close()
    return filme

def pickGenresFilme(db,filme):
    cursor = db.cursor()
    cursor.execute('select movieId, genreId from moviegenre where movieId = ?',(filme,))
    generos = cursor.fetchall()
    cursor.close()
    return [g[1] for g in generos]

def pickGenres(db):
    cursor = db.cursor()
    cursor.execute('select genreId, genre from genres')
    generos = cursor.fetchall()
    cursor.close()
    return {g[0]:g[1] for g in generos}

def predizNota(db,usuario,filme):
    totalFilmes = pickTotalFilmes(db)
    a = [None for x in range(totalFilmes+1)]
    for rt in pickRatingsUsuario(db,usuario):
        a[rt[1]]=rt[2]
    c = 0
    ous = pickRatingsFilme(db,filme)
    n = [[None for x in range(totalFilmes+1)] for y in range(len(ous))]
    for ou in ous:
        for rt in pickRatingsUsuario(db,ou[0]):
            n[c][rt[1]]=rt[2]
        c+=1
    return libRecomendacao.predicao(a,n,filme,libRecomendacao.similaridade)

def predizNotaRapidamente(db,usuario,filme):
    notas = [rt[2] for rt in pickRatingsFilme(db,filme)]
    return sum(notas)/len(notas)

def getUsuario(db):
    cursor = db.cursor()
    cursor.execute('select userId from ratings')
    allUsers = [i[0] for i in cursor.fetchall()]
    print('Usuários de exemplo: '+', '.join(map(str,random.sample(allUsers,3))))
    u = None
    while u is None:
        u = input('["x" para abortar] Insira ID do usuário: ')
        if u == 'x' or u == '"x"':
            return None
        elif (not u.isdigit()) or (int(u) not in allUsers):
            u = None
            print('Usuário inexistente')
        else:
            return int(u)

def searchMovie(db,u):
    u = u.replace('"',' ').replace('\'',' ').replace('%',' ').replace('_',' ')
    while '  ' in u:
        u = u.replace('  ',' ')
    terms = u.strip().split(' ')
    terms = ['title like "%'+term+'%"' for term in terms]
    cursor = db.cursor()
    cursor.execute('select movieId, title, year from movies where '+(' and '.join(terms))+' limit 7')
    r = list(cursor.fetchall())
    cursor.close()
    return r

def printMovieTable(searchResults):
    tbl = '| {0:>8} | {1:<40} | {2:>4} |'
    tblDiv = '+'+10*'-'+'+'+42*'-'+'+'+6*'-'+'+'
    print(tblDiv)
    print(tbl.format(*['ID','Título','Ano']))
    print(tblDiv)
    for searchResult in searchResults[:7]:
        print(tbl.format(*searchResult))
    print(tblDiv)

def getFilme(db):
    cursor = db.cursor()
    cursor.execute('select movieId, title, year from movies')
    dbrt = cursor.fetchall()
    cursor.close()
    allMovies = [i[0] for i in dbrt]
    print('Filmes de exemplo: '+', '.join(map(str,random.sample(allMovies,3))))
    u = None
    while u is None:
        u = input('["x" para abortar] Insira ID do filme ou pesquise: ')
        if u == 'x' or u == '"x"':
            return None
        elif (not u.isdigit()) or (int(u) not in allMovies):
            print('ID de filme inexistente: pesquisando pelo título...')
            searchResults = searchMovie(db,u)
            printMovieTable(searchResults)
            u = None
        else:
            return int(u)

def normalizaNota(pred):
    return max(min((pred*20),100),0)

def menuzaoGenerico(titulo:str, itens:dict)->int:
    o = ''
    acc = list(map(str,range(0,10)))
    while o not in acc:
        print('=== %s ==='%(titulo))
        for i in range(1,10):
            print(' %d. %s'%(i,itens.get(i,'')))
        print(' 0. Sair')
        o = input('Selecione sua opção: ')
        if (o not in acc) or (o.isdigit() and (str(itens.get(int(o),'')) == '')):
            if o == '0':
                print('Saindo...')
            else:
                print('Escolha não existente')
        else:
            print()
    return int(o)

def menuClassificacaoUsuarioFilme(db):
    clearScr()
    usuario = getUsuario(db)
    if usuario is None:
        return
    filme = getFilme(db)
    if filme is None:
        return
    cursor = db.cursor()
    cursor.execute('select userId, movieId, rating from ratings where userId = ? and movieId = ?',(usuario,filme))
    todos = cursor.fetchall()
    cursor.close()
    clearScr()
    if len(todos)>0:
        print('Usuário já deu nota para este filme.')
        print('%d%%'%(todos[0][2]*20))
    else:
        print('Predizendo nota... aguarde.')
        pred = predizNota(db,usuario,filme)
        if pred is None:
            print('Dados insuficientes')
        else:
            print('%d%%'%(normalizaNota(pred)))
    pressEnterToReturn()

def menuRecomendacaoFilmeParaUsuario(db):
    clearScr()
    usuario = getUsuario(db)
    if usuario is None:
        return
    clearScr()
    ratingsUsuario = pickRatingsUsuario(db,usuario)
    if len(ratingsUsuario)>0:
        assistido = set([rt[1] for rt in ratingsUsuario])
        aAssistir = []
        for filme in assistido:
            for telespectador in set([rt[0] for rt in pickRatingsFilme(db,filme)]):
                for sugestao in set([rt[1] for rt in pickRatingsUsuario(db,telespectador)]):
                    if sugestao not in assistido:
                        aAssistir.append(sugestao)
        aAssistir = list(set(aAssistir))
        if len(aAssistir)>0:
            print('Pessoas que assistiram os filmes que o usuário assistiu')
            print('assistiram %d títulos a mais.'%len(aAssistir))
            rank = []
            c = 0
            for filme in aAssistir:
                if c%250 == 0:
                    print('Preparando TOP-7... %d%%'%((100*c)/len(aAssistir)))
                pass
                nota = predizNotaRapidamente(db,usuario,filme)
                rank.append((nota, filme))
                c+=1
            print('Preparando TOP-7... 100%')
            rank = list(reversed(list(sorted(rank))))
            filmes = []
            for _,filme in rank[:7]:
                filmes.append(pickFilme(db,filme))
            pass
            printMovieTable(filmes)
        else:
            print('Usuário já assistiu todos os filmes de sua bolha social')
    else:
        print('Usuário não avaliou nada')
    pressEnterToReturn()

def menuRecomendacaoPerfilUsuarioParaFilme(db):
    clearScr()
    filme = getFilme(db)
    if filme is None:
        return
    ratingsFilme = pickRatingsFilme(db,filme)
    mediaFilme = avg([rt[2] for rt in ratingsFilme])
    outrosFilmes = []
    for telespectador in set([rt[0] for rt in ratingsFilme]):
        for sugestao in set([rt[1] for rt in pickRatingsUsuario(db,telespectador)]):
            outrosFilmes.append(sugestao)
    outrosFilmes = list(set(outrosFilmes))
    generosEste = dict()
    gens = pickGenresFilme(db,filme)
    for gen in gens:
        generosEste[gen] = generosEste.get(gen,mediaFilme)
    generosTodos = dict()
    print('As pessoas que avaliaram o filme selecionado,')
    print('também avaliaram outros %d filmes'%len(outrosFilmes))
    c = 0
    for outroFilme in outrosFilmes:
        if c%250 == 0:
            print('Preparando perfil do nicho de espectadores... %d%%'%((100*c)/len(outrosFilmes)))
        pass
        rf = avg([rf[2] for rf in pickRatingsFilme(db,outroFilme)])
        gens = pickGenresFilme(db,outroFilme)
        for gen in gens:
            generosTodos[gen] = generosTodos.get(gen,[])
            generosTodos[gen].append(rf)
        c+=1
    for key in generosTodos:
        generosTodos[key] = avg(generosTodos[key])
    clearScr()
    tbl = '| {0:<15} | {1:>6}% | {2:>7}% |'
    tblDiv = '+'+17*'-'+'+'+9*'-'+'+'+10*'-'+'+'
    print(tblDiv)
    print(tbl.format(*['Genero','Nicho','\u0394filme']))
    print(tblDiv)
    generosDb = pickGenres(db)
    for key in generosDb:
        notaGlobal = None
        if key in generosTodos: notaGlobal = normalizaNota(generosTodos[key])
        notaFilme = None
        if key in generosEste: notaFilme = normalizaNota(generosEste[key])
        display = ['Genre','???','???']
        display[0] = generosDb[key]
        if not (notaGlobal is None):
            display[1] = '%.2f'%notaGlobal
            if not (notaFilme is None):
                display[2] = '%.2f'%(notaGlobal-notaFilme)
        print(tbl.format(*display))
    print(tblDiv)
    try:
        gt = normalizaNota(avg(list(generosTodos.values())))
        ge = normalizaNota(avg(list(generosEste.values())))
        if gt is None or ge is None:
            raise Exception('dont print')
        print(tbl.format(*['Média','%.2f'%gt,'%.2f'%(gt-ge)]))
        print(tblDiv)
    except:
        pass
    pressEnterToReturn()

def menuPrincipal(db):
    selecao = 1
    while selecao!=0:
        selecao = menuzaoGenerico('Menu Principal',{
            1: 'Classificação usuário\u00d7filme',
            2: 'Recomendações de filmes para usuário',
            3: 'Perfil de usuários para filme',
        })
        if selecao == 0:
            break
        elif selecao == 1:
            menuClassificacaoUsuarioFilme(db)
        elif selecao == 2:
            menuRecomendacaoFilmeParaUsuario(db)
        elif selecao == 3:
            menuRecomendacaoPerfilUsuarioParaFilme(db)
        else:
            pass
    return

def main():
    db = None
    try:
        db = sqlite3.connect('database.db')
    except:
        print('Erro ao conectar-se ao banco de dados')
    if not (db is None):
        menuPrincipal(db)
    return

if __name__ == '__main__':
    main()

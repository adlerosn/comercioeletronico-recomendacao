#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import someUtils
import sqlite3
import csv

someUtils.rmf('database.db-journal')
someUtils.rmf('database.db')
someUtils.saveFile('database.db','')

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE movies (
    movieId serial,
    title varchar(255),
    genres varchar(255),
    primary key (movieId)
);''')

cursor.execute('''
CREATE TABLE ratings (
    userId int,
    movieId int,
    rating float,
    timestamp int,
    primary key (userId, movieId),
    foreign key (movieId) references movies(movieId)
);''')

cursor.execute('''
CREATE TABLE tags (
    userId int,
    movieId int,
    tag varchar(255),
    timestamp int,
    foreign key (movieId) references movies(movieId)
);''')

cursor.execute('''
CREATE TABLE links (
    movieId int,
    imdbId varchar(20),
    tmdbId varchar(20),
    primary key (movieId),
    foreign key (movieId) references movies(movieId)
);''')

cursor.execute('''
CREATE TABLE genometags (
    tagId int,
    tag varchar(255),
    primary key (tagId)
);''')

cursor.execute('''
CREATE TABLE genomescores (
    movieId int,
    tagId int,
    relevance float,
    primary key (movieId, tagId),
    foreign key (movieId) references movies(movieId),
    foreign key (tagId) references genometags(tagId)
);''')

tables = [
    ['movies.csv','movies'],
    ['ratings.csv','ratings'],
    ['tags.csv','tags'],
    ['links.csv','links'],
    ['genome-tags.csv','genometags'],
    ['genome-scores.csv','genomescores'],
]

import sys
from io import StringIO

for table in tables:
    print(table[1])
    try:
        with open(table[0]) as csvfile:
            wholefile = csvfile.read()
#            reader = csv.reader(csvfile)
            reader = csv.reader(StringIO(wholefile))
            del wholefile
            iterreader = iter(reader)
            fields = next(iterreader)
            preparedSql = (
                'insert into '+table[1]+
                '('+(','.join(fields))+') '+
                'values ('+(','.join(['?']*len(fields)))+')'
            )
            print(preparedSql)
            sys.stdout.flush()
            for row in iterreader:
                cursor.execute(preparedSql, row)
    except Exception as e:
        print('Skipped: ',end='')
        print(e.__class__.__name__,end='')
        print(': ',end='')
        print(e)


cursor.close()
connection.commit()
connection.close()

someUtils.mv('database.db','database_step1.db')

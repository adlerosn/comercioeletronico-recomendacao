#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import someUtils
import sqlite3

print('preparing envronment')

someUtils.rmf('database.db-journal')
someUtils.rmf('database.db')
someUtils.rmf('database_step2.db')
someUtils.cp('database_step1.db','database.db')

print('dealing with data')

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

print('>> add year to movies')
cursor.execute('ALTER TABLE movies ADD year int')
cursor.execute('update movies set year = cast(substr(title,-1,-4) as int)')
cursor.execute('update movies set title=substr(title, 0, length(title)-6) where year<>0')

print('>> normalize genres')
genres = set()
for row in cursor.execute('select distinct genres from movies where genres<>"(no genres listed)" and genres is not null'):
    genres = genres.union(set(row[0].split('|')))
    del row
genres = list(sorted(genres))
cursor.execute('''
CREATE TABLE genres (
    genreId serial not null,
    genre varchar(255),
    primary key (genreId)
);''')
genreAdd = []
for genre in genres:
    genreAdd.append([len(genreAdd)+1,genre])
    del genre
cursor.executemany('insert into genres(genreId,genre) values (?,?)',genreAdd)
del genreAdd
cursor.execute('''
CREATE TABLE moviegenre (
    movieId int,
    genreId int,
    primary key (movieId, genreId),
    foreign key (movieId) references movies(movieId),
    foreign key (genreId) references genres(genreId)
);''')
cursor.execute('''
insert into
    moviegenre(movieId,genreId)
select
    movies.movieId,
    genres.genreId
from
    movies
    left join
        genres
where
    '|' || movies.genres || '|'
        like
        '%|'||genres.genre||'|%'
''')
# SQLite não suporta "ALTER TABLE tbl DROP COLUMN col"
cursor.execute('''
CREATE TABLE movies2 (
    movieId serial,
    title varchar(255),
    year int,
    primary key (movieId)
);''')
cursor.execute('''
insert into
    movies2(movieId,title,year)
select
    movieId,
    title,
    year
from
    movies
''')
cursor.execute('''drop table movies''')
cursor.execute('''
CREATE TABLE movies (
    movieId serial,
    title varchar(255),
    year int,
    primary key (movieId)
);''')
cursor.execute('''
insert into
    movies(movieId,title,year)
select
    movieId,
    title,
    year
from
    movies2
''')
cursor.execute('''drop table movies2''')

print('>> normalize tags')
cursor.execute('update tags set tag=lower(tag)')
cursor.execute('alter table tags rename to movietag2')
cursor.execute('''
CREATE TABLE tags (
    tagId serial,
    tag varchar(255),
    primary key (tagId)
);''')
cursor.execute('''
CREATE TABLE movietag (
    userId int,
    movieId int,
    tagId int,
    timestamp int,
    foreign key (movieId) references movies(movieId)
    foreign key (tagId) references tags(tagId)
);''')

tags = list()
for row in cursor.execute('select distinct tag from movietag2 order by tag'):
    tags.append(row[0])
    del row
tags = list(sorted(tags))
tagAdd = []
for tag in tags:
    tagAdd.append([len(tagAdd)+1,tag])
    del tag
cursor.executemany('insert into tags(tagId,tag) values (?,?)',tagAdd)
del tagAdd

cursor.execute('''
insert into movietag(userId,movieId,tagId,timestamp)
select
    movietag2.userId,
    movietag2.movieId,
    tags.tagId,
    movietag2.timestamp
from
    movietag2
        inner join
    tags
        on (movietag2.tag = tags.tag)
''')

cursor.execute('drop table movietag2')

cursor.close()
connection.commit()
connection.close()

someUtils.mv('database.db','database_step2.db')

#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import someUtils
import sqlite3

print('preparing envronment')

someUtils.rmf('database.db-journal')
someUtils.rmf('database.db')
someUtils.rmf('database_step3.db')
someUtils.cp('database_step2.db','database.db')

print('vacumming')

connection = sqlite3.connect('database.db')
connection.execute('VACUUM')
connection.commit()
connection.close()

someUtils.cp('database.db','database_step3.db')

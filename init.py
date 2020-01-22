#!/usr/bin/python3

import configparser
import sqlite3
import sys

conn = sqlite3.connect('feeds.db')

c = conn.cursor()

c.execute('''CREATE TABLE settings
             (name text,
              url text)
          ''')

c.execute('''CREATE TABLE feeds
             (id integer primary key autoincrement,
              name text,
              title text,
              blog_url text,
              url text,
              etag text,
              modified text)
          ''')

c.execute('''CREATE TABLE posts
             (id integer primary key autoincrement,
             feed_id integer,
             author text,
             title text,
             post text,
             url text,
             published_date datetime)
          ''')

if len(sys.argv) > 1:

    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    for section in config.sections():
        if section == 'Planet':
            continue
        print(f"{section} {config[section]['name']}")
        c.execute(f'''INSERT INTO feeds (name, url) VALUES
                  ("{config[section]['name']}", "{section}")''')

conn.commit()

#!/usr/bin/python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import sqlite3
import time

MAX_ENTRIES_PER_FEED = 8


def filter_date(value, format='%d %B %Y'):
    return time.strftime(format, time.strptime(value, '%Y-%m-%d %H:%M:%S'))


conn = sqlite3.connect('feeds.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

c.execute('SELECT name, url, etag, modified, id FROM feeds ORDER BY name')

feeds = c.fetchall()

c.execute('''SELECT f.name, f.url as blog_url, f.title as blog_title,
                    p.feed_id, p.title, p.url, p.post, p.published_date,
                    p.author
             FROM posts p, feeds f
             WHERE f.id = p.feed_id
             ORDER by p.published_date DESC
             LIMIT 20''')

posts = c.fetchall()

conn.close()


file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.filters['date'] = filter_date

template = env.get_template('index.html.j2')

output = template.render(generate_time=datetime.strftime(datetime.utcnow(),
                                                         "%d %B %Y %H:%M"),
                         posts=posts, feeds=feeds)
print(output)

#!/usr/bin/python3

from datetime import datetime

import feedparser
import sqlite3
import sys
import time

MAX_ENTRIES_PER_FEED = 8

force = False

if len(sys.argv) > 1 and sys.argv[1] == '--force':
    force = True

conn = sqlite3.connect('feeds.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

c.execute('SELECT name, url, etag, modified, id FROM feeds')

for feed in c.fetchall():
    print(feed['name'])

    etag = feed['etag']
    modified = feed['modified']

    if force:
        etag = 0
        modified = 0

    url = feed['url']

    try:
        # etag and modified tell when we last checked so can get only newer
        # posts
        data = feedparser.parse(url, etag=etag, modified=modified)
        if 'etag' not in data:
            data.etag = 0
        if 'modified' not in data:
            data.modified = 0
        if 'status' not in data:
            data.status = 200

        print(f'''
ETag:      {data.etag}
Modified:  {data.modified}
Status:    {data.status}
Posts:     {len(data.entries)}
''')
        if data.status == 301:  # permanent redirection
            url = data.href

        c.execute('UPDATE feeds SET etag=?, modified=?, url=? WHERE id=?',
                  (data.etag, data.modified, url, feed['id']))

        # if we got all posts then drop all stored ones
        if data.status == 200:
            c.execute('DELETE FROM posts WHERE feed_id=?', (feed['id'],))

        counter = 0
        for post in data.entries:

            if 'content' in post:
                content = post.content[0].value
            elif 'summary' in post:
                content = post.summary

            published = datetime.fromtimestamp(
                time.mktime(post.published_parsed[:8] + (-1,)))

            c.execute('''INSERT INTO posts (feed_id, title, post, url,
                      published_date) VALUES (?, ?, ?, ?, ?)''',
                      (feed['id'], post.title, content, post.link,
                       published))
            counter += 1
            if counter == MAX_ENTRIES_PER_FEED:
                break

    except RuntimeError:
        print('failed')
        pass

    print(' ')

conn.commit()
conn.close()

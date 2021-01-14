# Very Simple Planet Aggregator

As Venus was Python 2 only I decided that I need something else to run my
[Developer's Planet](https://devplanet.one.pl/) aggregator.

This is the result of few hours of playing with FeedParser and Jinja2.

# Usage

1. Run `init.py planet.ini` to create database and import feeds from Venus
   config file.
2. `fetch.py` script will connect to each feed and fetch it's posts.
3. `generate.py` loads template files and outputs result (HTML page and RSS 2.0
   feed XML).

# Features

- first eight posts are then added to database. Amount is hard coded.
- if server responds with HTTP 301 then feed address will be updated.
- content of ETag and last modified date headers are stored in database and used
  if present
  - use '--force' option with 'fetch.py' script to force refresh

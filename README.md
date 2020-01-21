# Very Simple Planet Aggregator

As Venus is Python 2 only I decided that I need something else to run my
[Developer's Planet](https://devplanet.cf) aggregator.

This is the result of few hours of playing with FeedParser and Jinja2.

# Usage

Run `init.py planet.ini` to create database and import feeds from Venus config
file.

Next step is `fetch.py` which will connect to each feed and fetch it. First
eight posts add then added to database. If server responds with HTTP 301 then
address will be updated. ETag and last modified date are stored in database and
used if present - adding '--force' to script will make it forget about them
during run.

Last step is `generate.py` - it loads 'templates/index.html.j2' file and outputs
result.

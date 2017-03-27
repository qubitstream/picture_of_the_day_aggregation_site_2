Picture of the Day
==================

## About


This is the source code for an aggregation site for various "Picture of the day" sites, written in [Django](https://www.djangoproject.com/).

_Picture of the day_ site currently supported:

* [Wikipedia (english)](https://en.wikipedia.org/)

## Configuration

Create a virtualenv and install the requirements listed in `requirements.txt`. The code has been tested with **Python 3.4** in mind.
See `DEVNOTES.md` for additional information.


### Environment variables

#### Mandatory

* `DJANGO_SETTINGS_MODULE`: The settings module to be used, e.g.:`potd_ii.settings.local`
* `POTD_II_SECRET_KEY`: For Django's `SECRET_KEY` setting

#### Optional

If you wish to use PostgreSQL:

* `POTD_II_POSTGRESQL_HOST`: Hostname of the DB server - optional, default: `localhost`
* `POTD_II_POSTGRESQL_DB_NAME`: PostgreSQL DB name
* `POTD_II_POSTGRESQL_DB_USER`: PostgreSQL user
* `POTD_II_POSTGRESQL_DB_PW`: PostgreSQL password

---

* `POTD_II_SITE_DOMAIN`: The domain name, default: `http://www.potd.remote` (change your `hosts` file if needed)
* `THUMBNAIL_MAX_SCRAPE_SIZE`: maximum pixel width or height for Wikimedia image downloads, default: `2400`

Otherwise, a SQLite database (`potd_ii_db.sqlite3` at the project source root) will be created if any PostgreSQL environment variable is missing.

## Changelog

Currently, there is no changelog; the best option at the moment is to read the commit messages.

## License

At this moment, the code is not under a specific license, which means you are **not** allowed to use it
in any way without written permission to do so.

The Python, JavaScript and CSS libraries used are under their respective licenses.

## Acknowledgements

### Authors

Christoph Haunschmidt: Project lead

See `DEVNOTES.md` for the libraries used.

# Development notes

Miscellaneous development notes.

## REST API

Accessible under `/api/v1/`

## `/api/v1/potds/` query filter parameters:
* `start_date`, `end_date`: inclusive, format: `yyyy-mm-dd`
* `before_date`, `after_date`: exclusive, format: `yyyy-mm-dd`
* `source_type`: see `picture_of_the_day.POTD.PICTURE_SOURCE_CHOICES`

Example URL:

    /api/v1/potds/?min_date=2014-03-26&source_type=wikipedia_en&max_date=2017-03-20

## Log files created

Files created in the `logs` directory.

 - `potd_django.log`: general django log data
 - `potd_management.log`: used for "management"-like commands and operations, like scraping a picture of the day
 - `potd_app.log`: for the running webapp

## Used libraries

Links for keeping track of the used libraries.

### Python

See `requirements.txt`.

### CSS

- [Bootstrap 4](https://v4-alpha.getbootstrap.com/)

### JavaScript

- [JQuery](https://jquery.com/)
- [Vue.js](https://vuejs.org): JavaScript Framework
- [marked](https://github.com/chjj/marked): Markdown to HTML, for the Picture of the Day description

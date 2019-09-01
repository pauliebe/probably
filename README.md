# probably

A digital shoebox of Library of Congress images, built during the Spring 2018 [ChiPy mentorship program.](https://chipymentor.org/)

## Get started

`make init`: Installs requirements, downloads necessary nltk modules

`make search`: Searches for a query through the LOC API and saves individual JSON responses in `/json_archive`. Combines responses into `./app/static/json_files/query.json`

`make images`: Checks for image rights on each response in `/json_archive` for the specified query. If the image rights signify the photo is okay to use, it's downloaded to `./app/static/img/`

# MostPoisonedName2020

"Is Hilary still the most poisoned baby name in U.S. history?" In this repo's accompanying [blog post](https://medium.com/@williecostello/is-hilary-still-the-most-poisoned-baby-name-in-u-s-history-133b4a421304) I present a 2020 update of [Hilary Parker](https://twitter.com/hspter)'s classic 2013 blog post and statistical analysis ["Hilary: the most poisoned baby name in US history"](https://hilaryparker.com/2013/01/30/hilary-the-most-poisoned-baby-name-in-us-history/). The answer: No, though the new most poisoned name is probably not what you expect.

Repository contents:

- `mostpoisonedname.ipynb` presents the details of my statistical analysis
- `visualizations.ipynb` shows how I created the blog post's visualizations
- `setup.sh` & `process_data.py` will download and process the raw [baby name data from the Social Security Administration](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data), allowing you to reproduce my work and explore the data for yourself
- `app.py`, `app_setup.sh`, `requirements.txt`, `Procfile` are used for the accompanying [Baby Name Popularity Explorer app](https://baby-name-popularity.herokuapp.com/)
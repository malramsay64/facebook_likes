Facebook Likes
==============

This is a script to scrape the number of likes from a collection of Facebook pages.
The data is parsed from all pages listed in a google doc, 
see [this example page][facebook_likes] for an example.

Installation and Use
------------

Installation requires python 3.6 in addition to [pipenv][].
With the requirements installed collecting the likes can be done with

```shell
$ pipenv run ./get_likes.py
```

which will generate a `likes_data.h5` file in the directory.
Any time you run the above command, data will be append to the `likes_data.h5` file.

To create figures from the resulting data use the command

```shell
$ pipenv run python create_figures.py
```

which will generate a series of html files which you can view in any web browser.


[facebook_likes]: https://docs.google.com/spreadsheets/d/1WsobPIzZRRGompWYk3dPEzanlicFTwUaqRBIB5iUOVU/edit?usp=sharing
[pipenv]: https://docs.pipenv.org/

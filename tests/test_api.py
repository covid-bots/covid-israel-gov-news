import sys
import os
import json
import datetime
import typing
from bs4 import BeautifulSoup

from modules import NewsArticle


class TestNewsArticleModule:

    __ARTICLES = None
    __THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    __JSON_CONFIG_FILEPATH = os.path.join(__THIS_DIR, 'articles_db.json')
    __ARTICLES_FOLDER = os.path.join(__THIS_DIR, 'resources')

    @classmethod
    def _get_articles(cls,) -> typing.List[dict]:
        """ Returns a list of dictionaries. Each dictionary in the list represents
        an articles from the `resources` folder, when the keys to each dictionray
        are:

        *   `content`: the html content, as a string
        *   `expected`: a dictionary loaded directly from the json configurations
                        file, that saves all of the expected properties of the
                        api from the article instance.
        """

        if cls.__ARTICLES is None:
            # If articles are not loaded yet, loads them!

            # load the configuration file
            with open(cls.__JSON_CONFIG_FILEPATH, encoding='utf8') as open_file:
                cls.__ARTICLES = json.load(open_file)

            # load each file specified in the configuration file
            for article_config in cls.__ARTICLES:

                # generate the path to the current article file
                filepath = os.path.join(
                    cls.__ARTICLES_FOLDER, article_config['filename'])

                # open the article, and save the data in the dictionray
                with open(filepath, 'r', encoding='utf8') as open_file:

                    # read raw html file
                    content = open_file.read()

                    # convert html to NewsArticle instance
                    article_config['article'] = NewsArticle(
                        data=BeautifulSoup(content, 'lxml')
                    )

        return cls.__ARTICLES

    def test_title_property(self,):
        for article in self._get_articles():
            title = article['article'].title
            expected = article['expected']['title']
            assert title == expected

    def test_subtitle_property(self,):
        for article in self._get_articles():
            subtitle = article['article'].subtitle
            expected = article['expected']['subtitle']
            assert subtitle == expected

    def test_subject_property(self,):
        for article in self._get_articles():
            subject = article['article'].subject
            expected = article['expected']['subject']
            assert subject == expected

    def test_subsubjects_property(self,):
        for article in self._get_articles():
            subsubjects = article['article'].subsubjects
            expected = article['expected']['subsubjects']
            assert subsubjects == expected

    def test_posted_string_property(self,):
        for article in self._get_articles():
            posted_string = article['article'].posted_string
            expected = article['expected']['posted_string']
            assert posted_string == expected

    def test_posted_date_property(self,):
        for article in self._get_articles():
            posted_date = article['article'].posted_date
            assert isinstance(posted_date, datetime.date)

    def test_content_property(self,):
        for article in self._get_articles():
            content = article['article'].content
            expected = '\n'.join(article['expected']['content_lines'])
            assert content == expected

    def test_content_lines_property(self,):
        for article in self._get_articles():
            content = article['article'].content_lines
            expected = article['expected']['content_lines']
            assert content == expected

    def test_attached_files_property(self,):
        for article in self._get_articles():
            attached_files = article['article'].attached_files
            expected = article['expected']['attached_files']
            assert attached_files == expected

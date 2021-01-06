import os
import json
import datetime
import typing

from modules import NewsArticle


class TestNewsArticleModule:

    __ARTICLES = None
    __THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    __JSON_CONFIG_FILEPATH = os.path.join(__THIS_DIR, 'articles_db.json')
    __JSON_ARTICLES_DATA = os.path.join(__THIS_DIR, 'test_news_api.json')

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

            # loads the template api json file
            with open(cls.__JSON_ARTICLES_DATA, encoding='utf8') as open_file:
                articles_data = json.load(open_file)['results']

            # load the configuration file
            with open(cls.__JSON_CONFIG_FILEPATH, encoding='utf8') as open_file:
                cls.__ARTICLES = json.load(open_file)

            # load each file specified in the configuration file
            for article_config in cls.__ARTICLES:

                cur_article_data = articles_data[article_config['index']]
                article_config['article'] = NewsArticle(cur_article_data)

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

    def test_subjects_property(self,):
        for article in self._get_articles():
            subjects = article['article'].subjects
            expected = article['expected']['subjects']
            assert subjects == expected

    def test_subsubjects_property(self,):
        for article in self._get_articles():
            subsubjects = article['article'].subsubjects
            expected = article['expected']['subsubjects']
            assert subsubjects == expected

    def test_date_properties(self,):
        for article in self._get_articles():
            assert isinstance(article['article'].publish_date, datetime.date)
            assert isinstance(article['article'].update_date, datetime.date)

    def test_content_sentences_property(self,):
        for article in self._get_articles():
            content = article['article'].content_sentences
            expected = article['expected']['content_sentences']
            assert content == expected

    def test_type_property(self,):
        for article in self._get_articles():
            type = article['article'].type
            expected = article['expected']['type']
            assert type == expected

    def test_content_properties(self,):
        for article in self._get_articles():
            assert article['article'].content_html
            assert article['article'].content_text
            assert isinstance(article['article'].content_html, str)
            assert isinstance(article['article'].content_text, str)

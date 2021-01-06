"""
In this file, you will find the modules that are used in this project.
There are two main modules:
1.  The `NewsArticle` module - represents a single news article
2.  The `GovIlNews` module - represents the whole gov website. Methods can
    'pull' articles from the website, and return them as `NewsArticle` instances.
"""

import typing
import datetime
import requests
from bs4 import BeautifulSoup


class BaseModule:
    """ The base module in the project. """


class NewsArticle(BaseModule):
    """ An object that represents articles in the `gov.il` website.
    An example article can be found in https://www.gov.il/he/departments/news/03012021-03
    """

    def __init__(self, data: dict):
        self.__data = data

    @property
    def title(self,) -> str:
        """ The title of the article, as a string. """
        return self.__data['Title']

    @property
    def subtitle(self,) -> str:
        """ The subtitle (description) of the article, as a string. """
        return self.__data['Description']

    @property
    def subjects(self,) -> typing.List[str]:
        """ The list of the main subjects of the article. A list of strings. """
        return [topic_data['Title'] for topic_data in self.__data['ConnectedTopics']]

    @property
    def subsubjects(self,) -> typing.List[str]:
        """ A list of the 'sub-subjects' of the article. Each element in the list
        is a string. """
        return [topic_data['Title'] for topic_data in self.__data['ConnectedSubTopics']]

    @property
    def publish_date(self,) -> datetime.datetime:
        """ The date the article was posted on, as a `datatime` instance. """
        date_iso = self.__data['PublishDate']
        return datetime.datetime.fromisoformat(date_iso)

    @property
    def update_date(self,) -> datetime.datetime:
        """ The date the article was updated on, as a `datetime` instance. """
        date_iso = self.__data['UpdateDate']
        return datetime.datetime.fromisoformat(date_iso)

    @property
    def content_html(self,) -> str:
        """ Returns the content of the article, in the html format (raw
        from the API). """
        return self.__data['Content']

    @property
    def content_text(self,) -> str:
        """ Returns the content of the article (text only). """
        soup = BeautifulSoup(self.content_html, 'lxml')
        return soup.get_text()

    @property
    def content_sentences(self,) -> typing.List[str]:
        """ Returns the content of the article, represented as a list
        of sentences (list of strings). """

        lines = self.content_text.split('.')
        return [
            line.strip() + '.'
            for line in lines
            if line.strip()
        ]

    @property
    def type(self,) -> str:
        """ Returns the type of the article. Usually `'news'`. """
        return self.__data['NewsTypeDesc'].lower()


class GovIlNews(BaseModule):
    """ Represents a collection of `NewsArticle` instances. """

    def __init__(self, url: str):
        """ Requests the API data from the given URL, and saves it in memory. """
        response = requests.get(url)
        self._data = response.json()

    def articles(self) -> typing.List[NewsArticle]:
        """ Returns a list of all of the articles in the current news data,
        as `NewsArticle` instances. """
        return [NewsArticle(article_data) for article_data in self._data['results']]

    def latest_article(self) -> NewsArticle:
        """ Returns the last article from the current news data, as a
        `NewsArticle` instance. """
        return NewsArticle(self._data['results'][0])

    @property
    def num_of_articles(self) -> int:
        """ Returns the number of articles in the current news data, as
        an integer. """
        return len(self._data['results'])


class CovidGovIlNews(GovIlNews):
    """ Represents a collection of `NewsArticle` instances that are related
    to Covid19. """

    __API_URL = r'https://www.gov.il/he/api/NewsApi/Index?limit=100&OfficeId=104cb0f4-d65a-4692-b590-94af928c19c0&topic=3ef9cac8-a1a9-4352-91d4-860efd3b720d&skip=0'

    def __init__(self):
        super().__init__(self.__API_URL)

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
    Example article can be found in https://www.gov.il/he/departments/news/03012021-03
    """

    def __init__(self, url: str = None, data: BeautifulSoup = None):
        """ Generates an instance, and saves the url in it. Creating an instance
        doesn't automatically makes a https request (this can be done be calling
        the `request` method). """

        args_count = sum(cur is not None for cur in [data, url])
        if args_count != 1:
            raise ValueError(
                "One argument exactly must be specified - either `data` or `url`")

        self.__url = url

        # when the `request` methond is called,
        # it updates this property and saves in it the
        # `beautiful soup` instance.
        self.__data = data

    def request(self,) -> None:
        """ Makes a http request to the article URL, analyses the data and generates
        the object properties. Returns `None`. """

        if self.__data is not None:
            # make a request only if there is no data.
            return

        response = requests.get(self.__url)
        self.__data = BeautifulSoup(response.content, 'lxml')

    @property
    def title(self,) -> str:
        """ The title of the article, as a string. """
        self.request()
        element = self.__data.find(id='NewsTitle')

        if element is None or not element.text.strip():
            return None

        return element.text.strip()

    @property
    def subtitle(self,) -> str:
        """ The subtitle of the article, as a string. """
        self.request()
        element = self.__data.find(id='NewsDescription')

        if element is None or not element.text.strip():
            return None

        return element.text.strip()

    @property
    def subject(self,) -> str:
        """ The subject of the article, as a string. """
        self.request()
        element = self.__data.find(id='md_content_subject')

        if element is None:
            return None

        return element.text.strip()

    @property
    def subsubjects(self,) -> typing.List[str]:
        """ A list of the 'sub-subjects' of the article. Each element in the list
        is a string. """
        self.request()
        container = self.__data.find(id='md_content_subSubject')

        if container is None:
            return list()

        return [item.text.strip() for item in container.find_all('span')]

    @property
    def posted_string(self,) -> str:
        """ The date the article was posted on, as a string (raw, received
        from the request) """
        self.request()
        return self.__data.find(id='md_content_publishDate').text.strip()

    @property
    def posted_date(self,) -> datetime.date:
        """ A `datetime.date` instance that represents the date that the article
        was posted on. """
        day, month, year = self.posted_string.split('.')
        return datetime.date(day=int(day), month=int(month), year=int(year))

    @property
    def content(self,) -> str:
        """ Returns the content of the article, as a string. """

    @property
    def content_lines(self,) -> typing.List[str]:
        """ Returns the content of the article, represented as a list of sentences
        (list of strings). """

    @property
    def attached_files(self,) -> typing.List[str]:
        """ Returns a list of urls to attached files to the article. If
        there are no files attached, returns an empty list.

        An example of an article with an attached file can be found on:
        https://www.gov.il/he/departments/news/agra_2021 """

        self.request()
        container = self.__data.find(id='divFiles')

        if container is None:
            return list()

        return [item['href'] for item in container.find_all('a', href=True, title=True)]


class GovIlNews(BaseModule):

    ENDPOINT = r'https://www.gov.il/he/departments/news'

    def search(self, skip: int = 0, limit: int = 10, **extra_kwargs) -> typing.List[NewsArticle]:
        """ By default, searches for the most recant 10 articles, and returns
        them in a list, where the first element in the list is the newest article,
        and the 9th is the older one. Use `extra_kwargs` to filter the articles
        by different departments, subjects, and more! """

    def article(self, name: str) -> NewsArticle:
        """ Recives the article name (usually a string that inclues the date
        of the article and some additional numbers), and returns a `NewsArticle`
        instance that represents the article. """

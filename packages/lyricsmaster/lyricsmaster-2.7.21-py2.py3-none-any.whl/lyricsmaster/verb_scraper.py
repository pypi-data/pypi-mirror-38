# -*- coding: utf-8 -*-

"""Main module.

This module defines the Api interface for the various Lyrics providers.
All lyrics providers inherit from the base class LyricsProvider.

"""

# We use abstract methods to ensure that all future classes inheriting from LyricsProvider will
# implement the required methods in order to have a nice and consistent API.
from abc import ABCMeta, abstractmethod

from lyricsmaster.utils import TorController

import re
import urllib3
import certifi
from bs4 import BeautifulSoup, NavigableString
import json

# We use gevent in order to make asynchronous http requests while downloading lyrics.
# It is also used to patch the socket module to use SOCKS5 instead to interface with the Tor controller.
import gevent.monkey
from gevent.pool import Pool
from collections import OrderedDict

# Python 2.7 compatibility
# Works for Python 2 and 3
try:
    from importlib import reload
except ImportError:
    try:
        from imp import reload
    except:
        pass


class VerbProvider:
    """
    This is the base class for all Lyrics Providers. If you wish to subclass this class, you must implement all
    the methods defined in this class to be compatible with the LyricsMaster API.
    Requests to fetch songs are executed asynchronously for better performance.
    Tor anonymisation is provided if tor is installed on the system and a TorController is passed at instance creation.

    :param tor_controller: TorController Object.

    """
    base_url = 'https://conjit.cactus2000.de'
    name = ''

    def __init__(self, tor_controller=None):
        if not self.__socket_is_patched():
            gevent.monkey.patch_socket()
        self.tor_controller = tor_controller
        if not self.tor_controller:
            user_agent = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            self.session = urllib3.PoolManager(maxsize=10,
                                               cert_reqs='CERT_REQUIRED',
                                               ca_certs=certifi.where(),
                                               headers=user_agent)
        else:
            self.session = self.tor_controller.get_tor_session()
        self.__tor_status__()

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__,
                                     self.tor_controller.__repr__())

    def __tor_status__(self):
        """
        Informs the user of the Tor status.

        """
        if not self.tor_controller:
            print(
                'Anonymous requests disabled. The connexion will not be anonymous.')
        elif self.tor_controller and not self.tor_controller.controlport:
            print(
                'Anonymous requests enabled. The Tor circuit will change according to the Tor network defaults.')
        else:
            print(
                'Anonymous requests enabled. The Tor circuit will change for each album.')

    def __socket_is_patched(self):
        """
        Checks if the socket is patched or not.

        :return: bool.
        """
        return gevent.monkey.is_module_patched('socket')

    def get_page(self, url):
        """
        Fetches the supplied url and returns a request object.

        :param url: string.
        :return: urllib3.response.HTTPResponse Object or None.
        """
        if not self.__socket_is_patched():
            gevent.monkey.patch_socket()
        try:
            req = self.session.request('GET', url)
        except Exception as e:
            print(e)
            req = None
            print('Unable to download url ' + url)
        return req

    def get_model_verbs(self):
        """
        Fetches the web page containing the lyrics at the supplied url.

        :param url: string.
            Lyrics url.
        :return: string or None.
            Lyrics's raw html page. None if the lyrics page was not found.
        """
        url = self.base_url + '/index.fr.php'
        raw_html = self.get_page(url).data
        model_verbs_page = BeautifulSoup(raw_html, 'lxml')
        verbs_div = model_verbs_page.find_all('center')[1].find_all('tr')
        model_verbs = {}
        for line in verbs_div:
            for link in line.find_all('a'):
                model_verbs[link.text] = link.attrs['href']
        return model_verbs

    def get_all_verbs(self):
        url = self.base_url + '/index.fr.php'
        raw_html = self.get_page(url).data
        index_page = BeautifulSoup(raw_html, 'lxml')
        alpha_links = index_page.find("p", {'class': 'cent'}).find_all('a')
        verbs = {}
        for link in alpha_links:
            link_url = self.base_url + '/' + link.attrs['href']
            html = self.get_page(link_url).data
            alpha_page = BeautifulSoup(html, 'lxml')
            alpha_div = alpha_page.find("table", {'class': 'alphtab'}).find_all('td')
            for line in alpha_div:
                for link in line.find_all('a'):
                    verbs[link.text] = link.attrs['href']
        return verbs

    def get_verb_info(self, verb, url):
        url = self.base_url + '/' + url
        raw_html = self.get_page(url).data
        verb_page = BeautifulSoup(raw_html, 'lxml')
        conjug_table = verb_page.find("table", {'class': 'conjtab'}).find_all('tr')
        conjug_info = OrderedDict()
        for elmt in conjug_table:
            for tense in elmt.find_all('td'):
                tense_name = tense.find("div").text
                conjug = []
                for content in tense.contents:
                    if isinstance(content, NavigableString):
                        text = str(content)
                        result = text.strip().split(' ', 1)
                        conjug.append(result)
                conjug_info[tense_name] = conjug
        print('The verb {0} has been successfully processed.'.format(verb))
        return conjug_info





if __name__ == "__main__":
    verb_provider = VerbProvider()
    model_verbs = verb_provider.get_model_verbs()
    conjug_model_verbs = {}
    for verb, link in model_verbs.items():
        conjug_model_verbs[verb] = verb_provider.get_verb_info(verb, link)
    with open('model_verbs-it.json', 'w', encoding='utf-8') as file:
        json.dump(conjug_model_verbs, file, ensure_ascii=False, indent='4', sort_keys=True)
    print('All model verbs have been downloaded and saved to disk')

    all_verbs = verb_provider.get_all_verbs()
    conjug_verbs = {}
    for verb, link in all_verbs.items():
        conjug_verbs[verb] = verb_provider.get_verb_info(verb, link)
    with open('all_verbs-it.json', 'w', encoding='utf-8') as file:
        json.dump(conjug_verbs, file, ensure_ascii=False, indent='4', sort_keys=True)
    print('All verbs have been downloaded and saved to disk')
    pass

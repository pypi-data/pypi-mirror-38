# Copyright 2018 Joel Dunham
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""OLD Client --- functionality for connecting to an OLD application.

The primary class defined here is OLDClient. Use it to connect to a
server-side OLD web service.

"""

import codecs
import json
import locale
import sys
from time import sleep
import unicodedata

import requests

from .models import MODELS


# Wrap sys.stdout into a StreamWriter to allow writing unicode.
# This allows piping of unicode output.
# See http://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file
#sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


class Log(object):
    """A simple logger so that print statements can be filtered."""

    def __init__(self, silent=False):
        self.silent = silent

    def debug(self, msg):
        if not self.silent:
            print(u'[DEBUG] %s' % msg)

    def info(self, msg):
        if not self.silent:
            print(u'[INFO] %s' % msg)

    def warn(self, msg):
        if not self.silent:
            print(u'[WARN] %s' % msg)


# The global ``log`` instance can be used instead of ``print`` and output can be
# silenced by setting ``log.silent`` to ``True``.
log = Log()


class OLDClient(object):
    """Create an OLD instance to connect to a live OLD application.

    Basically this is just some OLD-specific conveniences wrapped around
    a requests.Session instance.
    """

    def __init__(self, baseurl):
        self.models = MODELS
        self.baseurl = baseurl
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def login(self, username, password):
        payload = json.dumps({'username': username, 'password': password})
        response = self.session.post('%s/login/authenticate' % self.baseurl,
            data=payload)
        return response.json().get('authenticated', False)

    def get(self, path, params=None, verbose=True):
        response = self.session.get('%s/%s' % (self.baseurl, path),
            params=params)
        return self.return_response(response, verbose=verbose)

    def post(self, path, data=json.dumps({})):
        response = self.session.post('%s/%s' % (self.baseurl, path),
            data=json.dumps(data))
        return self.return_response(response)

    create = post

    def put(self, path, data=json.dumps({})):
        response = self.session.put('%s/%s' % (self.baseurl, path),
            data=json.dumps(data))
        return self.return_response(response)

    update = put

    def delete(self, path, data=json.dumps({})):
        response = self.session.delete('%s/%s' % (self.baseurl, path),
            data=json.dumps(data))
        return self.return_response(response)

    def search(self, path, data):
        response = self.session.request('SEARCH', '%s/%s' % (self.baseurl,
            path), data=json.dumps(data))
        return self.return_response(response)

    def return_response(self, response, verbose=True):
        try:
            return response.json()
        except Exception as e:
            if verbose:
                print('Exception in return_response')
                print(e)
            return response

    def human_readable_seconds(self, seconds):
        return u'%02dm%02ds' % (seconds / 60, seconds % 60)

    def normalize(self, unistr):
        """Return a unistr using canonical decompositional normalization (NFD).
        """
        try:
            return unicodedata.normalize('NFD', unistr)
        except TypeError:
            return unicodedata.normalize('NFD', unicode(unistr))
        except UnicodeDecodeError:
            return unistr

    def poll(self, requester, changing_attr, changing_attr_originally,
             log, wait=2, vocal=True, task_descr='task'):
        """Poll a resource by calling ``requester`` until the value of
        ``changing_attr`` no longer matches ``changing_attr_originally``.
        """
        seconds_elapsed = 0
        while True:
            response = requester()
            if changing_attr_originally != response[changing_attr]:
                if vocal:
                    log.info('Task %s terminated' % task_descr)
                break
            else:
                if vocal:
                    log.info('Waiting for %s to terminate: %s' %
                        (task_descr, self.human_readable_seconds(seconds_elapsed)))
            sleep(wait)
            seconds_elapsed = seconds_elapsed + wait
        return response


def printform(form):
    """Pretty print an OLD form to the terminal."""
    tmp = [('id', form['id'])]
    if form.get('narrow_phonetic_transcription', None):
        tmp.append(('NP', form['narrow_phonetic_transcription']))
    if form.get('phonetic_transcription', None):
        tmp.append(('BP', form['phonetic_transcription']))
    tmp.append(('TR', '%s%s' % (form['grammaticality'], form['transcription'])))
    if form.get('morpheme_break', None):
        tmp.append(('MB', form['morpheme_break']))
    if form.get('morpheme_gloss', None):
        tmp.append(('MG', form['morpheme_gloss']))
    tmp.append(('TL', ', '.join([u'\u2018%s\u2019' % tl['transcription'] for tl
        in form['translations']])))
    if form.get('syntactic_category_string', None):
        tmp.append(('SCS', form['syntactic_category_string']))
    if form.get('break_gloss_category', None):
        tmp.append(('BGC', form['break_gloss_category']))
    if form.get('syntactic_category', None):
        tmp.append(('SC', form['syntactic_category']['name']))
    print(u'\n'.join([u'%-5s%s' % (u'%s:' % t[0], t[1]) for t in tmp]))

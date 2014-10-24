"""
Copyright (c) 2014, Myles Braithwaite <me@mylesbraithwaite.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the
  distribution.

* Neither the name of the Monkey in your Soul nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import os
import glob
import json
import textwrap
import datetime
from hashlib import md5
from collections import OrderedDict

from pytz import timezone
from tzlocal import get_localzone

class Weather(object):
    
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return "%s.%s()" % (self.__module__, self.__class__.__name__)

class Audio(object):
    
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return "%s.%s()" % (self.__module__, self.__class__.__name__)
    
    @property
    def avg(self):
        return self.data.get('avg', None)
    
    @property
    def peak(self):
        return self.data.get('peak', None)

class Placemark(object):
    
    def __init__(self, data):
        self.data = data

class Location(object):
    
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return "%s.%s()" % (self.__module__, self.__class__.__name__)
    
    @property
    def placemark(self):
        if self.data.get('placemark', None):
            return Placemark(self.data.get('placemark'))
        else:
            return None

class Response(object):
    
    def __init__(self, data):
        self.data = data
        
        if self.tokens:
            self.type = 'token'
        elif self.answered_options:
            self.type = 'answer'
        elif self.location_response:
            self.type = 'location'
        elif self.numeric_response:
            self.type = 'numeric'
        elif self.text_response:
            self.type = 'text'
        else:
            self.type = None
    
    def __repr__(self):
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, textwrap.wrap(self.question))
    
    @property
    def question(self):
        return self.data.get('questionPrompt', None)
    
    @property
    def anwser(self):
        if self.tokens:
            return self.tokens
        elif self.answered_options:
            return self.answered_options
        elif self.location_response:
            return self.location_response
        elif self.numeric_response:
            return self.numeric_response
        elif self.text_response:
            return self.text_response
        else:
            return None
    
    @property
    def answered_options(self):
        return self.data.get('answeredOptions', None)
    
    @property
    def location_response(self):
        return self.data.get('locationResponse', None)
    
    @property
    def tokens(self):
        return self.data.get('tokens', None)
    
    @property
    def numeric_response(self):
        return self.data.get('numericResponse', None)
    
    @property
    def text_response(self):
        return self.data.get('textResponse', None)
    
    @property
    def md5(self):
        return md5(self.question).hexdigest()

class Question(object):
    
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, textwrap.wrap(self.prompt))
    
    @property
    def prompt(self):
        return self.data.get('prompt', None)
    
    @property
    def placeholder_string(self):
        return self.data.get('placeholderString', None)
    
    @property
    def allow_multiple_selection(self):
        return self.data.get('allowMultipleSelection', None)
    
    @property
    def md5(self):
        return md5(self.prompt).hexdigest()

class Snapshot(object):
    
    def __init__(self, data):
        self.data = data
    
    def __repr__(self):
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, self.date.isoformat())
    
    @property
    def battery(self):
        if self.data.get('battery', None):
            return self.data.get('battery') * 100
        else:
            return None
    
    @property
    def location(self):
        if self.data.get('location', None):
            return Location(self.data.get('location'))
        else:
            return None
    
    @property
    def steps(self):
        return self.data.get('steps', None)
    
    @property
    def date(self):
        return self.data.get('date', None)
    
    @property
    def audio(self):
        if self.data.get('audio', None):
            return Audio(self.data.get('audio'))
        else:
            return
    
    @property
    def sync(self):
        return bool(self.data.get('sync', None))
    
    @property
    def connection(self):
        return self.data.get('connection', None)
    
    @property
    def connection_text(self):
        return_text = {
            0: u"Device is connected via cellular network",
            1: u"Device is connected via WiFi",
            2: u"Device is not connected"
        }
    
    @property
    def background(self):
        return self.data.get('background', None)
    
    @property
    def dwell_status(self):
        return self.data.get('dwellStatus', None)
    
    @property
    def draft(self):
        return self.data.get('draft', None)
    
    @property
    def weather(self):
        if self.data.get('weather', None):
            return Weather(self.data.get('weather'))
        else:
            return None
    
    @property
    def report_impetus(self):
        return self.data.get('reportImpetus', None)
    
    @property
    def report_impetus_text(self):
        return_text = {
            0: u"Report button tapped",
            1: u"Report button tapped while Reporter is asleep",
            2: u"Report triggered by notification",
            3: u"Report triggered by setting app to sleep",
            4: u"Report triggered by waking up app"
        }
        
        return return_text[self.report_impetus]
    
    @property
    def responses(self):
        responses = []
        
        for r in self.data.get('responses', []):
            responses += [Response(r),]
        
        return responses

class Export(object):
    
    def __init__(self, date, data):
        self.date = date
        self.data = data
    
    def __repr__(self):
        return "%s.%s(%s)" % (self.__module__, self.__class__.__name__, self.date.isoformat())
    
    @property
    def snapshots(self):
        snapshots = []
        
        for s in self.data.get('snapshots', []):
            snapshots += [Snapshot(s),]
        
        return snapshots
    
    @property
    def questions(self):
        questions = []
        
        for q in self.data.get('questions', []):
            questions += [Question(q),]
        
        return questions

class ReporterApp(object):
    
    def __init__(self, directory):
        self.directory = directory
        self.exprots = []
    
    def __repr__(self):
        return "%s.%s()" % (self.__module__, self.__class__.__name__)
    
    def export_files(self):
        return glob.glob(os.path.join(self.directory, "*-repoter-export.json"))
    
    def load_file(self, export):
        filename = os.path.basename(export)
        date = filename.strip('-reporter-export.json')
        
        with open(export, 'r') as f:
            data = json.loads(f.read())
        
        return [Export(date, data)]
    
    def all(self):
        for export in self.export_files():
            self.exports += [load_file(export),]
        
        self.exports.sort(key=lambda e: e.date, reverse=True)
    
    def get(self, date):
        path = os.path.join(self.directory, "%s-repoter-export.json" % date.isoformat())
        
        self.exports = [load_file(path),]
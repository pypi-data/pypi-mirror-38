# Copyright 2018 Deep Air. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""general tools"""
from __future__ import print_function
from __future__ import absolute_import

import time
import json
import datetime
from datetime import timedelta, date


def daterange(s_date, e_date):
    '''
        To return a list of all the dates from
        start date to end date (excluding end date)
        input :
            s_date     : start date (datetime)
            e_date     : end date (datetime)
        returns :
            list of dates
    '''
    for n in range(int((e_date - s_date).days)):
        yield s_date + timedelta(n)


def log(message):
    '''
        prints message on console
        input :
            message     : msg to print (string)
    '''
    print('[' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']:'
          + message)


def get_data(path):
    '''
        Single file loader function
        input :
            path     : abs path to load from (string)
    '''

    try:
        df = pd.read_csv(path)
        return df
    except:
        log('error: No file name ' + path)


def jsonReader(path):
    '''
        JSON File Reader (from absolute path).
        Args:
            path   : absolute path of json file (string)
        Return:
            data   : loaded JSON
    '''
    with open(path) as json_data_file:
        data = json.load(json_data_file)
    return data


def jsonWriter(data, path):
    '''
        JSON File Writer (to absolute path).
        Args:
            data   : data to write (JSON/DICT/STRING)
            path   : absolute path of json file (string)
    '''
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def ddmmyyyy2datetime(start_date):
    '''
        Convert dd-mm-yyyy to std data time format.
        Args:
            start_date   : date with dd-mm-yyyy (string)
        Return:
            date   : converted format
    '''
    str_date = start_date.split('-')
    return date(int(str_date[2]), int(str_date[1]), int(str_date[0]))

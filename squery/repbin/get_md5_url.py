# -*-coding:utf-8-*-
# !/usr/bin/env python
# Author           :               Jiucheng
# Email            :        chenjiucheng@1gene.com.com
# Last modified    :        
# Description      :        
# update      	   :               2017/5/26     

import hashlib
import requests
# import logging
from retrying import retry
import fire


# logging.basicConfig(filename = 'md5.log', level = logging.INFO, format = '%(asctime)s %(message)s',
#     datefmt = '%m/%d/%Y %I:%M:%S %p')

def lazy_property(func):
    name = '_lazy_' + func.__name__

    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value

    return lazy


class SampleInfo(object):
    """
    Get sample information from url:"http://medicine.1gene.com.cn/v1/api/reportInfo"
    """

    def __init__(self, sample_id):
        self.num = 0
        self.id = sample_id
        # self.md5 = self.get_md5()
  #      self.data = self.get_data()

    @lazy_property
    def get_md5(self, key = 'JZIn1cr75aE0dag1gene'):
        def md5_code(string):
            return hashlib.md5(str(string).encode('utf-8')).hexdigest()

        key_md5 = md5_code(key)
        id_md5 = md5_code(self.id)
        url_md5 = key_md5 + id_md5
        return md5_code(url_md5)

    @lazy_property
    @retry(stop_max_attempt_number = 5, wait_fixed = 5000)
    def data(self):
        url = 'http://medicine.1gene.com.cn/v1/api/reportInfo'
        params = {'id': self.id, 'signature': self.get_md5}
        try:
            resp = requests.get(url, params)
        except requests.exceptions.ConnectionError as e:
            self.num += 1
            raise ValueError('Connection timeout %d times. Wrong info: {!r%}'.format(self.num, e))
            # logging.error('Connection timeout %d times. Wrong info: {!r%}'.format(self.num, e))
        else:
            return resp.json()


if __name__ == '__main__':
    fire.Fire(SampleInfo)

# a = SampleInfo('OG175710801')

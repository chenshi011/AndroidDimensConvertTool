#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
import ConfigParser


class Config():
    def __init__(self, path):
        self.DEBUG = False
        self.path = path
        self.cf = ConfigParser.ConfigParser()
    def get(self, field, key, defval=''):
        result = defval
        try:
            if self.cf.has_option(field, key):
                result = self.cf.get(field, key)
            else:
                self.set(field, key, defval)
                if self.DEBUG:
                    print "field:%s key:%s not find" % (field, key)
        except:
            self.write_config(field, key, defval)
            if self.DEBUG:
                print "field:%s key:%s not find" % (field, key)
        return result
    def set(self, field, key, value):
        try:
            if self.cf.has_option(field, key):
                self.cf.read(self.path)
            elif not self.cf.has_section(field):
                self.cf.add_section(field)
            self.cf.set(field, key, value)
            with open(self.path,'w+') as fp:
                self.cf.write(fp)
        except:
            if self.DEBUG:
                print "write_config field:%s key:%s failed " % (field, key)
            return False
        return True

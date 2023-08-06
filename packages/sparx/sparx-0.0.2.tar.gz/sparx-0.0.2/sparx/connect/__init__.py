"""
    Module: Data Preprocessing Models
    Project: Sparx
    Authors: Bastin Robins. J
    Email : robin@cleverinsight.com
"""
import requests
import pandas as pd
import numpy as np


class Mysql(object):
    ''' Mysql class which can connect with mysql database
    and start a streaming data fetch
    '''
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = port
        self.password = password

    def connect(self):
        ''' Establish an connection to Mongo Instance and return
        '''
        return self.host

    def exit(self):
        ''' Simple way to disconnect '''
        pass



class Mongo(object):
    ''' Connector class for MongoDb instance to make query fetch
    easy
    '''
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password



    def connect(self):
        ''' Establish an connection to Mongo Instance and return
        '''
        pass

    def exit(self):
        ''' Simple way to disconnect '''
        pass


class Facebook(object):
    ''' Facebook API access using class which can simplify the
    `GET`, `POST`, `DELETE`, `PUT` requests '''

    def __init__(self, auth_token, auth_key):
        self.auth_token = auth_token
        self.auth_key = auth_key

    def connect(self):
        ''' Establish an connection to Mongo Instance and return
        '''
        return self.auth_token

    def exit(self):
        ''' Simple way to disconnect '''
        pass


class Twitter(object):
    ''' Twitter API access using class which can simplify the
    `GET`, `POST`, `DELETE`, `PUT` requests '''

    def __init__(self, auth_token, auth_key):
        self.auth_token = auth_token
        self.auth_key = auth_key

    def connect(self):
        ''' Establish an connection to Mongo Instance and return
        '''
        pass

    def exit(self):
        ''' Simple way to disconnect '''
        pass

    def fetch(self, hashtag):


        return tweets




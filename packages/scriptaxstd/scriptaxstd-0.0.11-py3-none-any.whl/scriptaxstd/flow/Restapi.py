import json
from commandtax.flow.Connector import Connector
import ast


class RestApi:
    def makeCmd(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = '--url ' + url

        if dataPost:
            command += " --data-post '" + json.dumps(ast.literal_eval(dataPost)) + "'"

        if dataHeader:
            command += " --data-header '" + json.dumps(ast.literal_eval(dataHeader)) + "'"

        if dataQuery:
            command += " --data-query '" + json.dumps(ast.literal_eval(dataQuery)) + "'"

        if dataPath:
            command += " --data-path '" + json.dumps(ast.literal_eval(dataPath)) + "'"

        return command

    # Arbitrary JSON API Calls

    def jget(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --get ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def jpost(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --post ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def jput(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --put ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def jpatch(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --patch ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def jdelete(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --delete ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    # Arbitrary XML API Calls

    def xget(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'apixml --get ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def xpost(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'apixml --post ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def xput(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'apixml --put ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def xpatch(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'apixml --patch ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def xdelete(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'apixml --delete ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    # Arbitrary XML API Calls

    def dget(self, apiDriver, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = apiDriver + ' --get ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def dpost(self, apiDriver, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = apiDriver + ' --post ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        print(command)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def dput(self, apiDriver, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = apiDriver + ' --put ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def dpatch(self, apiDriver, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = apiDriver + ' --patch ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def ddelete(self, apiDriver, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = apiDriver + ' --delete ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()


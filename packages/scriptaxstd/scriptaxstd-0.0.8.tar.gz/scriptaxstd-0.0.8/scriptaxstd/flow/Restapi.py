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

    def get(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --get ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def post(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --post ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def put(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --put ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def patch(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --patch ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

    def delete(self, url, dataPost=None, dataHeader=None, dataQuery=None, dataPath=None):
        command = 'api --delete ' + self.makeCmd(url, dataPost, dataHeader, dataQuery, dataPath)
        c = Connector(command=command)
        return c.execute().getResponseBody()

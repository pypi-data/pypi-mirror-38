from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from commandtax.models.Command import Command
from scriptax.drivers.builtin.Scriptax import Scriptax
from scriptaxstd.flow.Delegator import Delegator
from apitaxcore.utilities.Files import getPath


class StandardLibrary(Scriptax):
    def isDriverCommandable(self) -> bool:
        return True

    def getDriverName(self) -> str:
        return 'std'

    def getDriverDescription(self) -> str:
        return 'Provides a standard library for Scriptax'

    def getDriverHelpEndpoint(self) -> str:
        return 'coming soon'

    def getDriverTips(self) -> str:
        return 'coming soon'

    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        response = ApitaxResponse()
        try:
            delegator = Delegator(command)
            result = delegator.delegate()
            response.body.add({'result': result})
            response.status = 200
            return response
        except:
            return response.res_server_error(body={"message": "StandardLibrary@HandleDriverCommand exception."})

    def getDriverScript(self, path) -> str:
        path = getPath(__file__ + '/../../../scriptax/' + path)
        with open(path, 'r') as myfile:
            data = myfile.read().replace('\n', '')
        return data



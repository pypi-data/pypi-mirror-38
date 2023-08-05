# Application import
from scriptax.parser.utils.BoilerPlate import customizableParser
from scriptax.drivers.builtin.Scriptax import Scriptax
from commandtax.drivers.builtin.Commandtax import Commandtax
from scriptaxstd.drivers.builtin.StandardLibrary import StandardLibrary
from scriptaxstd.drivers.builtin.Api import Api
from scriptaxstd.drivers.builtin.ApiXml import ApiXml

from apitaxcore.logs.Log import Log
from apitaxcore.logs.StandardLog import StandardLog
from apitaxcore.models.State import State
from apitaxcore.flow.LoadedDrivers import LoadedDrivers
from apitaxcore.drivers.Drivers import Drivers

from apitaxcore.models.Options import Options

State.log = Log(StandardLog(), logColorize=False)

State.log.log("> test")
State.log.log("")

Drivers.add("commandtax", Commandtax())
Drivers.add("scriptax", Scriptax())
Drivers.add("std", StandardLibrary())
Drivers.add("api", Api())
Drivers.add("apixml", ApiXml())
LoadedDrivers.load("commandtax")
LoadedDrivers.load("scriptax")
LoadedDrivers.load("std")
LoadedDrivers.load("api")
LoadedDrivers.load("apixml")

#scriptax = "from std import String as stdstr; log(stdstr.substr(text='this_is_some_fantastic_text', start=3, length=10));"
#scriptax = "from std import Map as map; mymap = new map(); mymap.map.test = 'wtf'; mymap.map.bob = 'yes'; mymap.map.shawn = {'noway': 'yesway'}; log(mymap.has(key='noway', sMap=mymap.map.shawn)); return 'test complete';"
#scriptax = "from std import Restapi as stdapi; mydata = {}; mydata.title = 'awesome'; mydata.body='shawn is'; mydata.id=5; log(stdapi.jget(endp='https://jsonplaceholder.typicode.com/posts')); log(stdapi.jpost(endp='https://jsonplaceholder.typicode.com/posts', dataPost=mydata)); return 'test complete';"
#scriptax = "from std import Restapi as stdapi; mydata = {}; mydata.title = 'awesome'; mydata.body='shawn is'; mydata.id=555; log(stdapi.jpost(endp='https://jsonplaceholder.typicode.com/posts', dataPost=mydata)); return 'test complete';"
#scriptax = "from std import Restapi(debug=true) as stdapi; mydata = {}; mydata.title = 'awesome'; mydata.body='shawn is'; mydata.id=555; log(stdapi.dpost(driver='api',endp='https://jsonplaceholder.typicode.com/posts', dataPost=mydata)); return 'test complete';"
#scriptax = "from std import Json as stdjson; mydata = {}; mydata.title = 'awesome'; mydata.body='shawn is'; mydata.id=555; log(mydata); log(stdjson.toJson(obj=mydata)); log(ct('api --url https://jsonplaceholder.typicode.com/posts --post --data-post \\\'' + stdjson.toJson(obj=mydata) + '\\\''));"

#scriptax = "from std import Restapi(debug=true) as stdapi; mydata = {}; mydata.title = 'awesome'; mydata.body='shawn is'; mydata.id=555; mydata.something = {}; mydata.somnething={\"address\":\"address\",\"city\":\"Regina\",\"email\":\"selectedClinicId@regina.ca\",\"extra\":{},\"fax\":\"123456789\",\"name\":\"Tristans Legit Clinic\",\"phone_number\":\"987654321\",\"province\":\"Saskatchewan\"}; log(mydata); log(stdapi.dpost(driver='api',endp='https://jsonplaceholder.typicode.com/posts', dataPost=mydata)); return 'test complete';"

scriptax = "from std import Json as stdjson; from std import Restapi(debug=true) as stdapi; mydata={\"address\":\"address\",\"city\":\"Regina\",\"email\":\"selectedClinicId@regina.ca\",\"extra\":{},\"fax\":\"123456789\",\"name\":\"Tristans Legit Clinic\",\"phone_number\":\"987654321\",\"province\":\"Saskatchewan\"}; log(mydata); log(ct('api --url https://jsonplaceholder.typicode.com/posts --post --data-post \\\'' + stdjson.toJson(obj=mydata) + '\\\''));"

visitor = customizableParser(scriptax, file='inline_program', options=Options(debug=True))

print('Return: ' + str(visitor[0][1]))
print()
print("===")

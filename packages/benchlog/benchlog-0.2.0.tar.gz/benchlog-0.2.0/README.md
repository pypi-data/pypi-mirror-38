# Benchlog Package

Benchlog allows a user to record the runtime and resource allocation of their program overtime.

### Version 0.1
This version allows you to send data to a server or store the log file locally to the machine. It overwrites the last file saved at the moment.

## Installation
`pip install benchlog`

## Use
### Benchlog Arguments
| Argument  | Type | Description |
|---|---|---|
| projectname  | string  | The name of your project |
|  iterationNum | integer  | Number of iteration your code uses (Used to record progress)|
|  Opt: featureList | [string] | Record list of features used for project |
|  Opt: quiet | integer | Set to 1 to disable logging, default: 0  |

### Setup
1. Declare new instance of BenchLog
E.g. `logging = BenchLog('Test Project', 1024, ['tensorflow', 'featureB'], quiet1]`

2. **Optional:** Declare a host to send the telemetry data to. If no host is stored or data fails to send we will store the data in a file called `telemetry.json` in the directory of the project.
E.g `logging.setHost('http://localhost:3000')`

3. Start logging by calling `logging.start()`
4. Call `logging.log(iterationNum)` every once in awhile to log progress.
5. End logging by calling `logging.end()`

### Example Code

```
logging = BenchLog('My Project', 10000, ['FeatureA','FeatureB'])
logging.setHost('http://localhost:3000')
array = []
test.start()
for i in range(1,10000):
    if(i % 1000 == 0):
        #Do Something here
        test.log(i)
logging.end()
```

### Example telemetry output
```
{"cores":"4","runTime":"1.506113","size":"10000","features":["testa","testb"],"projectName":"test","infoRunTime":["0.177929","0.345282","0.511437","0.685919","0.850231","1.011178","1.182584","1.345929","1.505748","1.506086"],"infoCpuUsage":["13.2","32.4","30.3","35.7","30.8","28.1","36.2","26.2","28.1","0.0"],"infoMemoryUsage":["452567040","852570112","1252573184","1652576256","2052579328","2452582400","2852585472","3252588544","3652591616","3652591616"],"infoProgress":["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"]}
```

## Future To Do
- [ ] Do not overwrite old telemetry data
- [ ] GPU Utilization
- [ ] Local Visualization
- [ ] Web UI to view results
- [ ] Server
- [ ] Change progress to 0-100

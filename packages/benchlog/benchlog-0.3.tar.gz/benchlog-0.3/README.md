# Benchlog Package

Benchlog allows a user to record the runtime and resource allocation of their program overtime.

# Changelog
## Version 0.3
### Features
- Added logging of accuracy
- Added unique filename generation (using date and time)
- [Documentation] Added a changelog
- Allow local saving and sending to server with `setHost(HOST, local)`
- Added GPU logging of usage, memory, memory utilization, gpu UUID and name with `enableGPU()`
- Prevent users that do not have 'nvidia-smi' installed from enabling GPU

### Bug Fixes
- Fixed bug where sendData would only save to telemetry.json on error instead of calling `saveData`
- Prevented user from calling `end()` without calling `start()`
- Prevented user from calling `end()` twice
- Call for variable `deviceID` did not exist in `enableGPU()`, use `self.gpuObj` instead
- Fixed bug where we called `saveData()` instead of `self.saveData()`

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
1. Import BenchLog
`from benchlog import BenchLog`

2. Declare new instance of BenchLog
E.g. `logging = BenchLog('Test Project', 1024, ['tensorflow', 'featureB'], quiet1]`

3. **Optional:** Declare a host to send the telemetry data to. If no host is stored or data fails to send we will store the data in a file called `telemetry.json` in the directory of the project. If you would like to enable local and external logging, set the second argument to 1.
setHost(ipaddress, [OPTIONAL:1 to enable local logging, 0 default])
E.g `logging.setHost('http://localhost:3000',1)`

4. **Optional:** GPU Logging - Enable GPU Logging by calling `logging.enableGPU()` If you have more than one GPU refer to the enableGPU section

4. Start logging by calling `logging.start()`
5. Call `logging.log(iterationNum)` every once in awhile to log progress.
6. End logging by calling `logging.end()`

### Example Code

```
from benchlog import BenchLog
logging = BenchLog('My Project', 10000, ['FeatureA','FeatureB'])
logging.setHost('http://localhost:3000')
array =
logging.enableGPU(0)
logging.start()
for i in range(1,10000):
    if(i % 1000 == 0):
        #Do Something here
        logging.log(i)
logging.end()
```

### enableGPU()
`logging.enableGPU()` uses `GPUtil` in order to gather gpu information. This will only work with Nvidia GPUs.

If you have **multiple GPUs** you can pass in the index of the GPU you want to use. You can find which GPU you want to log by calling nvidia-smi and returning the GPU you want to use. E.g `logging.enableGPU(1)`

GPU logging records three things.

`GpuMemUsage` - This is the amount of memory being used by the GPU
`GpuMemUtil` - This is the memory activity (i/o) within GPU memory
`GpuUsage` - This is the standard gpu load

### Example telemetry output
```
{"cores":"4","runTime":"1.506113","size":"10000","features":["testa","testb"],"projectName":"test","infoRunTime":["0.177929","0.345282","0.511437","0.685919","0.850231","1.011178","1.182584","1.345929","1.505748","1.506086"],"infoCpuUsage":["13.2","32.4","30.3","35.7","30.8","28.1","36.2","26.2","28.1","0.0"],"infoMemoryUsage":["452567040","852570112","1252573184","1652576256","2052579328","2452582400","2852585472","3252588544","3652591616","3652591616"],"infoProgress":["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"]}
```

## Future To Do
- [X] Do not overwrite old telemetry data
- [X] GPU Utilization
- [ ] Local Visualization
- [ ] Web UI to view results
- [ ] Server
- [X] Change progress to 0-100

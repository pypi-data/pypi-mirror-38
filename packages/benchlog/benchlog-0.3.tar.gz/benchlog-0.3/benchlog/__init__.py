from datetime import datetime
import psutil
import requests
import json
import os
import multiprocessing
import subprocess
import time

class BenchLog:
    def __init__(self, projectName, projectSize, projectFeatures=[], quiet=0):
        if not (quiet == 1):
            print('[Project Initialized]')
            print('Project Name: %s, ProjectSize: %d' % (projectName, projectSize))
        self.projectName = projectName
        self.startTime = -1
        self.endTime = -1
        self.runTime = -1
        self.size = projectSize
        self.features = projectFeatures
        self.infoRunTime = []
        self.infoProgress = []
        self.infoMemoryUsage = []
        self.infoCpuUsage = []
        self.infoGpuUsage = []
        self.infoGpuMemUtil = []
        self.infoGpuMemUsage = []
        self.gpuLogging = 0
        self.gpuName = ''
        self.gpuMaxMem = -1
        self.gpuDriver = -1
        self.gpuUUID = -1
        self.filename = ''
        self.gpuObj = None
        self.gpuID = -1
        self.cores = multiprocessing.cpu_count()
        self.process = psutil.Process(os.getpid())
        self.host = 'N/A'
        self.local
        self.quiet = quiet
    def enableGPU(self, gpuID=-1):
        import GPUtil
        try:
            if(gpuID == -1):
                gpuID = 0
                print('No gpuID selected, selecting GPU 0')
            self.gpuObj = GPUtil.getGPUs()
            if(gpuID+1 > len(self.gpuObj)):
                print('[Error]')
                print('Device ID is not available')
                return
            else:
                self.gpuLogging = 1
                self.gpuID = gpuID
                self.gpuName = self.gpuObj[gpuID].name
                self.gpuMaxMem = self.gpuObj[gpuID].memoryTotal
                self.gpuDriver = self.gpuObj[gpuID].driver
                self.gpuUUID = self.gpuObj[gpuID].uuid
                if not (self.quiet == 1):
                    print('[GPU Logging Initialized]')
                    print('Logging gpuID %d, GPU: %s' % (gpuID, self.gpuName))
        except Exception as e:
            self.gpuLogging = -1;
            if not (self.quiet == 1):
                print('[ERROR]')
                print('Error enabling GPU logging. Is Nvidia GPU or nvidia-smi installed?')
                print(e)
            return
    def setHost(self, host, local=-1):
        if not (self.quiet == 1):
            print('Host set to ', host)
        self.host = host
        self.local = local
        return
    def start(self):
        if not (self.quiet == 1):
            print('[Benchmark Start]')
        self.startTime = datetime.now()
        return
    def end(self, accuracy=-1):
        if(self.startTime == -1):
            print('[ERROR]')
            print('The project has not been started, please call start()')
            return
        if (self.endTime == -1):
            print('[ERROR]')
            print('You may not call end() twice, the project has been recorded to ', self.filename)
            self.log(self.size)
            self.endTime = datetime.now()
            self.runTime = self.endTime - self.startTime
        if not (self.quiet == 1):
            print('[Benchmark End]')
            print('Runtime: %f seconds' % self.runTime.total_seconds())
            print('Attempting to send Data to Server')
        data = {'cores':self.cores,'accuracy':accuracy, 'runTime': self.runTime.total_seconds(), 'size': self.size, 'features':self.features, 'projectName':self.projectName, 'infoRunTime':self.infoRunTime, 'infoCpuUsage':self.infoCpuUsage, 'infoMemoryUsage':self.infoMemoryUsage, 'infoProgress':self.infoProgress}
        if(self.gpuLogging == 1):
            data.update({'gpuName':self.gpuName,'gpuUUID':self.gpuUUID,'gpuDriver':self.gpuDriver,'infoGpuUsage':self.infoGpuUsage, 'infoGpuMemUsage':self.infoGpuMemUsage, 'infoGpuMemUtil':self.infoGpuMemUtil})
        if not (self.host == 'N/A'):
            self.sendData(data)
        else:
            self.saveData(data)
        if (self.local == 1):
            self.saveData(data)
        return
    def log(self, iteration):
        progress = float(iteration/self.size*100)
        utilCPU = psutil.cpu_percent()
        utilMem = self.process.memory_info().rss
        self.infoRunTime.append((datetime.now()-self.startTime).total_seconds())
        self.infoProgress.append(progress)
        self.infoCpuUsage.append(utilCPU)
        self.infoMemoryUsage.append(utilMem)
        if(self.gpuLogging == 1):
            utilGPU = self.gpuObj[self.gpuID].load
            utilGPUMem = self.gpuObj[self.gpuID].memoryUtil
            gpuMem = self.gpuObj[self.gpuID].memoryUsed
            self.infoGpuUsage.append(utilGPU)
            self.infoGpuMemUtil.append(utilGPUMem)
            self.infoGpuMemUsage.append(gpuMem)
        if not (self.quiet == 1):
            print('Progress: %0.2f%% CPU:%0.1f MEM:%d MB' %(progress, utilCPU, utilMem/1000000))
            if(self.gpuLogging == 1):
                print('GPU:%0.1f gpuMem:%0.1f MB gpuMemUtil:%0.1f' % (utilGPU, gpuMem, utilGPUMem))
        return
    def sendData(self ,data):
        try:
            r = requests.post(self.host, data)
            if(r.status_code == 200):
                if not (self.quiet == 1):
                    print('Response sent successfully to server!')
            self.saveData(data)
        except requests.exceptions.RequestException as e:
            if not (self.quiet == 1):
                print('There is an error with sending the data to the server, logging data to file instead')
        return
    def saveData(self, data):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.filename = 'benchLog_'+timestr+'.json'
        if not (self.quiet == 1):
            print('Saving data to file %s' % self.filename)
        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile)
        return

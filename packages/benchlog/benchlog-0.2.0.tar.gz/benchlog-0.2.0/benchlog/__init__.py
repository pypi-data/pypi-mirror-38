from datetime import datetime
import psutil
import requests
import json
import os
import multiprocessing

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
        self.cores = multiprocessing.cpu_count()
        self.process = psutil.Process(os.getpid())
        self.host = 'N/A'
        self.quiet = quiet
    def setHost(self, host):
        if not (self.quiet == 1):
            print('Host set to ', host)
        self.host = host
        return
    def start(self):
        if not (self.quiet == 1):
            print('[Benchmark Start]')
        self.startTime = datetime.now()
        return
    def end(self):
        self.log(self.size)
        self.endTime = datetime.now()
        self.runTime = self.endTime - self.startTime
        if not (self.quiet == 1):
            print('[Benchmark End]')
            print('Runtime: %f seconds' % self.runTime.total_seconds())
            print('Attempting to send Data to Server')
        data = {'cores':self.cores, 'runTime': self.runTime.total_seconds(), 'size': self.size, 'features':self.features, 'projectName':self.projectName, 'infoRunTime':self.infoRunTime, 'infoCpuUsage':self.infoCpuUsage, 'infoMemoryUsage':self.infoMemoryUsage, 'infoProgress':self.infoProgress}
        if not (self.host == 'N/A'):
            self.sendData(data)
        else:
            self.saveData(data)
        return
    def log(self, iteration):
        progress = float(iteration/self.size)
        utilCPU = psutil.cpu_percent()
        utilMem = self.process.memory_info().rss
        self.infoRunTime.append((datetime.now()-self.startTime).total_seconds())
        self.infoProgress.append(progress)
        self.infoCpuUsage.append(utilCPU)
        self.infoMemoryUsage.append(utilMem)
        if not (self.quiet == 1):
            print('Progress: %0.2f%% CPU:%0.1f MEM:%d MB' %(progress*100, utilCPU, utilMem/1000000))
        return
    def sendData(self ,data):
        try:
            r = requests.post(self.host, data)
            if(r.status_code == 200):
                if not (self.quiet == 1):
                    print('Response sent successfully to server!')
        except requests.exceptions.RequestException as e:
            if not (self.quiet == 1):
                print('There is an error with sending the data to the server, logging data to file instead')
            with open('telemetry.json', 'w') as outfile:
                json.dump(data, outfile)
        return
    def saveData(self, data):
        filename = 'telemetry.json'
        if not (self.quiet == 1):
            print('Saving data to file %s' % filename)
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        return

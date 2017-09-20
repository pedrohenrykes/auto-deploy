#!/usr/bin/python2

import os
import sys
import time
import threading
import commands


class Deploy:
    def __init__(self, workingPath, scriptRunTime):
        self._workingPath = workingPath
        self._scriptRunTime = scriptRunTime
        self._versionedProjects = list()
        self._indexOfProjects = 0
        self._stopRunning = False
        self.searchProjects(workingPath)
        self.runningTimer()

    def searchProjects(self, workingPath):
        try:
            for archive in os.listdir(workingPath):
                if os.path.isdir(workingPath + os.sep + archive):
                    if archive == ".svn":
                        self._versionedProjects.insert(self._indexOfProjects, workingPath)
                        self._indexOfProjects += 1
                    self.searchProjects(workingPath + os.sep + archive)
        except Exception as ex:
            self._stopRunning = True
            self.createLog(self._workingPath, str(ex), "ERROR")

    def runningTimer(self):
        try:
            if not self._stopRunning:
                self.updateProject()
                thread = threading.Timer(self._scriptRunTime, self.runningTimer)
                thread.start()
        except Exception as ex:
            self._stopRunning = True
            self.createLog(self._workingPath, str(ex), "ERROR")

    def updateProject(self):
        if self._versionedProjects.__len__() > 0:
            for project in self._versionedProjects:
                self.shellCommand(project)
        else:
            self._stopRunning = True
            self.createLog(self._workingPath, "Nao existem projetos SVN no diretorio", "ERROR")

    def shellCommand(self, workingPath):
        repository = commands.getoutput("svn info " + workingPath + " | grep \"URL:\"")
        localRevision = commands.getoutput("svn info " + workingPath + " | grep \"Last Changed Rev:\"")
        remoteRevision = commands.getoutput("svn info -r HEAD " + repository[5:] + " | grep \"Last Changed Rev:\"")
        self.createLog(workingPath, "Revisoes: remota/local <=> " + remoteRevision[18:] + "/" + localRevision[18:], "INFOR")

        if int(localRevision[18:]) < int(remoteRevision[18:]):
            self.createLog(workingPath, "################################################", "#####")
            self.createLog(workingPath, "Removendo alteracoes na copia de trabalho...", "INFOR")
            self.executeShell("svn revert -R ", workingPath)
            self.executeShell("svn cleanup ", workingPath)
            self.createLog(workingPath, "Atualizando arquivos na copia de trabalho...", "INFOR")
            self.executeShell("svn update ", workingPath)
            self.createLog(workingPath, "Definindo usuario e grupo do diretorio...", "INFOR")
            self.executeShell("chown -R apache:root ", workingPath)
            self.createLog(workingPath, "Definindo permissoes ao diretorio...", "INFOR")
            self.executeShell("chmod -R 775 ", workingPath)
            self.createLog(workingPath, "################################################", "#####")

    def executeShell(self, command, workingPath):
        if os.system(command + workingPath) == 0:
            self.createLog(workingPath, command + workingPath + ": Ok!", "DEBUG")
        else:
            self._stopRunning = True
            self.createLog(workingPath, command + workingPath + ": Erro!", "DEBUG")

    @staticmethod
    def createLog(logFolder, logMessage, typeOf):
        try:
            if typeOf.__eq__("ERROR"):
                logFile = logFolder + os.sep + "crash.log"
            else:
                logFile = logFolder + os.sep + "deployment.log"

            if not os.path.exists(logFile):
                log = open(logFile, "w")
                log.close()
            elif os.path.getsize(logFile) >= 10485760:
                log = open(logFile, "w")
                log.write("")
                log.close()

            message = time.strftime("%d-%m-%Y %H:%M:%S") + " --- " + typeOf + ": " + logMessage + "\n"
            log = open(logFile, "a")
            log.write(message)
            log.close()
            print(message)
        except Exception as ex:
            print(ex)


file = os.path.realpath(__file__)
path = os.path.dirname(file)
try:
    if sys.argv.__len__() >= 2:
        param = sys.argv[1]
        if os.path.isdir(param):
            Deploy(param, 5)
        else:
            Deploy.createLog(path, "Informe um diretorio como argumento", "ERROR")
    else:
        Deploy(path, 5)
except Exception as e:
    Deploy.createLog(path, str(e), "ERROR")

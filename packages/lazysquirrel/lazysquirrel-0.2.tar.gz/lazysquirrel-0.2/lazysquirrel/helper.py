import os
import json
import subprocess
import signal

SCRIPT_CWD = os.getcwd()

CONFIG_FILE_NAME  = "/config.json"
PIDS_FILE_NAME    = "/pids.json"

def createCommandDirectory(configDir):
  if not os.path.exists(configDir):
    os.makedirs(configDir)

def printConfigFile(configFile):
  print json.dumps(configFile, indent=4, sort_keys=True)

def createLogDirectory(configDirPath):
  if not os.path.exists(configDirPath + "/logs"):
    os.makedirs(configDirPath + "/logs")

def createCustomLogDirectory(directoryName, configDirPath):
  if not os.path.exists(configDirPath + "/logs/" + str(directoryName)):
    os.makedirs(configDirPath + "/logs/" + str(directoryName))

def initializePidsFile(configDir, init = False):
  pidsPath = configDir + PIDS_FILE_NAME
  # Create pids file
  if not os.path.isfile(pidsPath):
    with open(pidsPath, 'w'): pass

  # Init pids json file only if its empty or init flag is true
  if os.stat(pidsPath).st_size == 0 or init == True:
    with open(pidsPath, mode='w') as f:
      json.dump([], f)

def initializeConfigurationFile(configDir, init = False):
  configPath = configDir + CONFIG_FILE_NAME
  # Create configuration file
  if not os.path.isfile(configPath):
    with open(configPath, 'w'): pass

  # Init configuration json file only if its empty or init flag is true
  if os.stat(configPath).st_size == 0 or init == True:
    with open(configPath, mode='w') as f:
      json.dump({
        "configuration": {
          "programs": [],
          "servers": []
        }
      }, f)
  
  return loadConfigFile(configDir)


def loadConfigFile(configDir):
  configPath = configDir + "/config.json"

  # Loads configuration file
  with open(configPath) as file:
    return json.load(file)['configuration']

def openProgram(program, configDirPath):
  createCustomLogDirectory(program, configDirPath)
  logFile       = os.path.join(configDirPath + str("/logs/" + program), "logs.log")
  errorLogFile  = os.path.join(configDirPath + str("/logs/" + program), "errors.log")
  subprocess.Popen([str(program)], stdout=open(logFile, 'w'), stderr=open(errorLogFile, 'a'), preexec_fn=os.setpgrp)

def addProgramToConfigFile(program, configDirPath):
  configPath = configDirPath + CONFIG_FILE_NAME
  with open(configPath, mode='r') as configFileJson:
    configFile = json.load(configFileJson)
  with open(configPath, mode='w') as configFileJson:
    configFile['configuration']['programs'].append(program)
    json.dump(configFile, configFileJson)

def addServerToConfigFile(serverName, serverPath, serverCommand, configDirPath):
  configPath = configDirPath + CONFIG_FILE_NAME
  with open(configPath, mode='r') as configFileJson:
    configFile = json.load(configFileJson)
  with open(configPath, mode='w') as configFileJson:
    configFile['configuration']['servers'].append({
      'name': serverName,
      'path': serverPath,
      'command': serverCommand
    })
    json.dump(configFile, configFileJson)

def saveProcessId(serverName, pid, configDirPath):
  location = configDirPath + "/pids.json"
  with open(location, mode='r') as pidsJson:
    pids = json.load(pidsJson)
  with open(location, mode='w') as pidsJson:
    pids.append({
      'name': serverName, 
      'pid': pid
    })
    json.dump(pids, pidsJson)

def killAllServers(configDirPath):
  location = configDirPath + "/pids.json"
  with open(location, mode='r') as pidsJson:
    pids = json.load(pidsJson)
    for server in pids:
      print server['name']
      try: 
        os.killpg(int(server['pid']), signal.SIGKILL)
      except:
        print "Server " + server['name'] + " is not running to terminate.."
  initializePidsFile(configDirPath, init=True)

def openServer(server, configDirPath):
  os.chdir(str(server['path']))
  createCustomLogDirectory(server['name'],configDirPath)
  logFile       = os.path.join(configDirPath + str("/logs/" + server['name']), "logs.log")
  errorLogFile  = os.path.join(configDirPath + str("/logs/" + server['name']), "errors.log")
  process       = subprocess.Popen(str(server['command']).split(), stdout=open(logFile, 'w'), stderr=open(errorLogFile, 'a'), preexec_fn=os.setpgrp)
  return process.pid
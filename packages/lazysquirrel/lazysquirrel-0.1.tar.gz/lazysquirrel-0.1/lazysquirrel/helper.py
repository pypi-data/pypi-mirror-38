import os
import json
import subprocess
import signal

SCRIPT_CWD = os.getcwd()

def getCwd():
  return SCRIPT_CWD

def createLogDirectory():
  if not os.path.exists(getCwd() + "/logs"):
    os.makedirs(getCwd() + "/logs")

def createCustomLogDirectory(directoryName):
  if not os.path.exists(getCwd() + "/logs/" + str(directoryName)):
    os.makedirs(getCwd() + "/logs/" + str(directoryName))

def initializePidsFile(init = False):
  pidsPath = getCwd() + '/pids.json'
  # Create pids file
  if not os.path.isfile(pidsPath):
    with open(pidsPath, 'w'): pass

  # Init pids json file only if its empty or init flag is true
  if os.stat(pidsPath).st_size == 0 or init == True:
    with open(pidsPath, mode='w') as f:
      json.dump([], f)

def loadConfigFile():
  initializePidsFile()

  # Loads configuration file
  with open(getCwd() + '/config.local.json') as file:
    return json.load(file)['configuration']

def openProgram(program):
  createCustomLogDirectory(program)
  logFile       = os.path.join(getCwd() + str("/logs/" + program), "logs.log")
  errorLogFile  = os.path.join(getCwd() + str("/logs/" + program), "errors.log")
  subprocess.Popen([str(program)], stdout=open(logFile, 'w'), stderr=open(errorLogFile, 'a'), preexec_fn=os.setpgrp)

def saveProcessId(serverName, pid):
  location = getCwd() + "/pids.json"
  with open(location, mode='r') as pidsJson:
    pids = json.load(pidsJson)
  with open(location, mode='w') as pidsJson:
    pids.append({
      'name': serverName, 
      'pid': pid
    })
    json.dump(pids, pidsJson)

def killAllServers():
  location = getCwd() + "/pids.json"
  with open(location, mode='r') as pidsJson:
    pids = json.load(pidsJson)
    for server in pids:
      print server['name']
      try: 
        os.killpg(int(server['pid']), signal.SIGKILL)
      except:
        print "Server " + server['name'] + " is not running to terminate.."
  initializePidsFile(init=True)

def openServer(server):
  os.chdir(str(server['path']))
  createCustomLogDirectory(server['name'])
  logFile       = os.path.join(getCwd() + str("/logs/" + server['name']), "logs.log")
  errorLogFile  = os.path.join(getCwd() + str("/logs/" + server['name']), "errors.log")
  process   = subprocess.Popen(str(server['command']).split(), stdout=open(logFile, 'w'), stderr=open(errorLogFile, 'a'), preexec_fn=os.setpgrp)
  return process.pid
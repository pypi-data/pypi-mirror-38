import click
import os
import helper
import json
import subprocess
import progressbar
from time import sleep


@click.group()
@click.pass_context
def main(ctx):
  """
  This python script should help easily open your daily use programs or/and development servers on Linux systems (that's what I've tested it on, so far). In case of any power outage, or unexpected shutdown it will be painful to click and walk through your programs and run each and single one of them, so this should help you get it together at one place and RUN THEM ALL!

  Examples:

  $ lazysquirrel program

  $ lazysquirrel server

  $ lazysquirrel kill servers

  $ lazysquirrel start [p, s] or [program, server]

  """
  configDir = "~/.lazysquirrel"
  configDir = os.path.expanduser(configDir)

  helper.createCommandDirectory(configDir)
  configFile = helper.initializeConfigurationFile(configDir)
  helper.initializePidsFile(configDir)

  ctx.obj = {
    'configFile'    : configFile,
    'configDirPath' : configDir
  }


@main.command()
@click.pass_context
def config(ctx):
  """
  Prints config file
  """
  configFile = ctx.obj['configFile']
  helper.printConfigFile(configFile)


@main.command()
@click.option(
  'server', '-ap',
  help='server you want to start',
  prompt="Please enter server name"
)
@click.pass_context
def server(ctx, server):
  """
  Adds server to list of lazy servers
  """
  serverPath = click.prompt(
    "Please enter your server path"
  )
  serverCommand = click.prompt(
    "Please enter your server run command"
  )
  configFile = ctx.obj['configFile']

  helper.addServerToConfigFile(server, serverPath, serverCommand, ctx.obj['configDirPath'])


@main.command()
@click.option(
  '--program',
  help='program you want to start',
  prompt="Please enter program name"
)
@click.pass_context
def program(ctx, program):
  """
  Adds program to list of lazy programs
  """
  configFile = ctx.obj['configFile']
  helper.addProgramToConfigFile(program, ctx.obj['configDirPath'])


def handleChoice(choice):
  return {
    "p": loadPrograms,
    "programs": loadPrograms,
    "s": loadServers,
    "servers": loadServers
  }.get(str(choice), None)


def loadPrograms(config, configDirPath):
  print "\n\033[0;37;48m--------------"
  print "\033[0;37;48mOpening registered programs"
  length = len(config['programs'])
  progressbar.print_progress(0, 1, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
  for i, program in enumerate(config['programs']):
    helper.openProgram(program, configDirPath)
    sleep(0.2)
    progressbar.print_progress(i + 1, length, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
  print "\033[0;37;48mOpening complete, check errors.log to see if there are any errors"
  print "\033[0;37;48m--------------\n"


def loadServers(config, configDirPath):
  print "\n\033[0;37;48m--------------"
  print "\033[0;37;48mOpening registered servers"
  length = len(config['servers'])
  progressbar.print_progress(0, 1, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
  for i, server in enumerate(config['servers']):
    pid = helper.openServer(server, configDirPath)
    helper.saveProcessId(server['name'], pid, configDirPath)
    sleep(0.2)
    progressbar.print_progress(i + 1, length, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
  print "\033[0;37;48m\nOpening complete, check logs associated with each server"
  print "\033[0;37;48m--------------\n"


@main.command()
@click.argument('start')
@click.pass_context
def start(ctx, start):
  """
  Starts lazy programs/servers 
  """
  configFile = ctx.obj['configFile']

  function = handleChoice(start)

  if function is None or not callable(function):
    print "\n\033[1;31;40m\n-Oh, you entered unknown option, please check again.\n"

  if callable(function):
    function(configFile, ctx.obj['configDirPath'])


@main.command()
@click.argument('kill')
@click.pass_context
def kill(ctx, kill):
  """
  Kills all working servers 
  """
  configDirPath = ctx.obj['configDirPath']

  print "\033[0;37;48m \n-Killing all running servers"
  helper.killAllServers(configDirPath)


if __name__ == "__main__":
    main()
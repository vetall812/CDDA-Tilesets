"""
this script will try to find out what overmap tiles have sprites
"""

import sys
import os
from subprocess import STDOUT, call, check_output
import argparse
import sqlite3

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def ShowExceptionAndExit (exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter to exit.")
    sys.exit(-1)

def CheckFile (str_path, str_file):
  my_file = os.path.join(str_path, str_file)
  return os.path.isfile(my_file)

def CheckCDDAdir (str_path):
  if CheckFile(str_path,'VERSION.txt'):
    return str(os.path.normpath(str_path)).lower()
  else:
    return False

def FindCDDAdir (cli_arg):
  print(f'Determining CDDA executable directory:')
  CDDAcli = False
  CDDAenv = False
  CDDAsql = False

  Result = False

  # Check command line argument
  if cli_arg :
    CDDAcli = CheckCDDAdir(cli_arg)
    if CDDAcli:
      print(f'- CLI argument : '+ CDDAcli + f'{bcolors.OKGREEN} found!{bcolors.ENDC}')
      Result = CDDAcli
    else:
      print(f'- CLI argument : '+ cli_arg + f'{bcolors.WARNING} not found!{bcolors.ENDC}')
  else:
    print(f'- CLI argument : ' + f'{bcolors.WARNING}not provided!{bcolors.ENDC}')

  # Check environment variable
  try:
    env_arg = CheckCDDAdir(os.getenv('CDDA_PATH'))
  except:
    env_arg = False

  if env_arg:
    CDDAenv = CheckCDDAdir(env_arg)
    if CDDAenv:
      if CDDAcli:
        if CDDAenv == CDDAcli:
          print(f'- ENV variable : exist and same as CLI argument.' )
        else:
          print(f'- ENV variable : ' + CDDAenv + f'{bcolors.WARNING} different from CLI!{bcolors.ENDC}')
      else:
        Result = CDDAenv
        print(f'- ENV variable : ' + CDDAenv + f'{bcolors.OKGREEN} found!{bcolors.ENDC}')
    else:
      print(f'- ENV variable : ' + cli_arg + f'{bcolors.WARNING} not found!{bcolors.ENDC}')
  else:
    print(f'- ENV variable : ' + f'{bcolors.WARNING}not provided!{bcolors.ENDC}')

  # Check Kitty CDDA Launcher settings
  AppsLocalDir = os.path.join(os.getenv('LOCALAPPDATA'), 'CDDA Game Launcher')
  KittenSettings = 'configs.db'
  if CheckFile(AppsLocalDir,KittenSettings):
    try:
      dbfile = os.path.join(AppsLocalDir, KittenSettings)
      con = sqlite3.connect(dbfile)
      cur = con.cursor()
      sql_arg = cur.execute('SELECT value FROM config_value WHERE name = "game_directory" ').fetchone()[0]
      con.close()
    except:
      sql_arg = False

    if sql_arg:
      CDDAsql = CheckCDDAdir(sql_arg)
      if CDDAsql:
        if CDDAenv:
          if CDDAcli:
            if CDDAsql == CDDAcli:
              print(f'- Launcher  DB : setting exist and same as CLI argument.')
            elif CDDAsql == CDDAenv:
              print(f'- Launcher  DB : setting exist and same as environment variable, but differs from CLI argument.')
            else:
              print(f'- Launcher  DB : ' + CDDAsql + f'{bcolors.WARNING} different from everything above!{bcolors.ENDC}')
          elif CDDAsql == CDDAenv:
            print(f'- Launcher  DB : setting exist and same as environment variable.')
          else:
            print(f'- Launcher  DB : ' + CDDAsql + f'{bcolors.WARNING} different from environment variable!{bcolors.ENDC}')
        elif CDDAcli:
          if CDDAsql == CDDAcli:
            print(f'- Launcher  DB : setting exist and same as CLI argument.')
          else:
            print(f'- Launcher  DB : ' + CDDAsql + f' setting exist, but differs from CLI argument.')
        else:
          Result = CDDAsql
          print(f'- Launcher  DB : ' + CDDAsql + f'{bcolors.OKGREEN} found!{bcolors.ENDC}')
      else:
        print(f'- Launcher  DB : ' + sql_arg + f'{bcolors.WARNING} setting exist, but no CDDA executable found{bcolors.ENDC}')
    else:
      print(f'- Launcher  DB : {bcolors.WARNING}Launcher is here, but no game_directory found!{bcolors.ENDC}')
  else:
    print(f'- Launcher  DB : no Kitten CDDA Launcher found.')

  #print('\n')
  if Result:
    print(f'+ game is here : {bcolors.OKCYAN}' + Result + f'{bcolors.ENDC}')
    return Result
  else:
    print(f'{bcolors.FAIL}! CDDA game directory not found!{bcolors.ENDC}')
    exit(1)

def GetGitRoot (p):
    """Return None if p is not in a git repo, or the root of the repo if it is"""
    if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w'), cwd=p) != 0:
        return None
    else:
        root = check_output(["git", "rev-parse", "--show-toplevel"], cwd=p)
        return root.strip().decode( "utf-8" )

def FindTilesetDir (cli_arg2):
  print('Determining tileset and its location')
  RepoDir = False

  ScriptDir = str(os.path.abspath(os.path.dirname(__file__))).lower()
  CWDir     = str(os.path.normpath(os.getcwd())).lower()

  if cli_arg2:
    print('- Tileset argument provided. Lets try to find tileset location.')
    print(f'{bcolors.OKBLUE}: '+cli_arg2+f'{bcolors.ENDC}')
    #if os.path.isdir(cli_arg2):

  else:
    print('- No tileset argument provided. Should try to find repository and offer a choice.')
  return

def main (args):
  sys.excepthook = ShowExceptionAndExit

  CDDAdir = FindCDDAdir(args.CDDAdir)
  print('\n')
  FindTilesetDir(args.tileset)

#  FullPath = args.CDDAdir
#
#  PathDetails = FullPath.split('\\')
#
#  print(f'Working path is : {bcolors.OKCYAN}' + FullPath + f'{bcolors.ENDC}')
#  if PathDetails[-1] == 'tools' :
#    print('in tools')
#    print('')
    # getting tilesets
#  else :
#    try :
#      GFXindex = PathDetails.index('gfx')
#    except :
#      GFXindex = 0

#    if GFXindex > 0 :
#      TilesetName = PathDetails[PathDetails.index('gfx')+1]
#      print(f'Tileset name : {bcolors.OKCYAN}' + TilesetName + f'{bcolors.ENDC}')
#      print('')
#    else :
#      print(f'No tileset detected. Exiting.')
#      print('')
#      quit()



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Check overmap tileset coverage.",
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog = "Can be used with environment variables.\n"
      "use the provided tools:\n"
      "  CDDAdir can be set up with `set_game_path.cmd`\n"
      "  tileset can be set up with `set_tileset.cmd`\n"
      "\n"
      "Additionally, if using the Kitten CDDA launcher,\n"
      "this tool can retrieve CDDAdir from the launcher.\n")
  parser.add_argument(
      "CDDAdir", type=str,
      nargs="?",
      help="Path to the game executable. If left empty, the tool will attempt to determine the path through other methods.")
  parser.add_argument(
      "tileset", type=str,
      nargs="?",
      help="Tileset directory name. If left empty, the tool will attempt to identify possible tilesets based on the current directory.")
  parser.add_argument(
      "--tile", type=str,
      help="Specific overmap tile to check.")

  main(parser.parse_args())

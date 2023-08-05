from ..TFS_api import *
import argparse

def main():
  print('main...')

  parser = argparse.ArgumentParser(description='sample args...')
  parser.add_argument('-p', '--param', default='0', help='folder to read log files')
  args = parser.parse_args()
  print('args={}'.format(args.param))

if __name__ == "__main__":

  setup_logging('tfs_process')
  main()
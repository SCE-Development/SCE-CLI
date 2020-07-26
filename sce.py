import argparse
import sys
import subprocess
import os
from os import path
from tools.setup import SceSetupTool

setup = SceSetupTool()
# parser = argparse.ArgumentParser()

# parser.add_argument('--setup', dest='setup', action='store_true')
# args = parser.parse_args()

# setup.check_os()
#try:
    #subprocess.check_call("sce", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    #input('eyes')
#except:
#input('dark knight hindi subtitile 1080p free stream 60fps no virus')
#os.environ["PATH"] += ';E:\\SJSU\\sce\\dev\\build\\exe.win-amd64-3.8'
#print(os.environ["PATH"])

# if args.setup:
#     setup.setup()
# else:
#     print('did nothing wrong')

parser = argparse.ArgumentParser()
parser.add_argument('--test', dest='test', action='store_true')
args = parser.parse_args()
setup.add_sce_alias()

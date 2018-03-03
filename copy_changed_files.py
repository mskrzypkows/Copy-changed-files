#!/usr/bin/python

import sys
import os
import time
import signal
import shutil
from datetime import datetime

def exitHandler(signal, frame):
    print '\nThanks for remote work! Bye!'
    sys.exit(0)

if len(sys.argv) != 3:
    print 'Wrong number of arguments, usage: ./' + os.path.basename(__file__) + ' /source/directory /destination/directory'
    sys.exit(0)

sourceDir = sys.argv[1]
destDir = sys.argv[2]

signal.signal(signal.SIGINT, exitHandler)

excludeSuffix = ['.kate-swp','.swp']    # list of excluded files suffixes

# get list of files and their modificaton time
filesMap = {}

def directoryTreeWalker(firstRun):
    """Go through directiories and check for modified files"""
    for root, dirs,files in os.walk(sourceDir):
        for fname in files:
            path = os.path.join(root, fname)
            if any(path.endswith(end) for end in excludeSuffix):
                continue
            st = os.stat(path)
            mtime = datetime.fromtimestamp(st.st_mtime)
            if firstRun:        # first time remember all files last modificaton time
                filesMap[path] = mtime
            else:               # next runs check if any file modified and copy
                if path not in filesMap or mtime > filesMap[path]:
                    filesMap[path] = mtime
                    relativeLoc = os.path.relpath(path, sourceDir)
                    destFile = os.path.join(destDir, relativeLoc)
                    if not os.path.exists(os.path.dirname(destFile)):
                        os.makedirs(os.path.dirname(destFile))
                    shutil.copy(path, destFile)
                    print('Copied: %s > %s  %s'%(path, destFile, mtime.strftime("%Y-%m-%d %H:%M:%S")))


directoryTreeWalker(True)

while True:
    directoryTreeWalker(False)
    time.sleep(0.7)

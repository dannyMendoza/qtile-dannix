#!/usr/bin/env python

from libqtile.command.client import InteractiveCommandClient as qicc

c = qicc()
history = None
history = c.group.info()['focus_history']
print(history)
# if len(history) > 1:
#     history = history[0]
# c.group.focus_by_name(history)

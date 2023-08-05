#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2018/11/2 14:47"
__author__ = "WeiYanfeng"
__email__ = "weiyf1225@qq.com"
__version__ = "0.0.1"
        
~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
借助线程，延迟定时执行某些函数。

参考 [在python中延迟执行函数 - Arian's Blog](https://arianx.me/2018/06/27/Simple-time-event-loop-in-python/)

[heapq — Heap queue algorithm — Python 3.7.1 documentation](https://docs.python.org/3/library/heapq.html)

heapq 使用示例如下：

    >>> from heapq import *
    >>> h = []
    >>> heappush(h, (5, 'write code'))
    >>> heappush(h, (7, 'release product'))
    >>> h
    [(5, 'write code'), (7, 'release product')]
    >>> heappush(h, (1, 'write spec'))
    >>> h
    [(1, 'write spec'), (7, 'release product'), (5, 'write code')]
    >>> heappush(h, (3, 'create tests'))
    >>> h
    [(1, 'write spec'), (3, 'create tests'), (5, 'write code'), (7, 'release product')]
    >>> heappop(h)
    (1, 'write spec')
    >>> h
    [(3, 'create tests'), (7, 'release product'), (5, 'write code')]
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from .WyfPublicFuncs import PrintTimeMsg, GetCurrentTime, GetYYYYMMDDhhnnss
import time
import heapq
from datetime import datetime, timedelta
from threading import Thread


class CTimeEvent:
    # 时间事件
    def __init__(self, cbFunc, sYmdHnsPlanTime, *args, **kwargs):
        self.cbFunc = cbFunc
        self.sYmdHnsPlanTime = sYmdHnsPlanTime
        self.args = args
        self.kwargs = kwargs
        self.oResult = None

        self.bRunAlive = False  # 是否在执行中
        self.bAlreayRun = False  # 是否已执行

    def __lt__(self, other):
        # For heap sort.
        return self.sYmdHnsPlanTime < other.sYmdHnsPlanTime

    def execute(self):
        self.bRunAlive = True
        self.oResult = self.cbFunc(*self.args, **self.kwargs)
        self.bRunAlive = False
        self.bAlreayRun = True
        return self.oResult


class CDeferFuncThread:
    def __init__(self):
        self.lsEvents = []
        self.bRunAlive = False  # 是否在执行中
        self.bAlreayRun = False  # 是否已执行
        self.thread = None

    def AddDeferFunc(self, cbFunc, sYmdHnsPlanTime, *args, **kwargs):
        oEvent = CTimeEvent(cbFunc, sYmdHnsPlanTime, *args, **kwargs)
        heapq.heappush(self.lsEvents, oEvent)
        return oEvent

    def CheckTimeRunDefer(self):
        while len(self.lsEvents) > 0:
            try:
                oEvent = heapq.heappop(self.lsEvents)
            except IndexError:
                break
            if GetCurrentTime() >= oEvent.sYmdHnsPlanTime:
                oEvent.execute()
            else:
                heapq.heappush(self.lsEvents, oEvent)
                break
        return len(self.lsEvents)

    def LoopAndCheckRun(self, sYmdHnsTimeOut=''):
        PrintTimeMsg('CDeferFuncThread.LoopAndCheckRun.Start...')
        self.bRunAlive = True
        while not self.bAlreayRun:
            if self.CheckTimeRunDefer() == 0:
                PrintTimeMsg('CDeferFuncThread.LoopAndCheckRun.EndOK!')
                break
            if sYmdHnsTimeOut and GetCurrentTime() >= sYmdHnsTimeOut:
                PrintTimeMsg('CDeferFuncThread.LoopAndCheckRun.TimeOut=%s!' % sYmdHnsTimeOut)
                break
            time.sleep(0.001)
        self.bRunAlive = False
        self.bAlreayRun = True

    def StartLoopCheckRun(self, sYmdHnsTimeOut='', bInThread=True):
        if bInThread:
            self.thread = Thread(target=self.LoopAndCheckRun, args=[sYmdHnsTimeOut])
            self.thread.start()
            return self.thread
        else:
            self.LoopAndCheckRun(sYmdHnsTimeOut)


def mainCDeferFuncThread():
    def cbTest(a, b):
        PrintTimeMsg('cbTest.a=%s,b=%s=' % (a, b))

    o = CDeferFuncThread()
    o.AddDeferFunc(cbTest, GetYYYYMMDDhhnnss(5), 1, 2)
    o.AddDeferFunc(cbTest, GetYYYYMMDDhhnnss(10), 3, 4)
    o.StartLoopCheckRun(GetYYYYMMDDhhnnss(8), True)

# --------------------------------------
if __name__ == '__main__':
    mainCDeferFuncThread()

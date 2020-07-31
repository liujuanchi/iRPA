#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import queue
import random
import time
import rpa_history_data as r


class Producter(threading.Thread):
    """年份生产者线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        for i in range(2002, 2005):
            self.queue.put(i)
            print('put num in Queue %s' %  i)
            time.sleep(1)

        print('put queue done')


class ConsumeEven(threading.Thread):
    """消费线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        while True:
            try:
                queue_val = self.queue.get()                
                print(queue_val)                
                r.gethistorylist(str(queue_val))
            except Exception as Argument:
                print(Argument)
                break



q = queue.Queue()
pt = Producter('producter', q)
ce1 = ConsumeEven('consumeeven1', q)
#ce2 = ConsumeEven('consumeeven2', q)
ce1.start()
#ce2.start()
pt.start()
pt.join()
ce1.join()
#ce2.join()

#q = queue.Queue(3)
#q.put(13, block=True, timeout=5)
#q.task_done()
#q.put_nowait(23)
#q.task_done()
#print(q.get())
#q.join()
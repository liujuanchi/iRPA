#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import queue
import random
import time


class Producter(threading.Thread):
    """生产者线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        for i in range(10):
            randomnum = random.randint(1, 99)
            self.queue.put(randomnum)
            print('put num in Queue %s' %  randomnum)
            time.sleep(1)

        print('put queue done')


class ConsumeEven(threading.Thread):
    """奇数消费线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        while True:
            try:
                queue_val = self.queue.get(1, 3)
            except Exception as Argument:
                print(Argument)
                break

            if queue_val % 2 == 0:
                print('--1 Get Even Num %s ' % queue_val)
            else:
                self.queue.put(queue_val)


class ConsumeEvenB(threading.Thread):
    """奇数消费线程"""
    def __init__(self, t_name, queue):
        self.queue = queue
        threading.Thread.__init__(self, name=t_name)

    def run(self):
        while True:
            try:
                queue_val = self.queue.get(1, 3)
            except Exception as Argument:
                print(Argument)
                break

            if queue_val % 2 > 0:
                print('--2 Get Even Num %s ' % queue_val)
            else:
                self.queue.put(queue_val)

q = queue.Queue()
pt = Producter('producter', q)
ce1 = ConsumeEven('consumeeven1', q)
ce2 = ConsumeEvenB('consumeeven2', q)
ce1.start()
ce2.start()
pt.start()
pt.join()
ce1.join()
ce2.join()

#q = queue.Queue(3)
#q.put(13, block=True, timeout=5)
#q.task_done()
#q.put_nowait(23)
#q.task_done()
#print(q.get())
#q.join()
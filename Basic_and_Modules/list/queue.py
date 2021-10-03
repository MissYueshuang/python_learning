# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:58:30 2020

@author: rmileng
"""
'''
队列是一种先进先出的数据类型，它的跟踪原理类似于在超市收银处排队，
队列里的的第一个人首先接受服务，
新的元素通过入队的方式添加到队列的末尾，而出队就是将队列的头元素删除。
'''
class Queue():
    def __init__(self,size):
        self.size = size
        self.front = -1
        self.rear = -1
        self.queue = []

    def enqueue(self,ele):
        if self.is_full():
            raise Exception('Queue is full')
        else:
            self.queue.append(ele)
            self.rear = self.rear + 1

    def dequeue(self):
        if self.is_empty():
            raise Exception('Queue is empty')
        else:
            self.queue.pop(0)
            self.front = self.front + 1
            
    def is_full(self):
        return self.rear - self.front +1 == self.size

    def is_empty(self):
        return self.front == self.rear

    def show_queue(self):
        print(self.queue)
        
q = Queue(10)
for i in range(5):
    q.enqueue(i)
q.show_queue()


for i in range(3):
    q.dequeue()
q.show_queue()
print(q.is_empty())
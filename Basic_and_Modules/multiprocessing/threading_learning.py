# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 10:34:17 2020

@author: rmileng
"""
############################################################   
import threading

def thread_job():
    print('This is an added Thread, number is %s' % threading.current_thread())

def main():
    added_thread = threading.Thread(target=thread_job)
    added_thread.start()
    print(threading.active_count())
    print(threading.enumerate())
    print(threading.current_thread())
    
if __name__=='__main__':
    main()
    
 
 ############################################################      
import threading
import time

# 不加join的结果
def thread_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(0.1) # 任务间隔0.1s
    print("T1 finish\n")

added_thread = threading.Thread(target=thread_job, name='T1')
added_thread.start()
print("all done\n")
# 结果是 T1 start， all done， T1 finish； 而不是 T1 start， T1 finish， all done

# 加入join的结果
# 如果要遵循顺序，可以在启动线程后对它调用join
added_thread.start()
added_thread.join()
print("all done\n")

def T1_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(0.1)
    print("T1 finish\n")

def T2_job():
    print("T2 start\n")
    print("T2 finish\n")

thread_1 = threading.Thread(target=T1_job, name='T1')
thread_2 = threading.Thread(target=T2_job, name='T2')
thread_1.start() # 开启T1
thread_2.start() # 开启T2
print("all done\n")


thread_1.start()
thread_1.join() # notice the difference!
thread_2.start()
print("all done\n")


thread_1.start()
thread_2.start()
thread_1.join() # notice the difference!
print("all done\n")


thread_1.start() # start T1
thread_2.start() # start T2
thread_2.join() # join for T2
thread_1.join() # join for T1
print("all done\n")

############################################################   
## Queue
import threading
import time
from queue import Queue

# 定义一个被多线程调用的函数
def job(l,q):
    for i in range (len(l)):
        l[i] = l[i]**2
    q.put(l)   #多线程调用的函数不能用return返回值
    
# 定义一个多线程函数
def multithreading():
    q =Queue()    # q中存放返回值，代替return的返回值
    threads = []
    data = [[1,2,3],[3,4,5],[4,4,4],[5,5,5]]

# 在多线程函数中定义四个线程，启动线程，将每个线程添加到多线程的列表中
for i in range(4):   #定义四个线程
    t = threading.Thread(target=job,args=(data[i],q)) #Thread首字母要大写，被调用的job函数没有括号，只是一个索引，参数在后面
    t.start()#开始线程
    threads.append(t) #把每个线程append到线程列表中
    
# 分别join四个线程到主线程
for thread in threads:
    thread.join()

# 定义一个空的列表results，将四个线运行后保存在队列中的结果返回给空列表results    
results = []
for _ in range(4):
    results.append(q.get())  #q.get()按顺序从q中拿出一个值
print(results)   
    

## 完整的代码
import threading
import time

from queue import Queue


def job(l,q):
    for i in range (len(l)):
        l[i] = l[i]**2 #
    q.put(l) # Put an item into the queue.

def multithreading():
    q =Queue()
    threads = []
    data = [[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    for i in range(4):
        t = threading.Thread(target=job,args=(data[i],q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(4):
        results.append(q.get(_))
    print(results)

if __name___=='__main__':
    multithreading()   

############################################################       
## GIL
import threading
from queue import Queue
import copy
import time

def job(l, q):
    res = sum(l)
    q.put(res)

def multithreading(l):
    q = Queue()
    threads = []
    for i in range(4):
        t = threading.Thread(target=job, args=(copy.copy(l), q), name='T%i' % i)
        t.start()
        threads.append(t)
    [t.join() for t in threads]
    total = 0
    for _ in range(4):
        total += q.get()
    print(total)

def normal(l):
    total = sum(l)
    print(total)

if __name__ == '__main__':
    l = list(range(1000000))
    s_t = time.time()
    normal(l*4)
    print('normal: ',time.time()-s_t)
    s_t = time.time()
    multithreading(l)
    print('multithreading: ', time.time()-s_t)
    
############################################################     
# 不使用LOCK
import threading

def job1():
    global A
    for i in range(10):
        A+=1
        print('job1',A)

def job2():
    global A
    for i in range(10):
        A+=10
        print('job2',A)

if __name__== '__main__':
    lock=threading.Lock()
    A=0
    t1=threading.Thread(target=job1)
    t2=threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()    
    
# 使用Lock    
def job1():
    global A,lock
    lock.acquire()
    for i in range(10):
        A+=1
        print('job1',A)
    lock.release()

def job2():
    global A,lock
    lock.acquire()
    for i in range(10):
        A+=10
        print('job2',A)
    lock.release()    
    
if __name__== '__main__':
    lock=threading.Lock()
    A=0
    t1=threading.Thread(target=job1)
    t2=threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()    
    

import threading
import time

class ThreadTool(object):
    def __init__(self, maxThreadNum):
        self.max_num     = int(maxThreadNum)
        self.cur_num     = 0
        self.thread_list = []
        self.sem         = threading.Semaphore(int(maxThreadNum))

    def threadFunc(self, index, function, paraList):
        function(paraList)
        self.thread_list[index] = None
        self.sem.release()

    def haveFree(self):
        if self.getFreeIndex() != -1:
            return True
        return False
    
    def getFreeIndex(self):
        num   = len(self.thread_list)
        index = 0
        for item in self.thread_list:
            if item == None:
                return index
            else:
                index = index + 1
        if num >= self.max_num:
            return -1
        return num

    def threadStart(self, function, paraList):
        index = self.getFreeIndex()
        if index < 0:
            return False
        
        self.sem.acquire()
        handle = threading.Thread(self.threadFunc, (index, function, paraList)) 
        self.thread_list[index] = handle
        handle.start()

    def threadStartWait(self, function, paraList):
        self.sem.acquire()
        index = self.getFreeIndex()
        if index < 0:
            return False

        if paraList == None:
            paraList = []

        handle = threading.Thread(target=self.threadFunc, args=(index, function, paraList))
        self.thread_list.append(str(index))
        self.thread_list[index] = handle
        handle.start()
    
    def allFree(self):
        for item in self.thread_list:
            if item != None:
                return False
        return True

    @classmethod
    def start(function, paraList):
        handle = threading.Thread(function, paraList)
        handle.start()
        return handle

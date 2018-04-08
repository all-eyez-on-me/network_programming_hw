You should not use queue.Queue to comminicate between multiprocess. 不能多进程间通信父子传对象

解决方法：

multiprocess.Queue()


实现多进程对象通信：


实现方法

multiprocessing.Vaule Lock 



多线程不能用debug


logger添加后不能name相同， 否则会输出多次。




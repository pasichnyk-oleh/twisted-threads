# coding: utf-8 -*-

from twisted.internet import reactor, threads, defer


def main_callback(result):
    #sort by order_priority
    sorted_res = sorted(result, key=lambda x: x[1][1])

    print ('result:', [item[1][0] for item in sorted_res])


def worker(num, order_priority=0):
    '''
    Run some number work

    :param num: number to processing
    :param order_priority: sort priority in result of main callback
    :return: tuple: (number result, sort priority)
    '''
    return num ** 2, order_priority


def worker_err(error):
    print(error)
    reactor.callFromThread(reactor.stop)


def processing(nums):
    workers_list = []
    for num, order_priority in nums:
        workers_list.append(threads.deferToThread(worker, num, order_priority).addErrback(worker_err))

    return defer.DeferredList(workers_list)


#numbers to sqrt
#(x, y): x - number, y - priority
nums = [(2, 4),(3, 3), (4, 2), (5, 6)]

d = processing(nums)
d.addCallback(main_callback)

reactor.run()

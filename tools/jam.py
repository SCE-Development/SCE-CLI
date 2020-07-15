import threading
import time
import random

pizza_sem = threading.Semaphore()
spagy_sem = threading.Semaphore()
costco_sem = threading.Semaphore()


def bake_pizza():
    print(' so u wanna bake_pizza ')
    time.sleep(random.randint(1, 5))
    pizza_sem.release()


def cook_spaghetti():
    print(' so u wanna cook_spaghetti ')
    time.sleep(random.randint(1, 5))
    spagy_sem.release()


def buy_chicken_bake():
    print(' so u wanna buy_chicken_bake ')
    time.sleep(random.randint(1, 5))
    costco_sem.release()


def main():
    semaphore_dict = {
        'pizza_sem': False,
        'spagy_sem': False,
        'costco_sem': False
    }
    while 1:
        if not pizza_sem.acquire(blocking=False):
            print('waiting for pizza_sem...')
        else:
            semaphore_dict['pizza_sem'] = True
            print('we got pizza_sem!!!!')
        if not spagy_sem.acquire(blocking=False):
            print('waiting for spagy_sem...')
        else:
            print('we got spagy_sem!!!!')
        if not costco_sem.acquire(blocking=False):
            print('waiting for costco_sem...')
        else:
            print('we got costco_sem!!!!')
        time.sleep(2)


# we have 3 semaphores to wait on
# we need to know when all 3 have finished
# when all 3 finish we go bye


t1 = threading.Thread(target=bake_pizza)
t2 = threading.Thread(target=cook_spaghetti)
t3 = threading.Thread(target=buy_chicken_bake)
t4 = threading.Thread(target=main)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

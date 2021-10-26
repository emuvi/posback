import threading
import time


test_global = "STARTED"
test_index = 0


def print_global():
    while True:
        print(test_global)
        time.sleep(1)


def change_global():
    global test_index
    global test_global
    while True:
        time.sleep(3)
        test_index += 1
        test_global = "ITERATION " + str(test_index)


if __name__ == "__main__":
    t1 = threading.Thread(target=print_global)
    t1.start()
    t2 = threading.Thread(target=change_global)
    t2.start()
    t1.join()
    t2.join()
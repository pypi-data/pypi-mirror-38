import psutil
import os
import threading
import time


def worker_thread(stop_event, load_share):
    if load_share<0 or load_share>1:
        raise ValueError("load_share 0<=x<=1 instead:{}".format(load_share))

    values = []

    while not stop_event.is_set():
        start = time.time()

        result = 0
        while not stop_event.is_set() and (start+load_share)>time.time():
            for i in range(100):
                result += i
            values.append(result)

        stop_event.wait(1-(time.time()-start))

    return result

def start_worker(stop_event, amount):
    worker = []
    for i in range(amount):
        load_share = (i+1) / ((amount+1)*2)
        t = threading.Thread(target=worker_thread, args=(stop_event, load_share,))
        worker.append(t)

    for t in worker:
        t.start()

    return worker

def main():
    process = psutil.Process(os.getpid())
    stop_event = threading.Event()
    worker = start_worker(stop_event, 5)
    try:
        while True:
            time.sleep(1)
            print("process", process,
                  "children", process.children(recursive=True),
                  "cpu process", round(process.cpu_percent() / psutil.cpu_count(), 1),
                  "cpu system", round(psutil.cpu_percent(), 1),
                  "system memory percentage", round(psutil.virtual_memory().available / psutil.virtual_memory().total * 100, 1),
                  "process memory percentage", round(process.memory_percent(), 1),
                  "rss", round(process.memory_info().rss/1024/1024,1),
                  "vms", round(process.memory_info().vms/1024/1024,1),
                  )
    except KeyboardInterrupt:
        pass
    stop_event.set()
    for thread in worker:
        thread.join()

main()


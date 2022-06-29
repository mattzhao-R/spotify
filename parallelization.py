from multiprocessing import Queue, cpu_count
from threading import Thread
from time import sleep
from numpy.random import randint
import logging

import dev_creds
import methods
import objects

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def parallel(full_data,function)
    logger = logging.getLogger(__name__)

    full_data.append("STOP")

    data_queue = Queue()
    worker_queue = Queue()

    worker_ids = list(range(5)) 
    workers = {i: sp_worker(i) for i in worker_ids}
    for worker_id in worker_ids:
        worker_queue.put(worker_id)


    def worker_task(worker, data):
        function(worker, data)


    def queue_listener(data_queue, worker_queue):
        logger.info("Func worker started")
        while True:
            current_data = data_queue.get()
            if current_data == 'STOP':
                # If a stop is encountered then kill the current worker and put the stop back onto the queue
                # to poison other workers listening on the queue
                logger.warning("STOP encountered, killing worker thread")
                data_queue.put(current_data)
                break
            else:
                logger.info(f"Got the item {current_data} on the data queue")
            # Get the ID of any currently free workers from the worker queue
            worker_id = worker_queue.get()
            worker = workers[worker_id]
            # Assign current worker and current data to function
            worker_task(worker, current_data)
            # Put the worker back into the worker queue as  it has completed it's task
            worker_queue.put(worker_id)
        return


    # Create one new queue listener thread per  worker and start them
    logger.info("Starting background processes")
    processes = [Thread(target=queue_listener,
                                 args=(data_queue, worker_queue)) for _ in worker_ids]
    for p in processes:
        p.daemon = True
        p.start()

    # Add each item of data to the data queue, this could be done over time so long as the queue listening
    # processes are still running
    logger.info("Adding data to data queue")
    for d in full_data:
        full_data.put(d)

    # Wait for all queue listening processes to complete, this happens when the queue listener returns
    logger.info("Waiting for Queue listener threads to complete")
    for p in processes:
        p.join()

    # Quit all the web workers elegantly in the background
    logger.info("Tearing down workers")
    for b in workers.values():
        b.quit()

    print(end-start, " iterations took", time.time()-start_time, "to run")


def blank():
    pass


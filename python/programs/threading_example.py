import threading
import time

def monitor_and_auto_save(arg):
    for i in range(3):
        print(f'Auto-saving {arg}...')
        time.sleep(1)
    raise Exception("Simulated crash")

def thread_manager():
    while True:
        t1 = threading.Thread(target=monitor_and_auto_save, args=('data',), daemon=True, name='auto_save')
        t1.start()
        print('Thread was started.')

        # Wait for the thread to complete
        t1.join()

        # If the thread has finished and we reach here, restart it
        print('Thread has completed or crashed. Restarting...')

# Start the thread manager in a non-daemon thread
thread_manager_thread = threading.Thread(target=thread_manager)
thread_manager_thread.start()

# Let the main program run for a while to observe the behavior
time.sleep(10)
print('Main program exiting.')


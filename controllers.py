from threading import Thread

from work import start_thread, print_last_file_name
from work_with_xls import main

# Start multiple threads
def run_main_loop():
    while True:
        main()

num_threads = 5
threads = [Thread(target=start_thread) for _ in range(num_threads - 1)]
threads.append(Thread(target=print_last_file_name))
threads.append(Thread(target=run_main_loop))
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
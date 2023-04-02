import logging
from data import login_name, password, friend
from skpy import Skype, SkypeFileMsg
import os.path
import time
from threading import Thread, Lock

# Set up logging to display messages in console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the Skype connection
sk = Skype(login_name, password)
ch = sk.chats['8:' + friend]

# Define a function to handle new messages
def handle_message(event):
    msg = event.msg
    if msg.chat == ch and isinstance(msg, SkypeFileMsg):
        with open(os.path.join("Documents/", msg.file.name), "wb") as f:
            f.write(msg.fileContent)  # Write the file to disk.
        logging.info("New message received: %s", msg.content)

        # Check if the file name contains an extension
        if "." in msg.file.name:
            # Get the file name without the extension
            file_name = os.path.splitext(msg.file.name)[0]
        else:
            file_name = msg.file.name

        # Send a response in Skype
        ch.sendMsg(f"(1f4be_floppydisk) File saved: {file_name} ✅")

        return file_name
    return None

last_downloaded_file = None
last_downloaded_file_lock = Lock()

# Define a function to print the last downloaded file name
def print_last_file_name():
    global last_downloaded_file
    while True:
        with last_downloaded_file_lock:
            logging.info("Last downloaded file: %s", last_downloaded_file)
        time.sleep(5)

# Define a function to start a new thread for handling messages
def start_thread():
    global last_downloaded_file
    while True:
        # Check for new events
        events = sk.getEvents()
        for event in events:
            if event.type == "NewMessage":
                file_name = handle_message(event)
                if file_name:
                    with last_downloaded_file_lock:
                        last_downloaded_file = file_name
        # Wait for a bit before polling again
        time.sleep(1)

# Start multiple threads
num_threads = 5
threads = [Thread(target=start_thread) for _ in range(num_threads - 1)]
threads.append(Thread(target=print_last_file_name))
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

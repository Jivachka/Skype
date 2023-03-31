from data import login_name, password, friend
from skpy import Skype
import os.path
import time
from threading import Thread


# Set up the Skype connection
sk = Skype(login_name, password)
ch = sk.chats['8:' + friend]

# Define a function to handle new messages
def handle_message(msg):
    if msg.chat == ch:
        with open(os.path.join("Documents/", msg.file.name), "wb") as f:
            f.write(msg.fileContent)  # Write the file to disk.
        print("New message received: ", msg.content)

# Define a function to start a new thread for handling messages
def start_thread():
    while True:
        # Check for new events
        events = sk.getEvents()
        for event in events:
            if event.type == "NewMessage":
                handle_message(event.msg)
        # Wait for a bit before polling again
        time.sleep(1)

# Start multiple threads
num_threads = 5
threads = [Thread(target=start_thread) for _ in range(num_threads)]
for t in threads:
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()

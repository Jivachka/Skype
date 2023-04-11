import logging
from data import login_name, password, allowed_friends
from skpy import Skype, SkypeFileMsg, SkypeNewMessageEvent
import os.path
import time
from threading import Lock

# Set up logging to display messages in console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up the Skype connection
sk = Skype(login_name, password)

# Define a function to handle new messages
def is_allowed_friend(friend_id):
    return friend_id in allowed_friends

def save_file(file_msg):
    with open(os.path.join("Documents/", file_msg.file.name), "wb") as f:
        f.write(file_msg.fileContent)  # Write the file to disk.

def get_file_name(file_msg):
    if "." in file_msg.file.name:
        return os.path.splitext(file_msg.file.name)[0]
    else:
        return file_msg.file.name

def send_response(chat, file_name):
    chat.sendMsg(f"(1f4be_floppydisk) File saved: {file_name} ✅")

def handle_message(event):
    msg = event.msg
    friend_id = msg.user.id
    ch = msg.chat

    if isinstance(msg, SkypeFileMsg) and is_allowed_friend(friend_id):
        save_file(msg)
        logging.info("New message received: %s", msg.content)
        file_name = get_file_name(msg)
        send_response(ch, file_name)
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
            if isinstance(event, SkypeNewMessageEvent):
                file_name = handle_message(event)
                if file_name:
                    with last_downloaded_file_lock:
                        last_downloaded_file = file_name
        # Wait for a bit before polling again
        time.sleep(1)


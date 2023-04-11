import logging
from data import allowed_friends
from skpy import Skype, SkypeFileMsg
import os.path
import time
from threading import Thread, Lock



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SkypeFileManager:
    def __init__(self, username, password):
        self.skype = Skype(username, password)
        self.last_downloaded_file = 'File dont download'
        self.last_downloaded_file_lock = Lock()

    def is_allowed_friend(self, friend_id):
        return friend_id in allowed_friends

    def save_file(self, file_msg):
        with open(os.path.join("Documents/", file_msg.file.name), "wb") as f:
            f.write(file_msg.fileContent)

    def get_file_name(self, file_msg):
        if "." in file_msg.file.name:
            return os.path.splitext(file_msg.file.name)[0]
        else:
            return file_msg.file.name

    def send_response(self, chat, file_name):
        chat.sendMsg(f"✅ File saved: (1f4be_floppydisk) \n {file_name} ")

    def handle_message(self, event):
        msg = event.msg
        friend_id = msg.user.id
        ch = msg.chat

        if isinstance(msg, SkypeFileMsg) and self.is_allowed_friend(friend_id):
            self.save_file(msg)
            logging.info("New message received: %s", msg.content)
            file_name = self.get_file_name(msg)
            self.send_response(ch, file_name)
            return file_name
        return None

    def start_thread(self):
        while True:
            events = self.skype.getEvents()
            for event in events:
                if event.type == "NewMessage":
                    file_name = self.handle_message(event)
                    if file_name:
                        with self.last_downloaded_file_lock:
                            self.last_downloaded_file = file_name
            time.sleep(1)

    def print_last_file_name(self):
        while True:
            with self.last_downloaded_file_lock:
                logging.info("Last downloaded file: %s", self.last_downloaded_file)
            time.sleep(5)




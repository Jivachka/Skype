import logging
import os.path
from threading import Thread, Lock

import schedule
from skpy import Skype, SkypeFileMsg

from .data import allowed_friends
from .work_with_xls import BASE_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SkypeFileManager:
    # Этот класс чисто проверяет наличие нового сообщения,
    # и если есть там файл сохраняет в указаное место. И все.
    _SHEDULE_TIME = 5
    _DOCUMENT_FOLDER_PATH = BASE_PATH

    def __init__(self, username, password):
        self._skype = Skype(username, password)
        self._last_downloaded_file = 'File not downloaded'
        self._last_downloaded_file_lock = Lock()
        self._setup_schedule()

    def _setup_schedule(self):
        schedule.every(self._SHEDULE_TIME).seconds.do(self.print_last_file_name)

    def _is_allowed_friend(self, friend_id):
        return friend_id in allowed_friends

    def _save_file(self, file_msg):
        with self._last_downloaded_file_lock:  # Это блокирует выполнение до тех пор, пока другой поток не освободит блокировку
            with open(os.path.join(self._DOCUMENT_FOLDER_PATH, file_msg.file.name), "wb") as f:
                f.write(file_msg.fileContent)


    def _get_file_name(self, file_msg):
        if "." in file_msg.file.name:
            return os.path.splitext(file_msg.file.name)[0]
        else:
            return file_msg.file.name

    def _send_response(self, chat, file_name):
        chat.sendMsg(f"(seenoevil)  File saved: (1f4be_floppydisk) \n {file_name} ")

    def _handle_message(self, event):
        msg = event.msg
        friend_id = msg.user.id
        ch = msg.chat

        if isinstance(msg, SkypeFileMsg) and self._is_allowed_friend(friend_id):
            self._save_file(msg)
            logging.info("New message received: %s", msg.content)
            file_name = self._get_file_name(msg)
            self._send_response(ch, file_name)
            return file_name
        return None

    def start_thread(self):
        while True:
            events = self._skype.getEvents()
            for event in events:
                if event.type == "NewMessage":
                    file_name = self._handle_message(event)
                    if file_name:
                        with self._last_downloaded_file_lock:
                            self._last_downloaded_file = file_name
            schedule.run_pending()

    def print_last_file_name(self):
        with self._last_downloaded_file_lock:
            logging.info("Last downloaded file: %s", self._last_downloaded_file)


import time
import os.path
import skpy
from data import login_name, password, friend
from skpy import Skype
from skpy import SkypeEventLoop


class FolderCreator:
    @staticmethod
    def _data_today():
        _time = time.gmtime()
        return f'{_time.tm_year}_{_time.tm_mon}_{_time.tm_mday}'

    @staticmethod
    def _if_folder_created():
        list_folder = os.listdir('documents/invoice')
        if FolderCreator._data_today() in list_folder:
            return True
        else:
            return False

    @staticmethod
    def create_folder_if():
        if not FolderCreator._if_folder_created():
            os.chdir('documents/invoice')
            os.makedirs(FolderCreator._data_today())
            os.chdir('/')
            print(f'Create new folder {FolderCreator._data_today()}')
        else:
            print('Not need create new folder')

    @staticmethod
    def data():
        if FolderCreator._if_folder_created():
            return FolderCreator._data_today()
        else:
            FolderCreator.create_folder_if()
            return FolderCreator._data_today()

class LoginToSkype(object):
    def __init__(self):
        self._sk = Skype(login_name, password)

    def __enter__(self):
        return self._sk

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class MySkype (SkypeEventLoop):
    def onEvent(self, event):
        if event.type == 'NewMessage':
            print('New NMes')
            return event

class PareservingBasic(LoginToSkype):
    def __init__(self, startswitch_file_name, folder_path):
        # self._sk = obj
        self._ch = ''
        self._msg = ''
        self._startswitch_file_name = startswitch_file_name
        self._folder_path = folder_path
        super(PareservingBasic, self).__init__()

    def _get_last_message(self, friend=friend):
        try:
            self._ch = self._sk.chats['8:' + friend]
            msg = self._ch.getMsgs()[0]
            return msg
        except Exception as e:
            print(e)

    def _if_check(self, check_name):
        try:
            self._msg = self._get_last_message()
            name = self._msg.file.name
            if name.startswith(check_name):
                return True
            else:
                return False
        except AttributeError:
            return False

    def save_to_folder(self):
        if self._if_check(self._startswitch_file_name):
            with open(os.path.join("documents/"+self._folder_path, self._msg.file.name), "wb") as f:
                f.write(self._msg.fileContent)  # Write the file to disk.

class ChecksSaver(PareservingBasic):
    def __init__(self, folder_path='checks/'):
        self._startswitch_file_name = 'Рахунок'
        self._folder_path = folder_path
        super(ChecksSaver, self).__init__(
            startswitch_file_name=self._startswitch_file_name,
            folder_path=self._folder_path
        )

class InvoiceSaver(PareservingBasic):
    def __init__(self, folder_path=f'invoice/{FolderCreator._data_today()}/'):
        self._startswitch_file_name = 'Видаткова'
        self._folder_path = folder_path
        super(InvoiceSaver, self).__init__(
            startswitch_file_name=self._startswitch_file_name,
            folder_path=self._folder_path
        )

    def if_folder_not_create(self):
        if not FolderCreator._if_folder_created():
            FolderCreator.create_folder_if()

class Event:
    def __init__(self):
        self.sk = Skype(login_name, password)

    def get_events(self):
        print('Start loop')
        res = self.sk.getEvents()
        res2 = self.sk.getEvents()
        print('Done loop')
        return [
            res,
            res2
        ]

    def if_new_message(self):
        for i in self.get_events():
            for ii in i:
                if type(ii) == skpy.event.SkypeNewMessageEvent:
                    return i
        return False

    def get_message_id(self):
        events = self.if_new_message()
        if events:
            return events[0].msgId


if __name__ == "__main__":
    WHILE = True
    check = ChecksSaver()
    invoice = InvoiceSaver()
    event = Event()
    while WHILE:
        message_id = event.get_message_id()
        print(message_id)
        time.sleep(3)
        if message_id:
            check.save_to_folder()
            invoice.if_folder_not_create ()
            invoice.save_to_folder()


















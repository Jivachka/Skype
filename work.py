from data import login_name, password, friend
from skpy import Skype
import os.path


class PareservingBasic(object):
    def __init__(self, startswitch_file_name, folder_path):
        self._sk = Skype(login_name, password)  # connect to Skype
        self._ch = ''
        self._msg = ''
        self._startswitch_file_name = startswitch_file_name
        self._folder_path = ''

    def _get_last_message(self, friend=friend):
        try:
            self._ch = self._sk.chats['8:' + friend]
            msg = self._ch.getMsgs()[0]
            return msg
        except Exception as e:
            print(e)

    def _if_check(self, check_name):
        self._msg = self._get_last_message()
        name = self._msg.file.name
        if name.startswith(check_name):
            return True
        else:
            return False
    def save_to_folder(self):
        if self._if_check(self._startswitch_file_name):
            with open(os.path.join("documents/"+self._folder_path, self._msg.file.name), "wb") as f:
                f.write(self._msg.fileContent)  # Write the file to disk.

class ChecksSaver(PareservingBasic):
    def __init__(self, folder_path = 'checks/'):
        self._startswitch_file_name = 'Рахунок'
        self._folder_path = folder_path
        super().__init__(
            startswitch_file_name=self._startswitch_file_name,
            folder_path=self._folder_path
        )

class InvoiceSaver(PareservingBasic):
    def __init__(self, folder_path='invoice/'):
        self._startswitch_file_name = 'Видаткова'
        self._folder_path = folder_path
        super().__init__(
            startswitch_file_name=self._startswitch_file_name,
            folder_path=self._folder_path
        )

if __name__ == "__main__":
    check = ChecksSaver()
    invoce = InvoiceSaver()
    check.save_to_folder()
    invoce.save_to_folder()



















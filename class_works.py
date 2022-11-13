from data import login_name, password, friend
from skpy import Skype
from skpy import SkypeEventLoop

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
            return 'New ess'

if __name__ == '__main__':
    sk = MySkype(login_name, password)
    print(type(sk))
    sk.cycle()
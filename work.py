from data import login_name, password, friend
from skpy import Skype


sk =  Skype(login_name, password)   # connect to Skype
print(sk.user)

ch = sk.chats['8:'+friend]
print(ch.getMsgs())

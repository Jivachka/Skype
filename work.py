from data import login_name, password, friend
from skpy import Skype
import os.path


sk =  Skype(login_name, password)   # connect to Skype
print(sk.user)

ch = sk.chats['8:'+friend]
msg = ch.getMsgs()[0]


with open(os.path.join("", msg.file.name), "wb") as f:
    f.write(msg.fileContent) # Write the file to disk.
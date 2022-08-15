# XMPP protocol implementation on python

##### Table of Contents  
[About](#about)  
[API](#api)  
[Installation](#installation) 


## About
This project simulates an instant messaging application ussing an existing protocol (XMPP) and Python (SLIXMPP library). XMPP is a protocol for streaming XML elements over a network in order to exchange messages and presence information in close to real time. This project is divided on two parts: account administration and communication.

### Account administration
* Register a new account
* Loggin
* Logout
* Delete account

### Communication
* Show all users and status (active/inactive)
* Add a new account to server
* Show contact details
* Private chat
* Group chat
* Presence message (contact status)
* Notification in-app

## API

* Register a new account
```python
# An Iq stanza is created using xep_0077 pluging and forcing registration
Account(user, password, register=True)
```

* Logging
```python
# session_start event handler is used if credentials are correct
# failed_auth event handler is used if credentials are incorrect
Account(user, password)
```

* Logout
```python
# bot is disconnected
Account(user, password).disconnect()
```

* Delete account
```python
# An Iq stanza is created using unreg1 id and remove parameter
Account(user, password, remove=True)
```

* Show user status
```python
# An Iq stanza is created using xep_0012 pluging and getting user inactive time
# If inactive time equals 0, then user is currently active
Communication(user, password, showUserList = True)
# If searching an individual contact
Communication(user, password, showUserList=True, addContact = contactToSearch)
```

* Add a new account
```python
# A Presence stanza is created using type "subscribe"
Communication(user, password, addContact = contactToAdd)
```

* Private chat
```python
# Message event handler is used for receiving messages
# send_message is used for sending messages with type="chat"

Communication(user, password, sendMessage=True, contactToTalk=contactToTalk)
```

* Group chat
```python
# groupchat_message event handler is used for receiving messages
# send_message is used for sending messages with type="groupchat"

Communication(user, password, room=contactToTalk)
```

* Presence message
```python
# A Presence stanza is created with the status parameter

Communication(user, password, status=status)
```

While user is on menu options or on another chat, notifications alerts will be received if another contact messages the user
<div align="center">
<img width="400" height="400" src="https://user-images.githubusercontent.com/28350445/184571651-d5aa180c-cf0e-4f75-bb76-545c90ab540f.png" alt="notifications-inapp" />
<img width="400" height="400" src="https://user-images.githubusercontent.com/28350445/184571972-786c1b51-f493-412c-85c0-deeeb5be9a60.png" alt="notifications-inapp" />
</div>


## Installation
Python is neeed for this project to run. Clone this repository and install the following dependencies:
```
pip install slixmpp=1.6.0
pip install getpass4
pip install aioconsole
pip install asyncio
pip install nest_asyncio
```
Run de project
```
python finalProject.py
```

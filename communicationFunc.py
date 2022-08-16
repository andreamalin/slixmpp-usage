import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import re
from inputimeout import inputimeout, TimeoutOccurred


from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aioconsole import ainput, aprint

'''
Communication bot for communication related functions
'''
class Communication(slixmpp.ClientXMPP):
    def __init__(self, jid, password, showUserList = False, addContact = None, sendMessage = False, contactToTalk = None, room = None, status = None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.contactToTalk = contactToTalk
        self.contactToAdd = addContact
        self.status = status
        self.option = 0
        
        self.room = room
        self.nick = 'amaya'
        
        # Needed plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0012') 
        self.register_plugin('xep_0060')  # pubsub
        self.register_plugin('xep_0199')  # xmpp ping
        self.register_plugin('xep_0045') # group chat

        # Add event handlers as needed
        if (sendMessage):
            self.add_event_handler("session_start", self.start)
            self.add_event_handler("message", self.message)
            self.add_event_handler("roster_update", self.chat_send)
        elif (room != None):
            self.add_event_handler('session_start', self.start_muc)
            self.add_event_handler("groupchat_message", self.muc_message)
            self.add_event_handler("roster_update", self.chat_send_muc)
        elif (status != None):
            self.add_event_handler("session_start", self.start_presence)
            self.add_event_handler("changed_status", self.get_presence)
        elif (showUserList):
            self.add_event_handler("session_start", self.getUserList)
        elif (addContact != None):
            self.add_event_handler("session_start", self.addContact)
        else:
            self.add_event_handler("session_start", self.start_notifications)
            self.add_event_handler("message", self.message)

    '''
    Basic bot start
    '''
    async def start(self, event):
        self.send_presence()
        await self.get_roster()

    '''
    Start chatgroup bot
    '''
    async def start_muc(self, event):
        self.send_presence()
        await self.get_roster()
        self.plugin['xep_0045'].join_muc(self.room, self.nick)

    '''
    Start change presence status bot
    '''
    async def start_presence(self, event):
        self.send_presence()
        await self.update_presence()
        await self.get_roster()
        
    
    '''
    Start notifications bot
    '''
    async def start_notifications(self, event):
        self.send_presence()
        await self.get_roster()

        self.option = await ainput('Ingrese la opcion: ')
        self.disconnect()


    '''
    Send add a new contact request
    -> Sending presence from connected contact to selected contact to add
    '''
    async def addContact(self, event):
        self.send_presence()
        await self.get_roster()

        self.send_presence(pfrom=self.boundjid, pto=self.contactToAdd, ptype="subscribe")

        self.contactToAdd = None
        self.disconnect()
    
    '''
    Get users status list
    -> Show a selected contact status or show complete contacts list
    '''
    async def getUserList(self, event):
        self.send_presence()
        await self.get_roster()

        contactsList = list(self.roster.__getitem__(self.boundjid))

        if (self.contactToAdd != None):
            for contact in contactsList:
                if contact == self.contactToAdd:
                    await self.getUserStatus(contact)
                    self.contactToAdd = None
                    
        else:
            for contact in contactsList:
                await self.getUserStatus(contact)
        print("----"*8)
        self.disconnect()
    
    
    '''
    Get users status
    -> Handle exception if user information is not shared to connected user (not subscribed)
    -> Depending user inactive time, show current status
    '''
    async def getUserStatus(self, contact):
        # https://xmpp.org/extensions/xep-0012.xml
        iq = self.make_iq(id='last1', ifrom=self.boundjid, ito=contact, itype='get')
        iq = self.make_iq_get(queryxmlns='jabber:iq:last', iq=iq)

        try:
            res2= await iq.send()
            posSeconds = str(res2).find("seconds")
            seconds = str(res2)[posSeconds:]
            posFinal = seconds.find("/")
            seconds = seconds[:posFinal]
            inactiveTime = int(re.findall('"([^"]*)"', seconds)[0])

            if (inactiveTime == 0):
                print(contact, "    status: active")
            else:
                print(contact, "    status: inactive")
        except:
            print(contact, 'Oops! No puedes ver la informacion de este contacto')
    
    
    '''
    Get message notification
    -> If user is messaging contact, show it as part of the chat
    -> If user is not messaging contact, show it as a new notification
    '''
    async def message(self, msg):
        if (self.contactToTalk == None) or not (self.contactToTalk in str(msg['from'])):
            await aprint('\n')
            await aprint('*' * 50)
            await aprint(' ' * 15 + 'NOTIFICACION:' + ' ' * 15)
            await aprint(msg['from'],':', msg['body'])
            await aprint('*' * 50)
        else:
            await aprint(msg['from'],':', msg['body'])
    
    '''
    Send a new message on individual chat to selected contact
    '''
    async def chat_send(self, msg):
        something = await ainput('>> ')
        self.recipient = self.contactToTalk
        self.msg = something

        if (something == "BACK"):
            self.disconnect()
        else:
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='chat')
            await self.get_roster()


    '''
    Send a new message on groupal chat to selected room
    '''
    async def chat_send_muc(self, msg):
        something = await ainput('>> ')
        self.recipient = self.room
        self.msg = something

        if (something == "BACK"):
            self.disconnect()
        else:
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='groupchat')
            await self.get_roster()


    '''
    Get groupal chat notification
    -> If user is messaging the room, show it as part of the chat
    -> If user is not messaging the room, show it as a new notification
    '''
    async def muc_message(self, msg):
        if (self.room == None) or not (self.room in str(msg['from'])):
            await aprint('\n')
            await aprint('*' * 50)
            await aprint(' ' * 15 + 'NOTIFICACION:' + ' ' * 15)
            await aprint(msg['from'], '->', msg['mucnick'],':', msg['body'])
            await aprint('*' * 50)
        else:
            await aprint(msg['mucnick'],':', msg['body'])
    
    
    '''
    Update user status
    '''
    async def update_presence(self):
        resp = self.Presence()
        resp["status"] = self.status

        await resp.send()
    
    
    '''
    Get user status if updated
    '''
    async def get_presence(self, resp):
        try:
            status = resp['status']
            if (status != '' and (self.boundjid.user in str(resp['from']))):
                print("Se ha actualizado el status a: ", status)
                self.disconnect()
        except:
            return
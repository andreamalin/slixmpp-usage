import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import re
from inputimeout import inputimeout, TimeoutOccurred


from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath

class Communication(slixmpp.ClientXMPP):
    def __init__(self, jid, password, showUserList = False, addContact = None, sendMessage = False):
        self.contactToAdd = addContact
        slixmpp.ClientXMPP.__init__(self, jid, password)
        
        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0012') 
        self.register_plugin('xep_0060')  # pubsub
        self.register_plugin('xep_0199')  # xmpp ping

        if (sendMessage):
            self.add_event_handler("message", self.message)
            self.add_event_handler("roster_update", self.chat_send)
        elif (showUserList):
            self.add_event_handler("session_start", self.getUserList)
        elif (addContact != None):
            self.add_event_handler("session_start", self.addContact)

        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
    

    async def addContact(self, event):
        self.send_presence()
        await self.get_roster()

        self.send_presence(pfrom=self.boundjid, pto=self.contactToAdd, ptype="subscribe")

        self.contactToAdd = None
        self.disconnect()
    
    async def getUserList(self, event):
        self.send_presence()
        await self.get_roster()

        contactsList = list(self.roster.__getitem__(self.boundjid))
        for contact in contactsList:
            if (self.contactToAdd != None and contact == self.contactToAdd):
                # https://xmpp.org/extensions/xep-0012.xml
                iq = self.make_iq(id='last1', ifrom=self.boundjid, ito=contact, itype='get')
                iq = self.make_iq_get(queryxmlns='jabber:iq:last', iq=iq)
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
                self.addContact = None
            elif (contact != self.boundjid.bare):
                print('ENTRA ELIIIIIF', contact)
                # https://xmpp.org/extensions/xep-0012.xml
                iq = self.make_iq(id='last1', ifrom=self.boundjid, ito=contact, itype='get')
                iq = self.make_iq_get(queryxmlns='jabber:iq:last', iq=iq)
                print('ENTRA iq', iq)
                res2= await iq.send()
                print('ENTRA res2', res2)
                
                posSeconds = str(res2).find("seconds")
                print('ENTRA posSeconds', posSeconds)
                seconds = str(res2)[posSeconds:]
                posFinal = seconds.find("/")
                seconds = seconds[:posFinal]
                inactiveTime = int(re.findall('"([^"]*)"', seconds)[0])

                if (inactiveTime == 0):
                    print(contact, "    status: active")
                else:
                    print(contact, "    status: inactive")
        print("----"*8)
        self.disconnect()
    
    
    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg['from'],':', msg['body'])

    async def chat_send(self, msg):
        try:
            something = inputimeout(prompt='>>', timeout=10)
            self.recipient = "batouuz@alumchat.fun"
            self.msg = something

            if (something == "BACK"):
                self.disconnect()
            else:
                self.send_message(mto=self.recipient,
                                mbody=self.msg,
                                mtype='chat')
                await self.get_roster()
        except TimeoutOccurred:
            await self.get_roster()

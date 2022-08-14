
import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath

class Account(slixmpp.ClientXMPP):
    def __init__(self, jid, password, remove=False, register=False):
        self.isNewAccount = register
        slixmpp.ClientXMPP.__init__(self, jid, password)

        
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self['xep_0077'].force_registration = True

        if (remove):
            self.add_event_handler("session_start", self.remove)
        else:
            self.add_event_handler("session_start", self.start)
        
        if (register):
            self.add_event_handler("register", self.register)
        
        
        self.add_event_handler("failed_auth", self.failedAuth)

    async def start(self, event):
        print('Sesion iniciada!', self.boundjid.user)
        self.send_presence()
        await self.get_roster()
        self.disconnect()
    
    def failedAuth(self, event):
        if not self.isNewAccount:
            print('Oops! Credenciales incorrectas')
            self.disconnect()

    async def register(self, iq):
        try:
            # Sending register form
            resp = self.Iq()
            resp['type'] = 'set'
            resp['register']['username'] = self.boundjid.user
            resp['register']['password'] = self.password
            await resp.send()
            self.disconnect() # Disconnecting after creating account
        except:
            # Already existing account
            return
    
    async def remove(self, event):
        try:
            self.send_presence()
            await self.get_roster()
            # Sending remove account form
            resp = self.Iq()
            resp['register']['remove'] = True
            resp['type'] = 'set'
            resp['id'] = 'unreg1'
            resp['from'] = self.boundjid

            await resp.send()
            self.disconnect() # Disconnecting after removing account
        except:
            print('Oops! No se pudo eliminar la cuenta')
            return
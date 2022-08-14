import logging
from getpass4 import getpass
from argparse import ArgumentParser
import slixmpp
from time import sleep
from threading import Thread
import asyncio

import nest_asyncio
nest_asyncio.apply()
from inputimeout import inputimeout, TimeoutOccurred


class SendMsgBot(slixmpp.ClientXMPP):
    def __init__(self, jid, pwd):
        slixmpp.ClientXMPP.__init__(self, 'amaya@alumchat.fun', 'Benjamin1')
        self.room = 'batouzuz@conference.alumchat.fun'
        self.nick = 'amaya'

        self.add_event_handler('session_start', self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("roster_update", self.chat_send)

    
    async def muc_message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.
        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] != self.nick :
            print(msg['mucnick'],':', msg['body'])


    async def start(self, event):
        print('start')
        self.send_presence()
        await self.get_roster()
        self.plugin['xep_0045'].join_muc(self.room, self.nick)


    async def chat_send(self, msg):
        try:
            something = inputimeout(prompt='>>', timeout=10)
            self.recipient = self.room
            self.msg = something
            self.send_message(mto=self.recipient,
                            mbody=self.msg,
                            mtype='groupchat')
            await self.get_roster()
        except TimeoutOccurred:
            await self.get_roster()

        

def initSendMsg():
    print('args SendMsgBot')
    sendMsg = SendMsgBot('', '')
    print('pasa SendMsgBot')
    sendMsg.register_plugin('xep_0030')  # service discovery
    sendMsg.register_plugin('xep_0004')  # date form
    sendMsg.register_plugin('xep_0060')  # pubsub
    sendMsg.register_plugin('xep_0199')  # xmpp ping
    # xmpp:batouzuz@conference.alumchat.fun?join
    sendMsg.register_plugin('xep_0045')
    

    print('pasa register')
    sendMsg.connect()
    sendMsg.process(forever=True)

# Setup the command line arguments.
parser = ArgumentParser(description=SendMsgBot.__doc__)

# Output verbosity options.
parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                    action="store_const", dest="loglevel",
                    const=logging.ERROR, default=logging.INFO)
parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                    action="store_const", dest="loglevel",
                    const=logging.DEBUG, default=logging.INFO)

# JID and password options.
parser.add_argument("-j", "--jid", dest="jid",
                    help="JID to use")
parser.add_argument("-p", "--password", dest="password",
                    help="password to use")
parser.add_argument("-t", "--to", dest="to",
                    help="JID to send the message to")
parser.add_argument("-m", "--message", dest="message",
                    help="message to send")

args = parser.parse_args()

logging.basicConfig(level=args.loglevel,
                format='%(levelname)-8s %(message)s')

if args.jid is None:
    args.jid = input("Username: ")
if args.password is None:
    args.password = getpass("Password: ")
initSendMsg()
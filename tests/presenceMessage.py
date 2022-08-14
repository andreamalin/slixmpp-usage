'''
--> remove
'''


import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout


from slixmpp.xmlstream.handler import Callback
from slixmpp.xmlstream.matcher import StanzaPath


class RegisterBot(slixmpp.ClientXMPP):

    """
    A basic bot that will attempt to register an account
    with an XMPP server.
    NOTE: This follows the very basic registration workflow
          from XEP-0077. More advanced server registration
          workflows will need to check for data forms, etc.
    """

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, "amaya@alumchat.fun", "Benjamin1")

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status", self.get_presence)


    async def start(self, event):
        """
        Process the session_start event.
        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.
        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        await self.send_custom_iq()
        res = await self.get_roster()
        # We're only concerned about registering, so nothing more to do here.
        # self.disconnect()

    async def send_custom_iq(self):
        resp = self.Presence()
        resp["status"] = "Llorandooo"

        await resp.send()

    
    async def get_presence(self, resp):
        print("PRESENCEEEEE", resp)


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser()

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

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    # Setup the RegisterBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = RegisterBot(args.jid, args.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()
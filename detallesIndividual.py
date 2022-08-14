#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.
import re
import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp


class CommandBot(slixmpp.ClientXMPP):

    """
    A simple Slixmpp bot that provides a basic
    adhoc command.
    """

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, 'amaya@alumchat.fun', 'Benjamin1')

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

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
        await self.get_roster()
        await self.send_custom_iq(list(self.roster.__getitem__('amaya@alumchat.fun')))


    async def send_custom_iq(self, contactsList):
        print("----INFORMATION ABOUT CONTACT----")
        for contact in contactsList:
            search = "batouuz@alumchat.fun"
            if (contact == search):
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
        print("----"*8)


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

    # Setup the CommandBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = CommandBot(args.jid, args.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0012') 

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()
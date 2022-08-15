from accountFunc import *
from communicationFunc import *

from threading import Thread

from getpass4 import getpass
import asyncio
import nest_asyncio
nest_asyncio.apply()

server = "@alumchat.fun"
muc_server = "@conference.alumchat.fun"

option = 0

print('*' * 50)
print(' ' * 17 + 'BIENVENIDO :)' + ' ' * 17)

async def initialize_bot(user, password):
    global option
    get_notifications = Communication(user, password)
    get_notifications.connect()
    get_notifications.process(forever=False)
    option = int(get_notifications.option)



def loggedInMenu():
    print('*' * 50)
    print('1. Mostrar informacion de contactos')
    print('2. Agregar un contacto')
    print('3. Mostrar detalles de contacto')
    print('4. Chat privado')
    print('5. Chat grupal')
    print('6. Definir mensaje de presencia')
    print('7. Cerrar sesion')
    print('8. Eliminar cuenta')
    print('9. Salir')
    print('-' * 50)

def anonymousMenu():
    print('*' * 50)
    print('1. Registrar una nueva cuenta')
    print('2. Iniciar sesion')
    print('3. Salir')
    print('-' * 50)
    
async def showMenu():
    global option
    loggedAccount = False

    while True:
        print('*' * 50)
        if not (loggedAccount):
            anonymousMenu()

            print('-' * 50)
            option = int(input('Ingrese la opcion: '))
            print('*' * 50)
        else:
            loggedInMenu()
            await initialize_bot(user, password)

        if not (loggedAccount ):
            if (option == 1):
                print('Ingrese la informacion de la nueva cuenta')
                user = input('Username: ')
                user = user+server
                password = getpass('Paswsord: ')

                print('Registrando cuenta...')
                register = Account(user, password, register=True)

                # Connect to the XMPP server and start processing XMPP stanzas.
                register.connect()
                register.process(forever=False)
                print('Cuenta registrada!')
            elif (option == 2):
                print('Ingrese las credenciales')
                user = input('Username: ')
                user = user+server
                password = getpass('Password: ')

                print('Iniciando sesion...', user)
                start = Account(user, password)

                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)

                loggedAccount = start.isLoggedIn
            else:
                print(' ' * 20 + 'ADIOS :)' + ' ' * 20)
                print('*' * 50)
                break
        else:
            print('option ELSEEEE', option, loggedAccount)
            if (option == 1):
                print('Informacion sobre los contactos')
                start = Communication(user, password, showUserList = True)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 2):
                contactToAdd = input('Usuario del contacto: ')
                contactToAdd += server
                start = Communication(user, password, addContact = contactToAdd)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
                print('Contacto agregado :)')
            elif (option == 3):
                contactToSearch = input('Usuario del contacto: ')
                contactToSearch += server
                start = Communication(user, password, showUserList=True, addContact = contactToSearch)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 4):
                contactToTalk = input('Usuario del contacto a mensajear: ')
                contactToTalk += server
                start = Communication(user, password, sendMessage=True, contactToTalk=contactToTalk)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 5):
                contactToTalk = input('Room a mensajear: ')
                contactToTalk += muc_server
                start = Communication(user, password, room=contactToTalk)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 6):
                status = input('Ingrese su status: ')
                start = Communication(user, password, status=status)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 7):
                print('Cerrando sesion de ' + user + '...')
                # Disconnect
                start.disconnect()
                loggedAccount = False
            elif (option == 8):
                confirmation = input('Esta seguro de borrar la cuenta? (Y/N) ')

                if (confirmation == 'Y'):
                    # Connect to the XMPP server and start processing XMPP stanzas.
                    print('Eliminando la cuenta de ', start.boundjid, '...')
                    start = Account(user, password, remove=True)
                    start.connect()
                    start.process(forever=False)
                    loggedAccount = False
                else:
                    print('Error en la confirmacion de borrado')
            else:
                print(' ' * 20 + 'ADIOS :)' + ' ' * 20)
                print('*' * 50)
                break


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(showMenu())
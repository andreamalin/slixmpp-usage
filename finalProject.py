from accountFunc import *
from communicationFunc import *

from getpass4 import getpass
import asyncio
import nest_asyncio
nest_asyncio.apply()

server = "@alumchat.fun"

print('*' * 50)
print(' ' * 17 + 'BIENVENIDO :)' + ' ' * 17)

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
    loggedAccount = False

    while True:
        print('*' * 50)
        if not (loggedAccount):
            anonymousMenu()
        else:
            loggedInMenu()
        print('-' * 50)
        option = int(input('Ingrese la opcion: '))
        print('*' * 50)

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
                break
        else:
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
                start = Communication(user, password, sendMessage=True)
                # Connect to the XMPP server and start processing XMPP stanzas.
                start.connect()
                start.process(forever=False)
            elif (option == 7):
                print('Cerrando sesion de ' + user + '...')
                # Disconnect
                start.disconnect()
                loggedAccount = False
            elif (option == 8):
                # Connect to the XMPP server and start processing XMPP stanzas.
                print('Eliminando la cuenta de ', start.boundjid, '...')
                start = Account(user, password, remove=True)
                start.connect()
                start.process(forever=False)
                loggedAccount = False
            else:
                break


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(showMenu())
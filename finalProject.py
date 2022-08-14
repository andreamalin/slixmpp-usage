from accountFunc import *
from getpass4 import getpass
import asyncio
import nest_asyncio
nest_asyncio.apply()

server = "@alumchat.fun"

print('*' * 50)
print(' ' * 17 + 'BIENVENIDO :)' + ' ' * 17)

async def showMenu():
    while True:
        print('*' * 50)
        print('1. Registrar una nueva cuenta')
        print('2. Iniciar sesion')
        print('3. Cerrar sesion')
        print('4. Eliminar cuenta')
        print('5. Salir')
        print('-' * 50)
        option = int(input('Ingrese la opcion: '))
        print('*' * 50)

        if (option == 1):
            print('Ingrese la informacion de la nueva cuenta')
            user = input('Username: ')
            user = user+server
            password = getpass('Passord: ')

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
            password = getpass('Passord: ')

            print('Iniciando sesion...', user)
            start = Account(user, password)

            # Connect to the XMPP server and start processing XMPP stanzas.
            start.connect()
            start.process(forever=False)
        elif (option == 3):
            print('Cerrando sesion de ' + user + '...')
            # Disconnect
            start.disconnect()
        elif (option == 4):
            # Connect to the XMPP server and start processing XMPP stanzas.
            print('Eliminando la cuenta de ', start.boundjid, '...')
            start = Account(user, password, remove=True)
            start.connect()
            start.process(forever=False)
        else:
            break


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(showMenu())
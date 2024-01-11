import asyncio
import socket
import json

from asyncio import AbstractEventLoop

from orm.models import User
from crud import get_user, db_methods
from utils import check_password


async def authentication_user(connection: socket, loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(connection, 1024):
        data = json.loads(data)
        email, password = data['email'], data['password']
        user = get_user(email)

        if user and check_password(password, user.hashed_password):
            message = 'True'
            loop.create_task(user_choise(connection, loop, user))

        await loop.sock_sendall(connection, message.encode())


async def user_choise(connection: socket, loop: AbstractEventLoop, user: User) -> None:
    while data := await loop.sock_recv(connection, 1024):
        data = json.loads(data)
        choise = data['choise']

        try:
            if data['args']:
                user_args = tuple(data['args'].split())
                db_method = db_methods[choise](user, *user_args)
            else:
                db_method = db_methods[choise](user)

            if db_method:
                await loop.sock_sendall(connection, db_method)
            else:
                message = json.dumps({
                    "response": "Succes",
                })
                await loop.sock_sendall(connection, message.encode())

        except KeyError:
            message = json.dumps({
                "response": "KeyError",
            })
            await loop.sock_sendall(connection, message.encode())


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, addres = await loop.sock_accept(server_socket)
        print(f'New connection {addres}')
        connection.setblocking(False)
        asyncio.create_task(authentication_user(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_addres = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_addres)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())

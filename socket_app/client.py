import asyncio
import json

from textwrap import dedent


async def tcp_client() -> None:
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8000)
    user_email = input('Введите почту: \n')
    user_password = input('Введите пароль: \n')
    user_option = {
        'email': user_email,
        'password': user_password,
    }

    user_auth_bytes = json.dumps(user_option).encode()
    writer.write(user_auth_bytes)
    await writer.drain()
    data = await reader.read(1024)

    response = data.decode()
    if response != 'False':
        while True:
            message = dedent('''\
                Добро пожаловать! Выберите опцию:
                - 1. Создать виртуальную машину: RAM и CPU +
                - 2. Список доступных виртуальных машин
                - 3. Обновить данные для текущего пользователя: новая почта и пароль
                - 4. Список жестких дисков с их параметрами
                - 5. Удалить виртуальную машину по ID: ID виртуальной машины
                - 6. Статистика по всем виртуальным машинам
                - 0. Выход из сервера

                Введите номер опции:
            ''')
            choise_option = input(message)

            if choise_option == "0":
                writer.close()
                await writer.wait_closed()
                break

            message = 'Введите аргументы опции: '
            args_option = input(message)

            user_option = {
                'choise': choise_option,
                'args': args_option,
            }
            user_option_bytes = json.dumps(user_option).encode()
            writer.write(user_option_bytes)
            await writer.drain()
            data = await reader.read(1024)
            print(json.loads(data))

asyncio.run(tcp_client())

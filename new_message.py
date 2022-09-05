import os.path
import telethon.tl.types
from conf import conf
from telethon import TelegramClient, functions, events, sync


def get_new_message():  # запустить бота и ждать получение новых сообщений из каналов
    client = TelegramClient('session_name', conf['api_id'], conf['api_hash'])
    client.start()
    if not os.path.isdir("new message"):  # создать папку
        os.mkdir("new message")
    channels = [chat[0] for chat in get_list_channel(conf['file_new_message'])]  # получить список каналов из txt файла
    [client(functions.channels.JoinChannelRequest(channel=chat)) for chat in channels]  # присоединиться ко всем каналам

    @client.on(events.NewMessage(chats=channels))  # пришло новое сообщение
    async def start(event):
        message = event.message.message
        if message == '' or message is None:  # сообщение содержит текст
            return
        chat = await event.get_chat()  # название чата
        if os.path.isfile(f'new message/{chat.title}.txt'):  # найти или создать файл с текущим каналом
            file = open(f'new message/{chat.title}.txt', 'a', encoding='utf8')
        else:
            file = open(f'new message/{chat.title}.txt', 'w', encoding='utf8')
        date = event.message.date
        sender = await event.get_sender()
        file_write(message, file, date, sender)  # записать сообщение, отправителя, дату
        file.close()
    client.run_until_disconnected()


def get_list_channel(file):  # получить список каналов из txt файла
    file = open(f'{file}', 'r')
    channels = []
    for line in file:
        try:
            channels.append(line.split('\n')[0].split())
        except:
            continue
    file.close()
    return channels


def file_write(message, file, date, sender):  # запись сообщения в файл
    if isinstance(sender, telethon.tl.types.User):  # если отправил пользователь а не сам канал указать отправителя
        if sender.last_name is None:
            sender.last_name = ''
        send = ' '.join(f'{sender.first_name} {sender.last_name} (@{sender.username})'.split()) + '\n'
    else:
        send = ''
    entry = f'{send}{message}\n{date}\n{"." * 100}\n'
    file.write(entry)


if __name__ == '__main__':
    get_new_message()

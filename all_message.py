import os.path
from conf import conf
import telethon.tl.types
from telethon import TelegramClient, events, sync

client = TelegramClient('session_name', conf['api_id'], conf['api_hash'])
client.start()


def get_list_channel(file):  # получение списка каналов из txt файла
    file = open(f'{file}', 'r')
    channels = []
    for line in file:
        try:
            channels.append(line.split('\n')[0].split())
        except:
            continue
    file.close()
    return channels


def file_write(message, file, date, sender):  # записать в созданный файл сообщение
    if isinstance(sender, telethon.tl.types.User):  # если отправил пользователь а не сам канал указать отправителя
        if sender.last_name is None:
            sender.last_name = ''
        send = ' '.join(f'{sender.first_name} {sender.last_name} (@{sender.username})'.split()) + '\n'
    else:
        send = ''
    entry = f'{send}{message}\n{date}\n{"." * 100}\n'
    file.write(entry)


def get_all_message():
    if not os.path.isdir("all message"):  # создать папку если её нет
        os.mkdir("all message")

    for channel in get_list_channel(conf['file_all_message']):  # проход по всем каналам из conf(txt файл)
        chat = client.get_entity(channel[0])
        file = open(f'all message/{chat.title}.txt', 'w', encoding='utf8')  # создать файл с название канала

        if len(channel) > 1:  # указан ли лимит в файле (https://t.me/... 1000 или https://t.me/...)
            limit = int(channel[1])
        else:
            limit = None

        history = client.get_messages(channel[0], limit=limit)  # получение истории канала
        for messages in history:
            message = messages.message
            if message == '' or message is None:  # сообщение состоит из текста
                continue
            date = messages.date
            sender = messages.sender
            file_write(message, file, date, sender)
        file.close()


if __name__ == '__main__':
    get_all_message()

import os
import re

import telebot
import vk_api
from telebot import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from vk_api import audio
from yandex_music import Client


def download(fullName, title):
    client = Client('AQAAAAAiUoaXAAG8XoQcQe1670dHgPP2Pt0jZVU').init()
    search_result = client.search(fullName)
    search_result.best.result.download(title)
    pass


def downloadMessage(message_chat_id, message_text, int):
    path = ''
    if int == 0:
        path = SPlink(message_text)
    elif int == 1:
        path = VKlink(message_text)
    elif int == 2:
        path = YAlink(message_text)
    elif int == 3:
        download(message_text, message_text)
        path = message_text
    path = f'\Yubot111-main\{path}'
    audiofile = open(path, 'rb')
    bot.send_audio(message_chat_id, audiofile)
    audiofile.close()
    os.remove(path)
    pass


def standartExeptMessage(message_chat_id):
    bot.send_message(message_chat_id, "что-то пошло не так")
    bot.send_sticker(message_chat_id, 'CAACAgIAAxkBAAEEAmNiGkgDcTEpshLkrNb2iJSEN7qTXwACxA8AAhVnoUoTrHadeZtE1yME')
    pass


def SPlink(link):
    cid = 'e5e3ea8106e148a3874e28586ca02d20'
    secret = '8c819ced162f421cba60821164edf666'
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    result = sp.track(link)
    name = result['name']
    artist = result['album']['artists'][0]['name']
    fullName = name + " " + artist
    title = name + "." + " " + artist
    download(fullName, title)
    return title
    pass


def VKlink(link):
    vk_session = vk_api.VkApi('+79252443675', 'E13032006')
    vk_session.auth()
    owner_id = '369422109'
    vk_audio = audio.VkAudio(vk_session)
    track_ = re.sub(r"https://vk.com/audio", "", link)
    track_ = track_.split('_')
    track_id = track_[1]
    artist = vk_audio.get_audio_by_id(owner_id, track_id)['artist']
    track = vk_audio.get_audio_by_id(owner_id, track_id)['title']
    fullName = track + " " + artist
    title = track + "." + artist
    download(fullName, title)
    return track + "." + artist
    pass


def YAlink(link):
    client = Client('AQAAAAAiUoaXAAG8XoQcQe1670dHgPP2Pt0jZVU').init()
    link = re.sub(r'https://music.yandex.ru/album/', "", link)
    link = link.split('/track/')
    trackID = link[1]
    name = client.tracks(trackID)
    name = name[0]
    track = name['title']
    artist = name['artists'][0]['name']
    fullName = track + " " + artist
    title = track + "." + artist
    download(fullName, title)
    return title
    pass


def downloadListSP(link, message_chat_id):
    cid = 'e5e3ea8106e148a3874e28586ca02d20'
    secret = '8c819ced162f421cba60821164edf666'
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    result = sp.album(link)
    nameList = result['name']
    nameArtist = result['artists'][0]['name']
    ii = result['total_tracks']
    i = 0
    bot.send_message(message_chat_id, f'Name: {nameList}\nTracks: {ii}')
    while i < ii:
        track = result['tracks']['items'][i]['name']
        i = i + 1
        fullName = track + " " + nameArtist
        title = track + "." + nameArtist
        download(fullName, title)
        path = f'\Yubot111-main\{title}'
        audiofile = open(path, 'rb')
        bot.send_audio(message_chat_id, audiofile)
        audiofile.close()
        os.remove(path)
    pass


def downloadListYA(link, message_chat_id):
    link = re.sub(r'https://music.yandex.ru/album/', "", link)
    client = Client('AQAAAAAiUoaXAAG8XoQcQe1670dHgPP2Pt0jZVU').init()
    result = client.albums(link)
    nameList = result[0]['title']
    nameArtist = result[0]['artists'][0]['name']
    ii = result[0]['track_count']
    allTracksResult = client.albums_with_tracks(link)
    i = 0
    bot.send_message(message_chat_id, f'Name: {nameList}\nTracks: {ii}')
    while i < ii:
        track = allTracksResult['volumes'][0][i]['title']
        i = i + 1
        fullName = track + " " + nameArtist
        title = track + "." + nameArtist
        download(fullName, title)
        path = f'\Yubot111-main\{title}'
        audiofile = open(path, 'rb')
        bot.send_audio(message_chat_id, audiofile)
        audiofile.close()
        os.remove(path)
    pass


bot = telebot.TeleBot('5266363672:AAEyg1z8QrEwfS31bJUhGybWZs7zpveD7wY')


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button2 = types.InlineKeyboardButton("Привет", callback_data="one")
    keyboard.add(url_button2)

    bot.send_message(message.chat.id,
                     f'Приветствую тебя, {message.from_user.first_name}!\nНажми на кнопку или напиши боту привет.\n\nКоманды:\n/start\n/help\nСсылка на трек Spotify\nСсылка на трек VK\nСсылка на трек Яндекс.Музыка\n/search + название и исполнитель',
                     reply_markup=keyboard)
    pass


@bot.callback_query_handler(func=lambda call: True)
def ans(call):
    kb = types.InlineKeyboardMarkup()
    cid = call.message.chat.id
    mid = call.message.message_id
    if call.data == "one":
        bot.edit_message_text("Привет!", cid, mid, reply_markup=kb, parse_mode='Markdown')
        bot.send_sticker(cid, 'CAACAgIAAxkBAAED3d9iA9h0JjqyriXuL9UROV5chyrnbAACchAAApUOoUoD5m-pWcpgMCME')
    pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAED3d9iA9h0JjqyriXuL9UROV5chyrnbAACchAAApUOoUoD5m-pWcpgMCME')

    elif re.search("https://open.spotify.com/track/*", message.text.lower()):
        try:
            downloadMessage(message.chat.id, message.text, 0)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://vk.com/audio*", message.text.lower()):
        try:
            downloadMessage(message.chat.id, message.text, 1)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://music.yandex.ru/album//track/", re.sub(r'\d', "", message.text.lower())):
        try:
            downloadMessage(message.chat.id, message.text, 2)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search(r"/search*", message.text.lower()):
        try:
            name = re.sub(r"/search ", "", message.text)
            downloadMessage(message.chat.id, name, 3)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://open.spotify.com/album/*", message.text.lower()):
        try:
            downloadListSP(message.text, message.chat.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://music.yandex.ru/album/*", message.text.lower()):
        try:
            downloadListYA(message.text, message.chat.id)
        except:
            standartExeptMessage(message.chat.id)

    pass


bot.infinity_polling()
x = "4203fe84-ec02-41bf-a8e6-ff304f76f077"

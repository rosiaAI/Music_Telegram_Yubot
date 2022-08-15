import re
import time

import spotipy
import telebot
from spotipy.oauth2 import SpotifyClientCredentials
from telebot import types
from yandex_music import Client, DownloadInfo

bot = telebot.TeleBot('5266363672:AAEyg1z8QrEwfS31bJUhGybWZs7zpveD7wY')
client = Client('AQAAAAAiUoaXAAG8XoQcQe1670dHgPP2Pt0jZVU').init()
cid = 'e5e3ea8106e148a3874e28586ca02d20'
secret = '8c819ced162f421cba60821164edf666'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button2 = types.InlineKeyboardButton("Привет", callback_data="one")
    keyboard.add(url_button2)

    bot.send_message(message.chat.id,
                     'Приветствую тебя, ' + message.from_user.first_name + '!\nНажми на кнопку или напиши боту привет.\n\nКоманды:\n/start\n/help\nСсылка на трек или альбом Spotify\nСсылка на трек или альбом Яндекс Музыка\n/search + название и исполнитель',
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
        bot.send_message(message.chat.id,
                         'Я знаю команды:\n/start\n/help\nСсылка на трек или альбом Spotify\nСсылка на трек или альбом Яндекс Музыка\n/search + название и исполнитель')

    elif re.search("https://open.spotify.com/track/*", message.text.lower()):
        try:
            SPlink(message.chat.id, message.text, message.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://music.yandex.ru/album//track/", re.sub(r'\d', "", message.text.lower())):
        try:
            YAlink(message.chat.id, message.text, message.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search(r"/search*", message.text.lower()):
        try:
            name = re.sub(r"/search ", "", message.text)
            search_result = client.search(name)
            trackID = search_result.best.result['id']
            download(message.chat.id, trackID, name, message.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://music.yandex.ru/album/*", message.text.lower()):
        try:
            downloadListYA(message.text, message.chat.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://open.spotify.com/album/*", message.text.lower()):
        try:
            downloadListSP(message.text, message.chat.id)
        except:
            standartExeptMessage(message.chat.id)
    pass


def standartExeptMessage(message_chat_id):
    bot.send_message(message_chat_id, "что-то пошло не так")
    bot.send_sticker(message_chat_id, 'CAACAgIAAxkBAAEEAmNiGkgDcTEpshLkrNb2iJSEN7qTXwACxA8AAhVnoUoTrHadeZtE1yME')
    pass


def download(message_chat_id, trackID, fullName, message_id):
    download_info = client.tracks_download_info(trackID)[0]
    audio = DownloadInfo.get_direct_link(download_info)
    bot.send_audio(message_chat_id, audio, fullName, reply_to_message_id=message_id)
    pass

def downloadList(message_chat_id, trackID, fullName):
    download_info = client.tracks_download_info(trackID)[0]
    audio = DownloadInfo.get_direct_link(download_info)
    bot.send_audio(message_chat_id, audio, fullName)
    pass

def SPlink(message_chat_id, message_text, message_id):
    result = sp.track(message_text)
    name = result['name']
    artist = result['album']['artists'][0]['name']
    fullName = name + " " + artist
    search_result = client.search(fullName)
    trackID = search_result.best.result['id']
    title = name + " - " + artist
    download(message_chat_id, trackID, title, message_id)
    pass


def YAlink(message_chat_id, message_text, message_id):
    link = re.sub(r'https://music.yandex.ru/album/', "", message_text)
    link = link.split('/track/')
    trackID = link[1]
    name = client.tracks(trackID)[0]
    track = name['title']
    artist = name['artists'][0]['name']
    fullName = track + " - " + artist
    download(message_chat_id, trackID, fullName, message_id)
    pass


def downloadListYA(message_text, message_chat_id):
    link = re.sub(r'https://music.yandex.ru/album/', "", message_text)
    result = client.albums(link)
    nameList = result[0]['title']
    nameArtist = result[0]['artists'][0]['name']
    ii = result[0]['track_count']
    allTracksResult = client.albums_with_tracks(link)
    i = 0
    bot.send_message(message_chat_id, f'Name: {nameList}\nTracks: {ii}')
    while i < ii:
        track = allTracksResult['volumes'][0][i]['title']
        fullName = track + " " + nameArtist
        trackID = allTracksResult['volumes'][0][i]['id']
        downloadList(message_chat_id, trackID, fullName)
        i += 1
    pass


def downloadListSP(message_text, message_chat_id):
    link = message_text
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
        search_result = client.search(fullName)
        trackID = search_result.best.result['id']
        downloadList(message_chat_id, trackID, fullName)
        i += 1
    pass


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
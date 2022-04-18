import os
import re
import time

import telebot
import vk_api
from telebot import types
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from vk_api import audio
from yandex_music import Client, DownloadInfo

bot = telebot.TeleBot('5266363672:AAEyg1z8QrEwfS31bJUhGybWZs7zpveD7wY')


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button2 = types.InlineKeyboardButton("Привет", callback_data="one")
    keyboard.add(url_button2)

    bot.send_message(message.chat.id,
                     'Приветствую тебя, ' + message.from_user.first_name + '!\nНажми на кнопку или напиши боту привет.\n\nКоманды:\n/start\n/help\nСсылка на трек Spotify\nСсылка на трек VK\nСсылка на трек Яндекс.Музыка\n/search + название и исполнитель',
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
            SPlink(message.chat.id, message.text, message.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://vk.com/audio*", message.text.lower()):
        try:
            VKlink(message.chat.id, message.text, message.id)
        except:
            standartExeptMessage(message.chat.id)

    elif re.search("https://music.yandex.ru/album//track/", re.sub(r'\d', "", message.text.lower())):
        try:
            print(1)
            YAlink(message.chat.id, message.text, message.id)
        except:
            standartExeptMessage(message.chat.id)

    # elif re.search(r"/search*", message.text.lower()):
    #     try:
    #         name = re.sub(r"/search ", "", message.text)
    #         downloadMessage(message.chat.id, name, 3)
    #     except:
    #         standartExeptMessage(message.chat.id)

    # elif re.search("https://open.spotify.com/album/*", message.text.lower()):
    #     try:
    #         downloadListSP(message.text, message.chat.id)
    #     except:
    #         standartExeptMessage(message.chat.id)
    #
    # elif re.search("https://music.yandex.ru/album/*", message.text.lower()):
    #     try:
    #         downloadListYA(message.text, message.chat.id)
    #     except:
    #         standartExeptMessage(message.chat.id)
    pass


client = Client('AQAAAAAiUoaXAAG8XoQcQe1670dHgPP2Pt0jZVU').init()

directory = os.getcwd()


def download(message_chat_id, trackID, fullName, message_id):
    print(5)
    vv = client.tracks_download_info(trackID)[0]
    print(8)
    vvp = DownloadInfo.get_direct_link(vv)
    print(7)
    bot.send_audio(message_chat_id, vvp, fullName, reply_to_message_id=message_id)
    print(6)
    pass


def standartExeptMessage(message_chat_id):
    bot.send_message(message_chat_id, "что-то пошло не так")
    bot.send_sticker(message_chat_id, 'CAACAgIAAxkBAAEEAmNiGkgDcTEpshLkrNb2iJSEN7qTXwACxA8AAhVnoUoTrHadeZtE1yME')
    pass


def SPlink(message_chat_id, message_text, message_id):
    cid = 'e5e3ea8106e148a3874e28586ca02d20'
    secret = '8c819ced162f421cba60821164edf666'
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
    result = sp.track(message_text)
    name = result['name']
    artist = result['album']['artists'][0]['name']
    fullName = name + " " + artist
    search_result = client.search(fullName)
    trackID = search_result.best.result['id']
    title = name + " - " + artist
    download(message_chat_id, trackID, title, message_id)
    pass


def VKlink(message_chat_id, message_text, message_id):
    vk = vk_api.VkApi(token='d066cbded8d87fb0f8d8f365436f0f094f23e859a9b6a09c66a4e3939c740c007ecb702c6a6facbedae7b')
    try:
        vk.http.headers[
            'User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
        vk.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    owner_id = '369422109'
    vk_audio = audio.VkAudio(vk)
    track_ = re.sub(r"https://vk.com/audio", "", message_text)
    track_ = track_.split('_')
    track_id = track_[1]
    artist = vk_audio.get_audio_by_id(owner_id, track_id)['artist']
    track = vk_audio.get_audio_by_id(owner_id, track_id)['title']
    fullName = track + " " + artist
    search_result = client.search(fullName)
    trackID = search_result.best.result['id']
    title = track + " - " + artist
    download(message_chat_id, trackID, title, message_id)
    pass


def YAlink(message_chat_id, message_text, message_id):
    link = re.sub(r'https://music.yandex.ru/album/', "", message_text)
    link = link.split('/track/')
    trackID = link[1]
    print(2)
    name = client.tracks(trackID)[0]
    print(3)
    track = name['title']
    artist = name['artists'][0]['name']
    fullName = track + " - " + artist
    print(4)
    download(message_chat_id, trackID, fullName, message_id)
    pass


# def downloadListSP(link, message_chat_id):
#     cid = 'e5e3ea8106e148a3874e28586ca02d20'
#     secret = '8c819ced162f421cba60821164edf666'
#     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
#     result = sp.album(link)
#     nameList = result['name']
#     nameArtist = result['artists'][0]['name']
#     ii = result['total_tracks']
#     i = 0
#     bot.send_message(message_chat_id, 'Name: ' + nameList + '\nTracks: ' + ii)
#     while i < ii:
#         track = result['tracks']['items'][i]['name']
#         i = i + 1
#         fullName = track + " " + nameArtist
#         title = track + "." + nameArtist
#         download(fullName, title)
#         path = f'{directory}\{title}'
#         audiofile = open(path, 'rb')
#         bot.send_audio(message_chat_id, audiofile)
#         audiofile.close()
#         os.remove(path)
#     pass
#
#
# def downloadListYA(link, message_chat_id):
#     link = re.sub(r'https://music.yandex.ru/album/', "", link)
#     result = client.albums(link)
#     nameList = result[0]['title']
#     nameArtist = result[0]['artists'][0]['name']
#     ii = result[0]['track_count']
#     allTracksResult = client.albums_with_tracks(link)
#     i = 0
#     bot.send_message(message_chat_id, f'Name: {nameList}\nTracks: {ii}')
#     while i < ii:
#         track = allTracksResult['volumes'][0][i]['title']
#         i = i + 1
#         fullName = track + " " + nameArtist
#         title = track + "." + nameArtist
#         download(fullName, title)
#         path = f'{directory}\{title}'
#         audiofile = open(path, 'rb')
#         bot.send_audio(message_chat_id, audiofile)
#         audiofile.close()
#         os.remove(path)
#     pass


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)

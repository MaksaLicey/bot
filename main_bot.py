from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

import requests
import requests

import requests

BOT_TOKEN = "7192682371:AAFae9kqOS_VXje3yvGryzsZ46wVjGh1pWw"
reply_keyboard = [['/rbk', '/tass'],
                  ["/vk"]]
reply_keyboard2 = [["/only_headers"], ["/brief_news"],
                   ["/full_news"], ["/back"]]
markup = None
application = Application.builder().token(BOT_TOKEN).build()
tass1 = 1
news_paper = 1
nums = 0
ende_sls = []


def show_tass():
    global nums
    geocoder_api_server = "https://www.rbc.ru"

    geocoder_params = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng"
                  ",*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language:": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control:": "max-age=0",
        "Connection:": "keep-alive",
        "User-Agent:": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                       " Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0 (Edition Yx GX 03)"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    # print(get(response).json())

    # with open("index.html", 'w') as file:
    #     file.write(response.text)

    soup = BeautifulSoup(response.text, "lxml")

    news = soup.find_all('div', class_='main__big js-main-reload-item')
    news2 = soup.find_all('div', class_='main__feed js-main-reload-item')

    def d1(news):
        global ende_sls
        sls = []
        index = 0
        for n in news:
            sls.append(n.text)
        for new_url in news:
            new_url = new_url.find("a").get("href")
            # print(new_url)  # ссылка на статью
            ende_sls.append([])
            ende_sls[index].append("ссылка на статью: " + str(new_url))
            ende_sls[index].append(str(sls[index]))
            # print(sls[index])
            new_parser = requests.get(new_url, params=geocoder_params)
            new_soup = BeautifulSoup(new_parser.text, "lxml")

            contect = new_soup.find_all('div', class_="article__text__overview")
            for n in contect:
                # print(n.text)  # краткое содержание
                ende_sls[index].append(n.text)
            contect_dop = new_soup.find_all('div', class_="article__text article__text_free")
            for dop_url in contect_dop:
                dop_url = dop_url.find("a").get("href")
                # print("!!!", dop_url)  # доп ссылки
                ende_sls[index].append("доп ссылки: " + str(dop_url))

            for x in contect_dop:
                texts = x.find_all_next('p')
            for text in texts:
                # print(text.get_text())
                ende_sls.append(str(text.get_text()))
            index += 1
        print(ende_sls)

    d1(news)
    d1(news2)


async def help(update, context):
    await update.message.reply_text(
        "Я бот для быстрого просмотра новостей."
        "/start начать поиск"
        "/back вернуться в начальному меню"
        "/statu - посмотреть текущий выбор")



async def start(update, context):
    global markup, news_paper, tass1, ende_sls
    # tass1, news_paper = 1, 1
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        "выберите новостное издание",
        reply_markup=markup

    )


def brief_news(update):
    global tass1, news_paper
    if news_paper != 0:
        tass1 = 2


def only_headerso(update):
    global tass1, news_paper
    if news_paper != 0:
        tass1 = 1


def full_news(update):
    global tass1, news_paper
    if news_paper != 0:
        tass1 = 3


async def stop(update, context):
    await update.message.reply_text(
        "выберите новостное издание",
        reply_markup=markup
    )


async def enter_num(update, context):
    global markup, nums, ende_sls
    text1 = ''
    if ende_sls == []:
        text1 = "введите, сколько последний новостей вы хотите увидеть"
    else:
        for i in ende_sls[0]:
            text1 += i
    await update.message.reply_text(
        text1,
        reply_markup=ReplyKeyboardRemove()
    )
    markup = None
    m = update.message.text
    if markup is None and m[0] != "/":
        try:
            nums = int(m)
            show_tass()
        except:
            pass


async def rbk(update, context):
    global markup, news_paper
    news_paper = 2
    markup = ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=False)
    await update.message.reply_text(
        "выберите формат отображения",
        reply_markup=markup
    )


async def vk(update, context):
    global markup, news_paper
    news_paper = 3


async def tass1(update, context):
    global markup, news_paper
    news_paper = 1


async def status(update, context):
    global tass1, news_paper
    news_paper_ = ''
    statut = ''
    if news_paper == 1: news_paper_ = "TACC"
    if news_paper == 2: news_paper_ = "РБК"
    if news_paper == 3: news_paper_ = "ВК"
    if tass1 == 1: statut = "только заголовки"
    if tass1 == 2: statut = "краткое содежания"
    if tass1 == 3: statut = "полная статья"

    await update.message.reply_text(
        f"выбранное новостное издание: {news_paper_}\n"
        f"вид вывода статьи: {statut}\n"
        f"чтобы вернуться в меню: /back или /start"
    )


def main():
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("back", start))
    application.add_handler(CommandHandler("tass", tass1))
    application.add_handler(CommandHandler("vk", vk))
    application.add_handler(CommandHandler("rbk", rbk))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("only_headers", enter_num))
    application.add_handler(CommandHandler("back", enter_num))
    application.add_handler(CommandHandler("brief_news", enter_num))
    application.add_handler(CommandHandler("full_news", enter_num))
    application.add_handler(CommandHandler("status", status))

    text_handler = MessageHandler(filters.TEXT, enter_num)
    application.add_handler(text_handler)
    # application.add_handler(CommandHandler("brief_news", enter_num))

    application.run_polling()


if __name__ == '__main__':
    main()

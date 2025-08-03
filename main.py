import ptbot
import time
import os
import random
from pytimeparse import parse
from decouple import config

TG_TOKEN = config("TG_TOKEN")
TG_CHAT_ID = "337897610"


def choose(author_id, question, bot):
    message = "Время вышло!"
    bot.send_message(author_id, message)
    print("Мне написал пользователь с ID:", author_id)
    print("Он спрашивал:", question)
    print("Я ответил:", message)


def notify(secs_left, chat_id, message_id, bot):
    bot.update_message(
        chat_id,
        message_id,
        "Осталось {} секунд!".format(secs_left)
        + "\n"
        + render_progressbar(secs_left, 1),
    )


def reply(chat_id, message, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(
        parse(message), notify, chat_id=chat_id, message_id=message_id, bot=bot
    )
    bot.create_timer(
        parse(message), choose, author_id=chat_id, question=message, bot=bot
    )


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == "__main__":
    main()

from polyMediaBot.core.videoParser import VideoParser
#from polyMediaBot.core.logger import Logger
from polyMediaBot.parsers import ParserFactory
from polyMediaBot.utils import download
from polyMediaBot.constants import *

from telegram import (
    Update,
    CallbackQuery,
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)

from telegram.ext import (
    Filters,
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext
)

from threading import Thread
from dataclasses import dataclass
from typing import Any

import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] [%(asctime)s] %(message)s"
)

logger = logging.getLogger(__name__)

@dataclass
class PolyMediaBot:
    updater: Updater
    dispatcher: Any
    state: State
    parser: VideoParser

    def __init__(self, updater: Updater):
        self.updater = updater
        self.dispatcher = self.updater.dispatcher
        self.state = None
        self.parser = None

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text("Please type /download")

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text("Help command!")

    def start_download(self, update: Update, context: CallbackContext):
        keyboard = [
            [
                InlineKeyboardButton("YouTube", callback_data=Parser.YOUTUBE.value), 
                InlineKeyboardButton("Vimeo", callback_data=Parser.VIMEO.value)
            ],
            [InlineKeyboardButton("Instagram", callback_data=Parser.INSTAGRAM.value)]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Choose a page to download a video from"
        update.message.reply_text(message, reply_markup=reply_markup)

        self.state = State.SELECT_PARSER.value
        return self.state

    def select_parser(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        choice = query.data
        self.parser = ParserFactory.get(choice)

        query.edit_message_text(text="Send video url ...")
        self.state = State.PARSING_URL.value
        return self.state

    def parse_url(self, update: Update, context: CallbackContext):
        url = update.message.text
        self.parser.info.url = url

        keyboard = [
            [
                InlineKeyboardButton("Video", callback_data=Type.VIDEO.value), 
                InlineKeyboardButton("Audio", callback_data=Type.AUDIO.value)
            ],
            [InlineKeyboardButton("Gif", callback_data=Type.GIF.value)]
        ] 

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Select type ..."
        update.message.reply_text(message, reply_markup=reply_markup)

        self.state = State.SELECT_TYPE.value
        return self.state


    def select_type(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        file_type = query.data
        self.parser.properties.file_extension = file_type

        if file_type != Type.VIDEO.value:
            self.download(context.bot, query)
            return ConversationHandler.END

        keyboard = [
            [InlineKeyboardButton("High", callback_data=Quality.HIGH.value)],
            [InlineKeyboardButton("Medium", callback_data=Quality.MEDIUM.value)],
            [InlineKeyboardButton("Low", callback_data="240p")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Choose quality ..."
        query.edit_message_text(text=message, reply_markup=reply_markup)

        self.state = State.SELECT_QUALITY.value
        return self.state


    def select_quality(self, update: Update, context: CallbackContext):
        query = update.callback_query
        query.answer()
        quality = query.data

        query.edit_message_text(text="Options parsed!")
        self.parser.properties.resolution = quality
        self.download(context.bot, query)

        return ConversationHandler.END

    def download(self, bot: Any, query: CallbackQuery):
        bot.send_message(chat_id=query.message.chat_id,
                text="Downloading file ...")

        try:
            self.parser.parse()
        except:
            bot.send_message(chat_id=query.message.chat_id,
                    text="Unable to fetch video data!")
            return ConversationHandler.END

        file_type = self.parser.properties.file_extension
        filename = download.download_file(self.parser.info.url, f"file.{file_type}")

        bot.send_message(chat_id=query.message.chat_id,
            text="Sending file ...")

        try:
            bot.send_video(chat_id=query.message.chat_id,
                    video=self.parser.info.url)
        except:
            try:
                bot.send_video(chat_id=query.message.chat_id,
                    video=open(filename, "rb"))
            except Exception as ex:
                print(ex)
                bot.send_message(chat_id=query.message.chat_id,
                    text="File too large! :C")
                return ConversationHandler.END

        bot.send_message(chat_id=query.message.chat_id,
            text="Video sent! :)")
        os.system(f"rm -rf {filename}")

    def cancel(self, update: Update, context: CallbackContext):
        update.message.reply_text("Download cancelled!")
        return ConversationHandler.END

    def _set_commands(self):
        conversation = ConversationHandler(
            entry_points=[CommandHandler("download", self.start_download)],
            states={
                State.SELECT_PARSER.value: [CallbackQueryHandler(self.select_parser)],
                State.PARSING_URL.value: [MessageHandler(Filters.text & ~Filters.command, self.parse_url)],
                State.SELECT_TYPE.value: [CallbackQueryHandler(self.select_type)],
                State.SELECT_QUALITY.value: [CallbackQueryHandler(self.select_quality)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)]
        )

        self.dispatcher.add_handler(conversation)
        self.dispatcher.add_handler(CommandHandler("start", self.start))

    def main(self):
        self._set_commands()
        self.updater.start_polling()
        self.updater.idle()

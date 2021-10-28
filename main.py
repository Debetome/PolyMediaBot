from telegram.ext import Updater
from polyMediaBot import PolyMediaBot

TOKEN = "1604021819:AAFCE5IiSCrqZqG0yY68w5H5qTMaRruZq0s"

if __name__ == '__main__':
    updater = Updater(TOKEN)
    myBot = PolyMediaBot(updater)
    myBot.main()

import cloudscraper
import cryptonator
import datetime

import requests
import telegram
import re

from numerize import numerize
from telegram.ext import *
from telegram import *


import json
import time
import telegram

from bs4 import BeautifulSoup
from requests import Session
import logging

import os
from getp import fpuppy,gen,bunny
from charts import *
from akas import sed_price1,sed_price2,sed_price3






from decimal import *


scraper = cloudscraper.create_scraper()


def sed_price(chat_id,context,vv,ca):
    dates = "%Y-%m-%d %H:%M:%S"
    query = """
    query
    {
      ethereum(network: bsc) {
        dexTrades(
        exchangeName: {in:["Pancake","Pancake v2"]},
        baseCurrency: {is: "%s"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height", "transaction.index"], limit: 1}
        ) {
        block {
            height
            timestamp {
            time(format: "%s")
            }
        }
        transaction {
            index
        }
        baseCurrency {
            symbol
        }
        quoteCurrency {
            symbol
        }
        quotePrice
       }
      }
    }
    """ % (ca, dates)

    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
            'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
            'Content-Type': 'application/json'
        }
    di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades']
    # Price of coin in BNB
    price = di[0]['quotePrice']
    # Coin Symbol
    symbol = di[0]['baseCurrency']['symbol']
    # Quoting and cut out some zero from price bnb
    price_bnb = '{0:.9f}'.format(float(price))
    # Getting current price of bnb
    bnb = cryptonator.get_exchange_rate("bnb", "usd")
    
    # Geting price of coin in usd
    p_usd = '{0:.15f}'.format(float(price))
    pr_usd = float(p_usd)*float(bnb)
    pr = pr_usd
    if pr > 0.001:
        pr = '{0:,.6f}'.format(float(pr))
    else:
        pr = '{0:,.9f}'.format(float(pr))
    #------------------------------------
    #------------------------------------
    #Now let's scrap some data from bscscan.com webpage
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'}
    URL = f"https://bscscan.com/token/{ca}"
    cotractpage = requests.get(URL,headers=headers)
    soupa = BeautifulSoup(cotractpage.content, 'lxml')
    #Getting token holders for the contract provided
    tokenholders = soupa.find(id='ContentPlaceHolder1_tr_tokenHolders').get_text()
    tokenholdersa = "Holders ➜ " + ((((tokenholders.strip()).strip("Holders:")).strip()).strip(" a ")).strip()
    #Now let's grt the coin name from bscscan.com
    name = soupa.find('span', class_='text-secondary small').get_text()
    #Getting total supply of the coin
    total_supply = soupa.find('div', class_='col-md-8').get_text().split('(')[0].strip()   # <--- we want only first part of the string
    #now let get only digits/interger from the strings
    result = ''.join([i for i in total_supply if  i.isdigit()])
    supply_now = numerize.numerize(float(int(result)))
    #--------------------------------------------------
    #--------------------------------------------------
    #Now bscscan done let's calculate the marketcap
    mc = float(pr_usd)*float(result)
    mcap = "${:,.4f}".format(float(mc))
    # MCap to bnb
    mctu = cryptonator.get_exchange_rate("usd", "bnb")
    mc_bn = float(mctu)*float(mc)
    mcap_bnb = numerize.numerize(float(int(mc_bn)))
    #---------------------------------------
    #Getting all data ready for printing
    bsss = "${:,.4f}".format(float(bnb))
    all_msg = f"<b>{name} ({symbol})</b>\n" \
              f"1 <b>{symbol}</b> ➜ $<b>{pr}</b>\n" \
              f"1 <b>{symbol}</b> ➜ <b>{price_bnb} BNB</b>\n" \
              f"<b>BNB Price</b> ➜ <b>{bsss}</b>\n" \
              f"---------------------------------------------\n" \
              f"---------------------------------------------\n" \
              f"<b>Total Supply</b> ➜ <b>{supply_now} {symbol}</b>\n" \
              f"<b>{tokenholdersa}</b>\n" \
              f"<b>MC</b> ➜ {mcap} ({mcap_bnb}) <b>BNB</b>"
    rkey = [[InlineKeyboardButton("Chart", url=f'https://poocoin.app/tokens/{ca}'),InlineKeyboardButton("Buy",url=f"https://poocoin.app/swap/?outputCurrency={ca}")],[InlineKeyboardButton("Back",callback_data="back")]]
    reply_mark = InlineKeyboardMarkup(rkey)
    if ca == "0xa9667d44b0f9d0fb7541869b59203b86bc867249":
        #FPUPPY
        chartfpuppy()
        
        context.bot.send_photo(chat_id=chat_id, photo=open("./fpuppy.png", "rb"),caption=all_msg,parse_mode="html",reply_markup=reply_mark)
        context.bot.deleteMessage (message_id = vv.message_id,
                           chat_id = chat_id)       
    if ca == "0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f":
        #Genshin
        chartgen()
       
        context.bot.send_photo(chat_id=chat_id, photo=open("./gen.png", "rb"),caption=all_msg,parse_mode="html",reply_markup=reply_mark)
        context.bot.deleteMessage (message_id = vv.message_id,
                           chat_id = chat_id)  
    if ca == "0xef98b948d031f1f4f1eb47b7ae999b314707acb5":
        #bunny
        chartbunny()
        
        context.bot.send_photo(chat_id=chat_id, photo=open("./bunny.png", "rb"),caption=all_msg,parse_mode="html",reply_markup=reply_mark)
        context.bot.deleteMessage (message_id = vv.message_id,
                           chat_id = chat_id)  
    
   
            
    
def price(update,context):
    hu = update.message
    kiki = update.message.chat.id
    #print(hu)
    fpupppy = "0xa9667d44b0f9d0fb7541869b59203b86bc867249"
    gen = "0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f"
    bunny = "0xef98b948d031f1f4f1eb47b7ae999b314707acb5"
    key1s = [[InlineKeyboardButton("FFPUPPY",callback_data=f"price {fpupppy}"),InlineKeyboardButton("GENSHIN_GT",callback_data=f"price {gen}")],[InlineKeyboardButton("BunnyRocket",callback_data=f"price {bunny}")],[InlineKeyboardButton("Close",callback_data='close')]]
    mark = InlineKeyboardMarkup(key1s)
    ms = f"GenToken's List"
    update.effective_message.reply_text(ms,parse_mode="markdown",reply_markup=mark)
    time.sleep(60)
    context.bot.deleteMessage (message_id = hu.message_id,
                           chat_id = kiki)
    
def start(update,context):
    update.message.reply_text("Welocme to GenToken's Pricebot\nUsage: /price")  
    
def chart(update,context):
    hu = update.message
    kiki = update.message.chat.id
    #print(hu)
    charts = [[InlineKeyboardButton("FFPUPPY", url='https://poocoin.app/tokens/0xa9667d44b0f9d0fb7541869b59203b86bc867249'),InlineKeyboardButton("GENSHIN_GT",url="https://poocoin.app/tokens/0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f")],[InlineKeyboardButton("BunnyRocket",url="https://poocoin.app/tokens/0xef98b948d031f1f4f1eb47b7ae999b314707acb5")],[InlineKeyboardButton("Close",callback_data="close")]]
    mark = InlineKeyboardMarkup(charts)
    ms = f"GenToken's Charts"
    update.effective_message.reply_text(ms,parse_mode="markdown",reply_markup=mark)
    context.bot.deleteMessage (message_id = hu.message_id,
                           chat_id = kiki)    

 
def contract(update,context):
    hu = update.message
    kiki = update.message.chat.id
    mss = f"<b>BunnyRocket</b>\n<code>0xef98b948d031f1f4f1eb47b7ae999b314707acb5</code>\n\n" \
          f"<b>GENSHIN_GT</b>\n<code>0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f</code>\n\n" \
          f"<b>Floki FrunkPuppy</b>\n<code>0xa9667d44b0f9d0fb7541869b59203b86bc867249</code>" 
    key1s = [[InlineKeyboardButton("Close",callback_data="close")]]
    mark = InlineKeyboardMarkup(key1s)         
    update.effective_message.reply_text(mss,parse_mode="html",reply_markup=mark)
    time.sleep(25)
    context.bot.deleteMessage (message_id = hu.message_id,
                           chat_id = kiki)
    
def refresh(update,context):
    query : CallbackQuery = update.callback_query
    chat_id = update.effective_chat.id
    ch = update.callback_query.data.split()
    if len(ch) ==2:
        ca = ch[1]
        print(ca)
        if query.data == f"price {ca}":
            ms = "<b>Fetching Price</b>"
            vv = query.edit_message_text(text=ms,parse_mode='html')
            sed_price(chat_id,context,vv,ca)
    if len(ch) == 1:
        if query.data == 'close':
            melo =  query.edit_message_text(text='`Closing`',parse_mode='markdown',disable_web_page_preview=True)
            time.sleep(5)
            context.bot.deleteMessage (message_id = melo.message_id,
                           chat_id = chat_id)
            
        if query.data == 'closing':
            context.bot.deleteMessage (message_id = query.data.message_id,
                           chat_id = chat_id)
            
        if query.data == 'back':
            fpupppy = "0xa9667d44b0f9d0fb7541869b59203b86bc867249"
            gen = "0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f"
            bunny = "0xef98b948d031f1f4f1eb47b7ae999b314707acb5"
            key1s = [[InlineKeyboardButton("FFPUPPY",callback_data=f"price {fpupppy}"),InlineKeyboardButton("GENSHIN_GT",callback_data=f"price {gen}")],[InlineKeyboardButton("BunnyRocket",callback_data=f"price {bunny}")],[InlineKeyboardButton("Close",callback_data='close')]]
            mark = InlineKeyboardMarkup(key1s)
            ms = f"GenToken's List"
            query.edit_message_text(ms,parse_mode="markdown",reply_markup=mark)
            
         
        
    
def main() -> None:
    # Create the Updater and pass it your bot's token.
    token = "2098411703:AAE2JqKNUshhKOMAYdhl76cm3W4_7xMd94w"
    updater = Updater(token)
    #dispatcher = updater
    print('started')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('price', price))
    updater.dispatcher.add_handler(CommandHandler('chart', chart))
    updater.dispatcher.add_handler(CommandHandler('contract', contract))
    updater.dispatcher.add_handler(CommandHandler('fpuppy', sed_price2))
    updater.dispatcher.add_handler(CommandHandler('genshin', sed_price3))
    updater.dispatcher.add_handler(CommandHandler('bunny', sed_price1))
    updater.dispatcher.add_handler(CallbackQueryHandler(refresh))
    job_queue = updater.job_queue
    job_queue.run_repeating(bunny, 300)
    job_queue.run_repeating(gen, 600)
    job_queue.run_repeating(fpuppy,  900)
    
   
    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
    
    
if __name__ == '__main__':
    main()
    

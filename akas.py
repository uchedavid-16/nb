import cryptonator
import requests
import json
import time
import telegram

from bs4 import BeautifulSoup
from requests import Session
import logging

import os


import cloudscraper
import cryptonator
import datetime

import requests
import telegram
import re

from numerize import numerize
from telegram.ext import *
from telegram import *

def sed_price1(update,context):
    ca = "0xef98b948d031f1f4f1eb47b7ae999b314707acb5"
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
    print(di)
    # Price of coin in BNB
    price = di[0]['quotePrice']
    # Coin Symbol
    symbol = di[0]['baseCurrency']['symbol']
    # Quoting and cut out some zero from price bnb
    price_bnb = '{0:.16f}'.format(float(price))
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
    #CLACULATING 1 MILLION TOKENS 
    milliont = float(pr_usd)*float("1000000")
    mill = "{:,.9f}".format(float(milliont))
    # CALCULATING 1 MILLION TOKENS IN BNB
    millionbnb = float(price_bnb)*float("1000000")
    milli_bnb = "{:,.9f}".format(float(millionbnb))
    #Getting all data ready for printing
    bsss = "${:,.4f}".format(float(bnb))
    all_msg = f"🎮 <a href='https://t.me/TradeScapeHQ'>{symbol}</a> ({symbol})\n\n" \
              f"⏳ <b>1 {symbol} ➜ ${pr}</b>\n\n" \
              f"📊 <b>1 {symbol} ➜ {price_bnb} BNB</b>\n\n" \
              f"🔔 <b>BNB/USD ➜ {bsss}</b>\n\n" \
              f"🔁 <b>Buy/Sell ➜</b><a href='https://pancakeswap.finance/swap?outputCurrency=0xef98b948d031f1f4f1eb47b7ae999b314707acb5&inputCurrency=BNB'>Pancakeswap</a> || <a href='https://poocoin.app/swap/?outputCurrency=0xef98b948d031f1f4f1eb47b7ae999b314707acb5'>Poocoin</a>\n\n" \
              f"<b>Charts ➜ </b><a href='https://poocoin.app/tokens/0xef98b948d031f1f4f1eb47b7ae999b314707acb5'>Poocoin</a>\n\n" \
              f"<b>{tokenholdersa}</b>\n\n" \
              f"📝 <b>MC</b> ➜ {mcap} ({mcap_bnb}) <b>BNB</b>"
              
    update.message.reply_text(all_msg,parse_mode="html",disable_web_page_preview=True)
              
              
def sed_price2(update,context):
    ca = "0xa9667d44b0f9d0fb7541869b59203b86bc867249"
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
    print(di)
    # Price of coin in BNB
    price = di[0]['quotePrice']
    # Coin Symbol
    symbol = di[0]['baseCurrency']['symbol']
    # Quoting and cut out some zero from price bnb
    price_bnb = '{0:.16f}'.format(float(price))
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
    #CLACULATING 1 MILLION TOKENS 
    milliont = float(pr_usd)*float("1000000")
    mill = "{:,.9f}".format(float(milliont))
    # CALCULATING 1 MILLION TOKENS IN BNB
    millionbnb = float(price_bnb)*float("1000000")
    milli_bnb = "{:,.9f}".format(float(millionbnb))
    #Getting all data ready for printing
    bsss = "${:,.4f}".format(float(bnb))
    all_msg = f"🎮 <a href='https://t.me/TradeScapeHQ'>{symbol}</a> ({symbol})\n\n" \
              f"⏳ <b>1 {symbol} ➜ ${pr}</b>\n\n" \
              f"📊 <b>1 {symbol} ➜ {price_bnb} BNB</b>\n\n" \
              f"🔔 <b>BNB/USD ➜ {bsss}</b>\n\n" \
              f"🔁 <b>Buy/Sell ➜</b><a href='https://pancakeswap.finance/swap?outputCurrency=0xa9667d44b0f9d0fb7541869b59203b86bc867249&inputCurrency=BNB'>Pancakeswap</a> || <a href='https://poocoin.app/swap/?outputCurrency=0xa9667d44b0f9d0fb7541869b59203b86bc867249'>Poocoin</a>\n\n" \
              f"<b>Charts ➜ </b><a href='https://poocoin.app/tokens/0xa9667d44b0f9d0fb7541869b59203b86bc867249'>Poocoin</a>\n\n" \
              f"<b>{tokenholdersa}</b>\n\n" \
              f"📝 <b>MC</b> ➜ {mcap} ({mcap_bnb}) <b>BNB</b>"
              
    update.message.reply_text(all_msg,parse_mode="html",disable_web_page_preview=True)
    
    
    
def sed_price3(update,context):
    ca = "0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f"
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
    print(di)
    # Price of coin in BNB
    price = di[0]['quotePrice']
    # Coin Symbol
    symbol = di[0]['baseCurrency']['symbol']
    # Quoting and cut out some zero from price bnb
    price_bnb = '{0:.16f}'.format(float(price))
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
    #CLACULATING 1 MILLION TOKENS 
    milliont = float(pr_usd)*float("1000000")
    mill = "{:,.9f}".format(float(milliont))
    # CALCULATING 1 MILLION TOKENS IN BNB
    millionbnb = float(price_bnb)*float("1000000")
    milli_bnb = "{:,.9f}".format(float(millionbnb))
    #Getting all data ready for printing
    bsss = "${:,.4f}".format(float(bnb))
    all_msg = f"🎮 <a href='https://t.me/TradeScapeHQ'>{symbol}</a> ({symbol})\n\n" \
              f"⏳ <b>1 {symbol} ➜ ${pr}</b>\n\n" \
              f"📊 <b>1 {symbol} ➜ {price_bnb} BNB</b>\n\n" \
              f"🔔 <b>BNB/USD ➜ {bsss}</b>\n\n" \
              f"🔁 <b>Buy/Sell ➜</b><a href='https://pancakeswap.finance/swap?outputCurrency=0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f&inputCurrency=BNB'>Pancakeswap</a> || <a href='https://poocoin.app/swap/?outputCurrency=0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f'>Poocoin</a>\n\n" \
              f"<b>Charts ➜ </b><a href='https://poocoin.app/tokens/0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f'>Poocoin</a>\n\n" \
              f"<b>{tokenholdersa}</b>\n\n" \
              f"📝 <b>MC</b> ➜ {mcap} ({mcap_bnb}) <b>BNB</b>"
              
    update.message.reply_text(all_msg,parse_mode="html",disable_web_page_preview=True)
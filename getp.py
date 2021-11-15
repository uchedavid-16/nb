
import requests
import json
import csv
import cryptonator
import time
from charts import chartbunny,chartfpuppy,chartgen

tims = []
prss =  []

#FUPPY FPUPPY 

def bunny(context):
    query = """
    query
    {
    ethereum(network: bsc){
        dexTrades(
        baseCurrency: {is: "0xef98b948d031f1f4f1eb47b7ae999b314707acb5"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height","transaction.index"] limit:500}
        ) {
            block{
                height
                timestamp{
                    time (format: "%Y-%m-%d %H:%M:%S")
                }
            }
            transaction {
                index
            }
            baseCurrency{
                symbol
            }
            quoteCurrency {
                symbol
            }
            quotePrice
         }
        }
    }
    """
    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
        'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
        'Content-Type': 'application/json'
        }
    di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades']
    print(di)
    bnb = cryptonator.get_exchange_rate("bnb", "usd")
    with open("bunny.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['Date','Price'])
        for data in di:
            high = data['quotePrice']
            pr = float(high)*float(bnb)
            date = f"{data['block']['timestamp']['time']}+00:00"
            writer.writerow([date,pr])
            
            
      
            
# GENSHIN
def gen(context):
    query = """
    query
    {
    ethereum(network: bsc){
        dexTrades(
        baseCurrency: {is: "0xa516338a2ae891774c8c67e4f974a48f6e1b8d6f"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height","transaction.index"] limit:500}
        ) {
            block{
                height
                timestamp{
                    time (format: "%Y-%m-%d %H:%M:%S")
                }
            }
            transaction {
                index
            }
            baseCurrency{
                symbol
            }
            quoteCurrency {
                symbol
            }
            quotePrice
         }
        }
    }
    """
    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
        'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
        'Content-Type': 'application/json'
        }
    di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades']
    print(di)
    bnb = cryptonator.get_exchange_rate("bnb", "usd")
    with open("gen.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['Date','Price'])
        for data in di:
            high = data['quotePrice']
            pr = float(high)*float(bnb)
            date = f"{data['block']['timestamp']['time']}+00:00"
            writer.writerow([date,pr])
  
  
  
  #fpuppy
  
  
def fpuppy(context):
    query = """
    query
    {
    ethereum(network: bsc){
        dexTrades(
        baseCurrency: {is: "0xa9667d44b0f9d0fb7541869b59203b86bc867249"}
        quoteCurrency: {is: "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"}
        options: {desc: ["block.height","transaction.index"] limit:500}
        ) {
            block{
                height
                timestamp{
                    time (format: "%Y-%m-%d %H:%M:%S")
                }
            }
            transaction {
                index
            }
            baseCurrency{
                symbol
            }
            quoteCurrency {
                symbol
            }
            quotePrice
         }
        }
    }
    """
    d = {'query': query, 'variables': {}}
    payload = json.dumps(d)
    url = "https://graphql.bitquery.io"
    headers = {
        'X-API-KEY': 'BQYxBh0DXYCwroM9PKnGS2tZXWDZhNEx',
        'Content-Type': 'application/json'
        }
    di = requests.request("POST", url, headers=headers, data=payload).json()['data']['ethereum']['dexTrades']
    print(di)
    bnb = cryptonator.get_exchange_rate("bnb", "usd")
    with open("fpuppy.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['Date','Price'])
        for data in di:
            high = data['quotePrice']
            pr = float(high)*float(bnb)
            date = f"{data['block']['timestamp']['time']}+00:00"
            writer.writerow([date,pr])
  

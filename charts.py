import time
import matplotlib.pyplot as plt
import mplfinance as mpf

import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

from PIL import Image
from telegram.ext import *
from telegram import *
import telegram

def chartbunny():
    dataframe = pd.read_csv("./bunny.csv")
    # convert object to datetime64[ns]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]) 
    dates = dataframe["Date"]
    mbps = dataframe["Price"]
    plt.plot(dates, mbps,)
    plt.title("Price Chart BunnyRocket")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid()
    plt.xticks(rotation=45)
    #plt.show() #Preview of chart
    plt.savefig('cbunny.png')
    plt.close()
    #BLENDING TWO IMAGES
    Im = Image.open("cbunny.png")
    newIm = Image.new ("RGBA", (640, 480), (255, 0, 0))
    Im2 = Image.open("safu.png").convert(Im.mode)
    Im2 = Im2.resize(Im.size)
    img = Image.blend(Im,Im2,0.2)
    img.save('bunny.png')
    
    
# FPUUPY

def chartfpuppy():
    dataframe = pd.read_csv("./fpuppy.csv")
    # convert object to datetime64[ns]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]) 
    dates = dataframe["Date"]
    mbps = dataframe["Price"]
    plt.plot(dates, mbps,)
    plt.title("Price Chart Floki FrunkPuppy")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid()
    plt.xticks(rotation=45)
    #plt.show() #Preview of chart
    plt.savefig('cfpuppy.png')
    plt.close()
    time.sleep(10)
    #BLENDING TWO IMAGES
    Im = Image.open("cfpuppy.png")
    newIm = Image.new ("RGBA", (640, 480), (255, 0, 0))
    Im2 = Image.open("safu.png").convert(Im.mode)
    Im2 = Im2.resize(Im.size)
    img = Image.blend(Im,Im2,0.2)
    img.save('fpuppy.png')
    
    
    #GEN GEN
    
    
def chartgen():
    dataframe = pd.read_csv("./gen.csv")
    # convert object to datetime64[ns]
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]) 
    dates = dataframe["Date"]
    mbps = dataframe["Price"]
    plt.plot(dates, mbps,)
    plt.title("Price Chart GENSHIN_GT")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid()
    plt.xticks(rotation=45)
    #plt.show() #Preview of chart
    plt.savefig('cgen.png')
    plt.close()
    time.sleep(10)
    #BLENDING TWO IMAGES
    Im = Image.open("cgen.png")
    newIm = Image.new ("RGBA", (640, 480), (255, 0, 0))
    Im2 = Image.open("safu.png").convert(Im.mode)
    Im2 = Im2.resize(Im.size)
    img = Image.blend(Im,Im2,0.2)
    img.save('gen.png')


    

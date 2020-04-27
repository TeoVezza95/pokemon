#!/usr/bin/env python
import sys



def mapping():
    lines = sys.stdin.readlines()
    Ticker_sector = {}
    for line in lines:
        line = line.strip()
        splits = line.split(",")
        if splits[0] == "ticker":
            continue
        if len(splits) == 8:
            Ticker,CloseValue, LowThe, HighThe, Volume, Date=historical_stock_prices(splits)
            year = Date.split("-")[0]
            if year >= '2008':
                sector = Ticker_sector.get(Ticker)
                print(Ticker,CloseValue, LowThe, HighThe, Volume, Date, sector, sep='\t')
        else:
            Ticker,Sector=historical_stocks(splits)
            Ticker_sector[Ticker] = Ticker_sector.get(Ticker, []) + [Sector]


def historical_stocks(splits):
    if len(splits) == 5:
        Ticker = splits[0]
        Sector = splits[3]
    else:
        Ticker = splits[0]
        if len(splits) <= 7:
            if ':' in splits[len(splits)-2]:
                posSect=len(splits)-3
            else:
                posSect= len(splits)-2
        else:
            posSect = len(splits) - 3
        Sector = splits[posSect]
    return Ticker,Sector

def historical_stock_prices(splits):
    Ticker = splits[0]
    CloseValue = splits[2]
    LowThe = splits[4]
    HighThe = splits[5]
    Volume = splits[6]
    Date = splits[7]
    return Ticker,CloseValue, LowThe, HighThe, Volume, Date

if __name__ == '__main__':
    mapping()

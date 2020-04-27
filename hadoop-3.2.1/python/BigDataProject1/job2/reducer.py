#!/usr/bin/env python
import sys
import time


def reducer():
    #sectorDict = {}
    listOfOutputs = []
    sectorDict=createDict()

    for key, value in sectorDict.items():
        for sy_key, sy_value in value.items():
            finalVolume = (sy_value['totVolumes']) / (sy_value['numbersOfTicker'])
            totXCen = 0
            totQuot = 0
            for currentTicker in sy_value['ticker'].values():
                quot = currentTicker['totDailyQuo'] / currentTicker['totDays']
                first = currentTicker['start'][1]
                last = currentTicker['finish'][1]
                xCen = ((last - first) / first) * 100
                totXCen += xCen
                totQuot += quot
            finalQuot = totQuot / len(sy_value['ticker'])
            finalXCen = round(totXCen / len(sy_value['ticker']), 2)
            listOfOutputs.append(((key,sy_key,str(finalXCen) + "%", str(finalQuot),str(finalVolume)), key))
    sortedOutput = sorted(listOfOutputs, key=lambda x: x[1], reverse=False)
    print(f'{"SETTORE":30} | {"ANNO":30} | {"VARIAZIONE ANNUALE MEDIA":30} | {"QUOTAZIONE MEDIA GIORNALIERA":30} | {"VOLUME MEDIO ANNUALE ":30} \n')

    for output in sortedOutput:
        print(f'{output[0][0]:30} | {output[0][1]:30} | {output[0][2]:30} | {output[0][3]:30} | {output[0][4]:25} ')


def updateQuote(ticker, low, high):
    q = (float(low) + float(high)) / 2.0
    ticker['totDailyQuo'] += q
    ticker['totDays'] += 1


def updateVariance(ticker, Date, CloseValue):
    if Date < ticker['start'][0]:
        ticker['start'][0] = Date
        ticker['start'][1] = float(CloseValue)
    if Date > ticker['finish'][0]:
        ticker['finish'][0] = Date
        ticker['finish'][1] = float(CloseValue)

def createDict():
    sectorDict={}
    for line in sys.stdin.readlines():
        Ticker, CloseValue, LowThe, HighThe, Volume, Date, Sector = line.strip().split("\t")
        try:
            sector = sectorDict[Sector]
        except KeyError:
            sectorDict[Sector] = {}
            sector = sectorDict[Sector]
        year = Date.split("-")[0]
        try:
            sector_year = sector[year]
        except KeyError:
            sector[year] = {'numbersOfTicker': 0, 'totVolumes': 0, 'ticker': {}}
            sector_year = sector[year]
        try:
            ticker = sector_year['ticker'][Ticker]
        except KeyError:
            sector_year['ticker'][Ticker] = {'start': ['2100-01-01', 0],'finish': ['2000-01-01', 0],'totDailyQuo': 0,'totDays': 0}
            ticker = sector_year['ticker'][Ticker]
        updateQuote(ticker, LowThe, HighThe)
        updateVariance(ticker, Date, CloseValue)
        sector_year['numbersOfTicker'] += 1
        sector_year['totVolumes'] += (float(Volume))
    return sectorDict

if __name__ == '__main__':
    reducer()
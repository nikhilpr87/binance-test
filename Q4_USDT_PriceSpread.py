import requests
import json
import Q2_USDT_QuoteAsset_Trade_24Hr

def getPriceSpread(USDTList):

  error = None
  priceSpreadDict = {}

  # Get data from Order Book Ticker API for each symbol
  for i in range(len(USDTList)):
    orderBookTicketerApiUrl = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={USDTList[i]['symbol']}"
    orderBookTicketerApiRequest = requests.get(orderBookTicketerApiUrl)
    if (orderBookTicketerApiRequest.status_code != 200):
      error = f"ERROR : Unable to get data from Order Book Ticker API - {orderBookTicketerApiUrl}\nERROR CODE : {orderBookTicketerApiRequest.status_code}\nDETAILS : {orderBookTicketerApiRequest.text}"
      return priceSpreadDict, error
    
    ## Convert the data to json
    orderBookTicketerApiData = json.loads(orderBookTicketerApiRequest.text)
    ## Calculate the price spread -> askPrice - bidPrice
    ## This data is stored as dict with key - symbol name and value and list of price spread(single element)
    priceSpread = float(orderBookTicketerApiData['askPrice']) - float(orderBookTicketerApiData['bidPrice'])
    priceSpreadDict[USDTList[i]['symbol']] = format(priceSpread, '.10f')
  
  return priceSpreadDict, error

if __name__ == "__main__":
  USDTHighTradeSymbolsList = []
  topUSDTHighTradeSymbolsLimit = 5
  priceSpreadDict = {}
  USDTHighTradeSymbolsList, error = Q2_USDT_QuoteAsset_Trade_24Hr.getUSDTHighTradeSymbols(topUSDTHighTradeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours\n")
  for i in range(len(USDTHighTradeSymbolsList)):
    print (f"{USDTHighTradeSymbolsList[i]['symbol']} - {USDTHighTradeSymbolsList[i]['count']}")

  priceSpreadDict, error = getPriceSpread(USDTHighTradeSymbolsList)
  if error is not None:
    print(error)
    exit(0)
  print ("\nThe price spread of the above symbols\n")
  for i in priceSpreadDict:
    print (f"{i} - {priceSpreadDict[i]}")
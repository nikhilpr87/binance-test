import Q2_USDT_QuoteAsset_Trade_24Hr
import Q4_USDT_PriceSpread
import time

def getPriceSpreadAbsoluteDelta(priceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread):

  error = None
  tempPreviousPriceSpreadDict = previousPriceSpreadDict.copy()
  
  try:

    if not bool(previousPriceSpreadDict):

      for i in priceSpreadDict:
        tempPreviousPriceSpreadDict[i] = "0.0000000000"
      absoluteDeltaPriceSpread = priceSpreadDict.copy()
      previousPriceSpreadDict = priceSpreadDict.copy()

      return tempPreviousPriceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread, error

    for i in priceSpreadDict:
      if i not in absoluteDeltaPriceSpread:
        absoluteDeltaPriceSpread[i] = priceSpreadDict[i].value()
        continue
      absoluteDeltaPriceSpread[i] = format(abs(float(priceSpreadDict[i]) - float(previousPriceSpreadDict[i])), '.10f')
  
    for i in priceSpreadDict:
      if i not in previousPriceSpreadDict:
        previousPriceSpreadDict[i] = "0.0000000000"
        continue
      previousPriceSpreadDict[i] = priceSpreadDict[i].value()
      
  
  except Exception as e:
    error = f"ERROR : Unable to get the absolute delta of price spread\nDETAILS : {str(e)}"

  return tempPreviousPriceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread, error

if __name__ == "__main__":
  USDTHighTradeSymbolsList = []
  topUSDTHighTradeSymbolsLimit = 5
  priceSpreadDict = {}
  USDTHighTradeSymbolsList, error = Q2_USDT_QuoteAsset_Trade_24Hr.getUSDTHighTradeSymbols(topUSDTHighTradeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print (f"\n\nThe top {topUSDTHighTradeSymbolsLimit} symbols with quote asset USDT and the highest number of trades over the last 24 hours\n")
  for i in range(len(USDTHighTradeSymbolsList)):
    print (f"{USDTHighTradeSymbolsList[i]['symbol']} - {USDTHighTradeSymbolsList[i]['count']}")

  previousPriceSpreadDict = {}
  absoluteDeltaPriceSpread = {}
  priceSpreadDict = {}
  print ("\nThe price spread and absolute delta of price spread for each of the above symbols for quote asset USDT on every 10 seconds\n")
  print ("Press Ctrl-C to terminate the execution\n")
  try:
    while True:
      priceSpreadDict, error = Q4_USDT_PriceSpread.getPriceSpread(USDTHighTradeSymbolsList)
      if error is not None:
        print(error)
        exit(0)
      tempPreviousPriceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread, error = getPriceSpreadAbsoluteDelta(priceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread)
      for i in priceSpreadDict:
        print (f"{i}\n - Price Spread : {priceSpreadDict[i]}\n - Previous Price Spread : {tempPreviousPriceSpreadDict[i]}\n - Absolute Delta Price Spread : {absoluteDeltaPriceSpread[i]}\n")
      print ("#####################################################################################################\n")
      time.sleep(10)
  except KeyboardInterrupt:
    print("Received Ctrl-C to terminate the code")
    pass
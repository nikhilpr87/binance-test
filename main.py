import Q1_BTC_QuoteAsset_Volume_24Hr
import Q2_USDT_QuoteAsset_Trade_24Hr
import Q3_BTC_QuoteAsset_NotionalValue
import Q4_USDT_PriceSpread
import Q5_USDT_PriceSpread_AbsoluteDelta
import Q6_USDT_PriceSpread_AbsoluteDelta_To_Prometheus
import time


if __name__ == "__main__":

  # 1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.

  print ("\n\n1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order")
  print ("-----------------------------------------------------------------------------------------------------------------")
  
  BTCHighVolumeSymbolsList = []
  topBTCHighVolumeSymbolsLimit = 5
  BTCHighVolumeSymbolsList, error = Q1_BTC_QuoteAsset_Volume_24Hr.getBTCHighVolumeSymbols(topBTCHighVolumeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order\n")
  for i in range(len(BTCHighVolumeSymbolsList)):
    print (f"{BTCHighVolumeSymbolsList[i]['symbol']} - {BTCHighVolumeSymbolsList[i]['volume']}")
  

  # 2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.

  print ("\n\n2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order")
  print ("----------------------------------------------------------------------------------------------------------------------------")

  USDTHighTradeSymbolsList = []
  topUSDTHighTradeSymbolsLimit = 5
  USDTHighTradeSymbolsList, error = Q2_USDT_QuoteAsset_Trade_24Hr.getUSDTHighTradeSymbols(topUSDTHighTradeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours\n")
  for i in range(len(USDTHighTradeSymbolsList)):
    print (f"{USDTHighTradeSymbolsList[i]['symbol']} - {USDTHighTradeSymbolsList[i]['count']}")


  # 3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?

  print ("\n\n3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?")
  print ("-------------------------------------------------------------------------------------------------------------------------")

  notionalValueList = []
  topOrderBookLimit = 200
  notionalValueList, error = Q3_BTC_QuoteAsset_NotionalValue.getBTCTotalNotionalValue(BTCHighVolumeSymbolsList, topOrderBookLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe total notional value of the above symbols for the top 200 bids and asks currently on each order book\n")
  for i in range(len(notionalValueList)):
    print(f"{notionalValueList[i]['symbol']}\n - Bids : {notionalValueList[i]['totalTopBidsNotionalValue']}\n - Asks : {notionalValueList[i]['totalTopAsksNotionalValue']}\n")


  # 4. What is the price spread for each of the symbols from Q2?

  print ("\n4. What is the price spread for each of the symbols from Q2?")
  print ("------------------------------------------------------------")

  priceSpreadDict = {}
  priceSpreadDict, error = Q4_USDT_PriceSpread.getPriceSpread(USDTHighTradeSymbolsList)
  if error is not None:
    print(error)
    exit(0)
  print ("\n\nThe price spread of the above symbols\n")
  for i in priceSpreadDict:
    print (f"{i} - {priceSpreadDict[i]}")


  # 5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.
  # 6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

  print ("\n\n5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol")
  print ("                                                    &                                                        ")
  print ("6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format")
  print ("-----------------------------------------------------------------------------------------------------------------")
  
  previousPriceSpreadDict = {}
  absoluteDeltaPriceSpread = {}
  priceSpreadDict = {}
  promethusPushGatewayURL = 'http://localhost:8080/metrics/job/pushgateway'
  print ("\n\nThe price spread and absolute delta of price spread for each of the above symbols for quote asset USDT on every 10 seconds\n")
  print ("Press Ctrl-C to terminate the loop\n")
  try:
    while True:
      priceSpreadDict, error = Q4_USDT_PriceSpread.getPriceSpread(USDTHighTradeSymbolsList)
      if error is not None:
        print(error)
        exit(0)
      tempPreviousPriceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread, error = Q5_USDT_PriceSpread_AbsoluteDelta.getPriceSpreadAbsoluteDelta(priceSpreadDict, previousPriceSpreadDict, absoluteDeltaPriceSpread)
      for i in priceSpreadDict:
        print (f"{i}\n - Price Spread : {priceSpreadDict[i]}\n - Previous Price Spread : {tempPreviousPriceSpreadDict[i]}\n - Absolute Delta Price Spread : {absoluteDeltaPriceSpread[i]}\n")
    
      error = Q6_USDT_PriceSpread_AbsoluteDelta_To_Prometheus.pushPriceSpreadDeltaToPrometheus(absoluteDeltaPriceSpread, promethusPushGatewayURL)
      if error is not None:
        print(error)
        exit(0)
      print ("Pushed absolute delta of price spread to Prometheus")
      print ("\n#####################################################################################################\n")
      time.sleep(10)
  except KeyboardInterrupt:
    print("Received Ctrl-C to terminate the execution")
    pass
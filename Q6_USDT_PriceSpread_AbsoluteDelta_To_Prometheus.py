import requests
import Q2_USDT_QuoteAsset_Trade_24Hr
import Q4_USDT_PriceSpread
import Q5_USDT_PriceSpread_AbsoluteDelta
import time

def pushPriceSpreadDeltaToPrometheus(absoluteDeltaPriceSpread, promethusPushGatewayURL):
  error = None

  prometheusMetricData = "# TYPE absolute_price_spread gauge\n# HELP absolute_price_spread Absolute Price Spread of Symbols\n"
  for i in absoluteDeltaPriceSpread:
    prometheusMetricData = f"{prometheusMetricData}absolute_price_spread{{symbol=\"{i}\"}} {absoluteDeltaPriceSpread[i]}\n"

  try:
    pushMetricsRequest = requests.post(promethusPushGatewayURL, prometheusMetricData.encode())
    if pushMetricsRequest.status_code != 200:
      error = f"Unable to push metrics to {promethusPushGatewayURL}\n  >> Error Code : {pushMetricsRequest.status_code}\n  >> Details : {pushMetricsRequest.text}"
  except Exception as e:
    error = f"Unable to push metrics to {promethusPushGatewayURL}\n >> Details : {str(e)}"
  
  return error

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
  promethusPushGatewayURL = 'http://localhost:8080/metrics/job/pushgateway'
  print ("\nThe price spread and absolute delta of price spread for each of the above symbols for quote asset USDT on every 10 seconds\n")
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
    
      error = pushPriceSpreadDeltaToPrometheus(absoluteDeltaPriceSpread, promethusPushGatewayURL)
      if error is not None:
        print(error)
        exit(0)
      print ("Pushed absolute delta of price spread to Prometheus")
      print ("\n#####################################################################################################\n")
      time.sleep(10)
  except KeyboardInterrupt:
    print("Received Ctrl-C to terminate the execution")
    pass
import requests
import json

def getUSDTHighTradeSymbols(topUSDTHighTradeSymbolsLimit):
  error = None
  USDTHighTradeSymbolsList = []
  tickerApiUrl = "https://api.binance.com/api/v3/ticker/24hr"
  
  # Get data from Ticker API
  try:
    tickerApiRequest = requests.get(tickerApiUrl)
    if (tickerApiRequest.status_code != 200):
      error = f"ERROR : Unable to get data from Ticker API - {tickerApiUrl}\nERROR CODE : {tickerApiRequest.status_code}DETAILS : {tickerApiRequest.text}"
      return USDTHighTradeSymbolsList, error
    # Convert the data to JSON
    tickerApiDataJson = json.loads(tickerApiRequest.text)
  except Exception as e:
    error = error = f"ERROR : Unable to get data from Ticker API - {tickerApiUrl}\nDETAILS : {str(e)}"
    return USDTHighTradeSymbolsList, error

  # Create list of quote asset USDT from Filter Ticker API data
  USDTSymbolsTradeList = []
  for i in range(len(tickerApiDataJson)):
    if (tickerApiDataJson[i]['symbol'].endswith("USDT")):
      USDTSymbolsTradeList.append({"symbol": tickerApiDataJson[i]['symbol'], "count": float(tickerApiDataJson[i]['count'])})

  # Reverse sort the list
  USDTSymbolsTradeList.sort(key=lambda item: item.get('count'), reverse=True)

  # Get the top list of symbols with high trade count
  for i in range(topUSDTHighTradeSymbolsLimit):
    USDTHighTradeSymbolsList.append({'symbol': USDTSymbolsTradeList[i]['symbol'], 'count': float(USDTSymbolsTradeList[i]['count'])})
  
  return USDTHighTradeSymbolsList, error

if __name__ == "__main__":
  USDTHighTradeSymbolsList = []
  topUSDTHighTradeSymbolsLimit = 5
  USDTHighTradeSymbolsList, error = getUSDTHighTradeSymbols(topUSDTHighTradeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours\n")
  for i in range(len(USDTHighTradeSymbolsList)):
    print (f"{USDTHighTradeSymbolsList[i]['symbol']} - {USDTHighTradeSymbolsList[i]['count']}")
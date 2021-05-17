import requests
import json

def getBTCHighVolumeSymbols(topBTCHighVolumeSymbolsLimit):
  error = None
  BTCHighVolumeSymbolsList = []
  tickerApiUrl = "https://api.binance.com/api/v3/ticker/24hr"
  
  # Get data from Ticker API
  try:
    tickerApiRequest = requests.get(tickerApiUrl)
    if (tickerApiRequest.status_code != 200):
      error = tickerApiRequest.text
      error = f"ERROR : Unable to get data from Ticker API - {tickerApiUrl}\nERROR CODE : {tickerApiRequest.status_code}\nDETAILS : {tickerApiRequest.text}"
      return BTCHighVolumeSymbolsList, error
    # Convert the data to JSON
    tickerApiDataJson = json.loads(tickerApiRequest.text)
  except Exception as e:
    error = error = f"ERROR : Unable to get data from Ticker API - {tickerApiUrl}\nDETAILS : {str(e)}"
    return BTCHighVolumeSymbolsList, error

  # Create list of quote asset BTC from Filter Ticker API data
  BTCSymbolsVolumeList = []
  for i in range(len(tickerApiDataJson)):
    if (tickerApiDataJson[i]['symbol'].endswith("BTC")):
      BTCSymbolsVolumeList.append({"symbol": tickerApiDataJson[i]['symbol'], "volume": float(tickerApiDataJson[i]['volume'])})

  # Reverse sort the list
  BTCSymbolsVolumeList.sort(key=lambda item: item.get('volume'), reverse=True)

  # Get the top list of symbols with high Volume
  for i in range(topBTCHighVolumeSymbolsLimit):
    BTCHighVolumeSymbolsList.append({'symbol': BTCSymbolsVolumeList[i]['symbol'], 'volume': BTCSymbolsVolumeList[i]['volume']})
  
  return BTCHighVolumeSymbolsList, error

if __name__ == "__main__":
  BTCHighVolumeSymbolsList = []
  topBTCHighVolumeSymbolsLimit = 5
  BTCHighVolumeSymbolsList, error = getBTCHighVolumeSymbols(topBTCHighVolumeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order\n")
  for i in range(len(BTCHighVolumeSymbolsList)):
    print (f"{BTCHighVolumeSymbolsList[i]['symbol']} - {BTCHighVolumeSymbolsList[i]['volume']}")
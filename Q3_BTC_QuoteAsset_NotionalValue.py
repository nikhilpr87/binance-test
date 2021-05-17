import requests
import json
import Q1_BTC_QuoteAsset_Volume_24Hr

def getBTCTotalNotionalValue(BTCList, topOrderBookLimit):
  error = None
  notionalValueList = []
  for i in range(len(BTCList)):
    # Get the data from Order Book Api for each symbol
    try:
      orderBookApiURL = f"https://api.binance.com/api/v3/depth?symbol={BTCList[i]['symbol']}"
      orderBookApiRequest = requests.get(orderBookApiURL)
      if orderBookApiRequest.status_code != 200:
        error = f"ERROR : Unable to get data from Order Book API - {orderBookApiURL}\nERROR CODE : {orderBookApiRequest.status_code}\nDETAILS : {orderBookApiRequest.text}"
        return notionalValueList, error
      orderBookApiData = json.loads(orderBookApiRequest.text)
    except Exception as e:
      error = f"ERROR : Unable to get data from Order Book API - {orderBookApiURL}\nDETAILS : {str(e)}"
      return notionalValueList, error
    
    if len(orderBookApiData['bids']) == 0 and len(orderBookApiData['asks']) == 0:
      notionalValueList.append({'symbol': BTCList[i]['symbol'], 'bids': [], 'asks': [], 'topBidsNotionalValueList': [], 'totalTopBidsNotionalValue': 0, 'topAsksNotionalValueList': [], 'totalTopAsksNotionalValue': 0})
      continue

    ## bidsNotionalValueList - Create list of notional value -> price * quatity for bids
    bidsNotionalValueList = []
    for j in range(len(orderBookApiData['bids'])):
      #print (orderBookApiData['bids'][j])
      bidsNotionalValue = float(orderBookApiData['bids'][j][0]) * float(orderBookApiData['bids'][j][1])
      #print (f"notionalValue : {bidsNotionalValue}")
      bidsNotionalValueList.append(round(bidsNotionalValue, 10))
  
    ### Reverse sort the list
    bidsNotionalValueList.sort(reverse = True)

    ### topBidsNotionalValueList - List of Notional value of bids for the topOrderBookLimit(200)
    ### totalTopBidsNotionalValue - Sum of of Notional value of bids for the topOrderBookLimit(200)
    topBidsNotionalValueList = []
    totalTopBidsNotionalValue = 0
    for k in range(len(bidsNotionalValueList)):
      if (topOrderBookLimit > k):
        topBidsNotionalValueList.append(bidsNotionalValueList[k])
        totalTopBidsNotionalValue = totalTopBidsNotionalValue + bidsNotionalValueList[k]

    ## asksNotionalValueList - Create list of notional value -> price * quatity for asks
    asksNotionalValueList = []
    #print (orderBookApiData['asks'])
    for l in range(len(orderBookApiData['asks'])):
      asksNotionalValue = float(orderBookApiData['asks'][l][0]) * float(orderBookApiData['asks'][l][1])
      asksNotionalValueList.append(round(asksNotionalValue, 10))
  
    ### Reverse sort the list
    asksNotionalValueList.sort(reverse = True)

    ### topAsksNotionalValueList - List of Notional value of asks for the topOrderBookLimit(200)
    ### totalTopAsksNotionalValue - Sum of of Notional value of bids for the topOrderBookLimit(200)
    topAsksNotionalValueList = []
    totalTopAsksNotionalValue = 0
    for m in range(len(asksNotionalValueList)):
      if (topOrderBookLimit > m):
        topAsksNotionalValueList.append(asksNotionalValueList[m])
        totalTopAsksNotionalValue = totalTopAsksNotionalValue + asksNotionalValueList[i]
  
    notionalValueList.append({'symbol': BTCList[i]['symbol'], 'bids': bidsNotionalValueList, 'asks': asksNotionalValueList, 'topBidsNotionalValueList': topBidsNotionalValueList, 'totalTopBidsNotionalValue': totalTopBidsNotionalValue, 'topAsksNotionalValueList': topAsksNotionalValueList, 'totalTopAsksNotionalValue': totalTopAsksNotionalValue})
    #print (orderBookApiData)

  return notionalValueList, error

if __name__ == "__main__":
  BTCHighVolumeSymbolsList = []
  topBTCHighVolumeSymbolsLimit = 5
  notionalValueList = []
  topOrderBookLimit = 200
  BTCHighVolumeSymbolsList, error = Q1_BTC_QuoteAsset_Volume_24Hr.getBTCHighVolumeSymbols(topBTCHighVolumeSymbolsLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order\n")
  for i in range(len(BTCHighVolumeSymbolsList)):
    print (f"{BTCHighVolumeSymbolsList[i]['symbol']} - {BTCHighVolumeSymbolsList[i]['volume']}")

  notionalValueList, error = getBTCTotalNotionalValue(BTCHighVolumeSymbolsList, topOrderBookLimit)
  if error is not None:
    print (error)
    exit(0)
  print ("\n\nThe total notional value of the above symbols for the top 200 bids and asks currently on each order book\n")
  for i in range(len(notionalValueList)):
    print(f"{notionalValueList[i]['symbol']}\n - Bids : {notionalValueList[i]['totalTopBidsNotionalValue']}\n - Asks : {notionalValueList[i]['totalTopAsksNotionalValue']}\n")

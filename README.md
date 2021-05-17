# Pre-requisites
Below packages are required
- docker
- docker-compose
- python3

I used prometheus pushgateway to push the metrics to promethus

# How to run

### Start the prometheus and pushgateway containers
```
docker-compose -f docker-compose.yaml up -d
```
Once the containers are up, you can access them from below urls
* Prometheus - http://localhost:9090
* Prometheus Pushgateway - http://localhost:8080

### Run the below to execute the code

1. Print the top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order.
  
    ```
    python3 Q1_BTC_QuoteAsset_Volume_24Hr.py
    ```

    Sample Output
    ```

    The top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order

    WINBTC - 2093993989.0
    DENTBTC - 2008376255.0
    DOGEBTC - 1979098233.0
    NPXSBTC - 1963359809.0
    BTTBTC - 1899964312.0

    ```

2. Print the top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours in descending order.

    ```
    python3 Q2_USDT_QuoteAsset_Trade_24Hr.py
    ```

    Sample Output
    ```

    The top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours

    DOGEUSDT - 5585361.0
    ETHUSDT - 2701036.0
    BTCUSDT - 2578044.0
    ADAUSDT - 2464358.0
    SHIBUSDT - 2427462.0

    ```

3. Using the symbols from Q1, what is the total notional value of the top 200 bids and asks currently on each order book?

    ```
    python3 Q3_BTC_QuoteAsset_NotionalValue.py
    ```

    Sample Output
    ```


    The top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order

    WINBTC - 2093993989.0
    DENTBTC - 2008376255.0
    DOGEBTC - 1979227929.0
    NPXSBTC - 1963359809.0
    BTTBTC - 1899964312.0


    The total notional value of the above symbols for the top 200 bids and asks currently on each order book

    WINBTC
    - Bids : 0
    - Asks : 0

    DENTBTC
    - Bids : 0
    - Asks : 0

    DOGEBTC
    - Bids : 202.4458701
    - Asks : 815.0212440000012

    NPXSBTC
    - Bids : 0
    - Asks : 0

    BTTBTC
    - Bids : 0
    - Asks : 0

    ```

4. What is the price spread for each of the symbols from Q2?

    ```
    python3 Q4_USDT_PriceSpread.py
    ```

    Sample Output
    ```

    The top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours

    DOGEUSDT - 5586468.0
    ETHUSDT - 2697996.0
    BTCUSDT - 2576247.0
    ADAUSDT - 2461037.0
    SHIBUSDT - 2424255.0

    The price spread of the above symbols

    DOGEUSDT - 0.0000200000
    ETHUSDT - 0.2800000000
    BTCUSDT - 0.0100000000
    ADAUSDT - 0.0001000000
    SHIBUSDT - 0.0000000100

    ```
5. Every 10 seconds print the result of Q4 and the absolute delta from the previous value for each symbol.

    ```
    python3 Q5_USDT_PriceSpread_AbsoluteDelta.py
    ```

    Sample Output
    ```

    The top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours

    DOGEUSDT - 5587868.0
    ETHUSDT - 2695968.0
    BTCUSDT - 2574669.0
    ADAUSDT - 2459939.0
    SHIBUSDT - 2422761.0

    The price spread and absolute delta of price spread for each of the above symbols for quote asset USDT on every 10 seconds

    Press Ctrl-C to terminate the execution

    DOGEUSDT
    - Price Spread : 0.0000100000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0000100000

    ETHUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0100000000

    BTCUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0100000000

    ADAUSDT
    - Price Spread : 0.0001000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0001000000

    SHIBUSDT
    - Price Spread : 0.0000000100
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0000000100

    #####################################################################################################
    DOGEUSDT
    - Price Spread : 0.0000100000
    - Previous Price Spread : 0.0000100000
    - Absolute Delta Price Spread : 0.0000000000

    ETHUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.0100000000
    - Absolute Delta Price Spread : 0.0000000000

    BTCUSDT
    - Price Spread : 4.3800000000
    - Previous Price Spread : 0.0100000000
    - Absolute Delta Price Spread : 4.3700000000

    ADAUSDT
    - Price Spread : 0.0002000000
    - Previous Price Spread : 0.0001000000
    - Absolute Delta Price Spread : 0.0001000000

    SHIBUSDT
    - Price Spread : 0.0000000100
    - Previous Price Spread : 0.0000000100
    - Absolute Delta Price Spread : 0.0000000000

    #####################################################################################################

    ```

6. Make the output of Q5 accessible by querying http://localhost:8080/metrics using the Prometheus Metrics format.

    ```
    python3 Q6_USDT_PriceSpread_AbsoluteDelta_To_Prometheus.py
    ```

    Sample Output
    ```

    The top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours

    DOGEUSDT - 5589752.0
    ETHUSDT - 2695015.0
    BTCUSDT - 2573423.0
    ADAUSDT - 2457099.0
    SHIBUSDT - 2420788.0

    The price spread and absolute delta of price spread for each of the above symbols for quote asset USDT on every 10 seconds

    Press Ctrl-C to terminate the loop

    DOGEUSDT
    - Price Spread : 0.0000100000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0000100000

    ETHUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0100000000

    BTCUSDT
    - Price Spread : 0.9100000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.9100000000

    ADAUSDT
    - Price Spread : 0.0002000000
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0002000000

    SHIBUSDT
    - Price Spread : 0.0000000100
    - Previous Price Spread : 0.0000000000
    - Absolute Delta Price Spread : 0.0000000100

    Pushed absolute delta of price spread to Prometheus

    #####################################################################################################

    DOGEUSDT
    - Price Spread : 0.0000100000
    - Previous Price Spread : 0.0000100000
    - Absolute Delta Price Spread : 0.0000000000

    ETHUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.0100000000
    - Absolute Delta Price Spread : 0.0000000000

    BTCUSDT
    - Price Spread : 0.0100000000
    - Previous Price Spread : 0.9100000000
    - Absolute Delta Price Spread : 0.9000000000

    ADAUSDT
    - Price Spread : 0.0001000000
    - Previous Price Spread : 0.0002000000
    - Absolute Delta Price Spread : 0.0001000000

    SHIBUSDT
    - Price Spread : 0.0000000100
    - Previous Price Spread : 0.0000000100
    - Absolute Delta Price Spread : 0.0000000000

    Pushed absolute delta of price spread to Prometheus

    #####################################################################################################

    ```

    Sample Output from metric url - http://localhost:8080/api/v1/query?query=absolute_price_spread
    ```
    curl 'http://localhost:8080/api/v1/query?query=absolute_price_spread'
    {"status":"success","data":{"resultType":"vector","result":[{"metric":{"__name__":"absolute_price_spread","category":"pushgateway","environment":"hoge","exported_job":"pushgateway","instance":"pushgateway:9091","job":"pushgateway","symbol":"ADAUSDT"},"value":[1620997031.235,"0.0001"]},{"metric":{"__name__":"absolute_price_spread","category":"pushgateway","environment":"hoge","exported_job":"pushgateway","instance":"pushgateway:9091","job":"pushgateway","symbol":"BTCUSDT"},"value":[1620997031.235,"0.9"]},{"metric":{"__name__":"absolute_price_spread","category":"pushgateway","environment":"hoge","exported_job":"pushgateway","instance":"pushgateway:9091","job":"pushgateway","symbol":"ETHUSDT"},"value":[1620997031.235,"0"]},{"metric":{"__name__":"absolute_price_spread","category":"pushgateway","environment":"hoge","exported_job":"pushgateway","instance":"pushgateway:9091","job":"pushgateway","symbol":"SHIBUSDT"},"value":[1620997031.235,"0"]}]}}
    ```

#### Note
All the above scripts can be run using a single script as well
This will provide the output of all the questions
```
python main.py
```

## Post Execution
Once the execution is completed
Run the below to stop the container
```
docker-compose -f docker-compose.yaml down
```

# customer-api-data-request


Directions on using Python script

##  Through Coin Metrics API you can make a requests to the api using the python Module "requests". Customize your search by using Coin Metrics's Parameters


```url = "https://community-api.coinmetrics.io/v4/timeseries/market-trades?markets=coinbase-btc-usd-spot&start_time=2022-03-07&end_time=2022-03-07&page_size=10000&paging_from=start"```


 Check Coin Metrics Documentation for more information on Coin Metrics's search parameters on Market Trade data - 
https://docs.coinmetrics.io/api/v4#operation/getTimeseriesMarketTrades


## Data is parsed for readability
``` python
response = requests.get(url)
data = response.text
parse_data = json.loads(data)
```

## Make sure you are grabbing the list name so the function can get the dictionaries within the list and save them to the csv file
 ```python
 requested_trades = parse_data.get("data")
 ```


## The function is already built out for you. You only need to pass the parsed data requested from Coin Metrics API as the function's parameter.

``` python 

def collect_trades(trades):
    for trade in trades:
        # looping through list of dictionaries
        # for each next page url get data list

        convert_datetime = parser.isoparse(trade["database_time"])
        # parsing iso816 time so python can read it

        if convert_datetime.hour in trades_by_timeslot:
            # checking if the hour is equal to one of the timeslots in list

            date = convert_datetime.strftime("%Y-%m-%d")
            # changing the timezone format to just the date without time
            # I am doing this so I can name the file after the hour for readability

            if trade not in trades_by_timeslot[convert_datetime.hour]:
                # if item is not in key's list
                # above we are preventing duplicates

                found_home = trades_by_timeslot[convert_datetime.hour].append(
                    trade)
                # above we are appending new trades to one of the specified lists in trades_by_timeslot dictionary

            with open(str(date) + ":" + str(convert_datetime.hour) + ".csv", "w", newline="") as create_file:
                # writes csv file
                field_headers = ["market", "time", "coin_metrics_id","amount", "price", "database_time", "side"]
                
                writer = csv.DictWriter(create_file,
                                        fieldnames=field_headers,
                                        )
                writer.writeheader()
                create_file.close()

                for key in trades_by_timeslot[convert_datetime.hour]:
                    key = [key["market"], key["time"], key["coin_metrics_id"],key["amount"], key["price"], key["database_time"], key["side"]]

                    def append_to_file(file_name, list_of_trades):
                        # appends to csv file
                        with open(str(file_name), "a", newline="") as trade_file:
                            append_trades = csv.writer(trade_file)
                            append_trades.writerow(list_of_trades)

                    append_to_file(str(date) + ":" +
                                   str(convert_datetime.hour) + ".csv", key)

        else:
            error("Error please check line 53 and below"
 ```


## Call Function and enter the parameter in our case its
``` python 
requested_trades 
```

```python
collect_trades = collect_trades(requested_trades) 
```



## now that thats over, the function generates a file. The file is created based of the current or passed hour the trades are under and you can see the file in under each hour in UTC Time like so

<img width="141" alt="Screen Shot 2022-03-08 at 12 10 48 PM" src="https://user-images.githubusercontent.com/79281530/157316968-c7e7855b-d030-4c21-93e7-77e6da193e3e.png">


<img width="1065" alt="Screen Shot 2022-03-08 at 12 11 56 PM" src="https://user-images.githubusercontent.com/79281530/157317152-fc0f3c64-80f5-42ad-a4c8-f58589a1a40a.png">


# You can use these csv files to store the trades to a database or spreadsheet. Happy Usage!


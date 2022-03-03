import csv
from hmac import new
from operator import contains
from os import times
from numpy import append
from parso import parse
from pkg_resources import FileMetadata
import requests
import json
import pandas as pd
import datetime 




# market_trades = [
#     {
#         "market": "coinbase-btc-usd-spot",
#         "time": "2022-02-26T18:46:49.577735000Z",
#         "coin_metrics_id": "287721200",
#         "amount": "0.00060058",
#         "price": "38959.58",
#         "database_time": "2022-02-26T18:46:49.760007000Z",
#         "side": "buy"
#     },
#     {
#         "market": "coinbase-btc-usd-spot",
#         "time": "2022-02-26T18:46:51.992040000Z",
#         "coin_metrics_id": "287721207",
#         "amount": "0.00080013",
#         "price": "38963.41",
#         "database_time": "2022-02-26T18:46:52.261496000Z",
#         "side": "sell"
#     },
#     {
#         "market": "coinbase-btc-usd-spot",
#         "time": "2022-02-27T18:46:51.992040000Z",
#         "coin_metrics_id": "287721207",
#         "amount": "0.00080013",
#         "price": "38963.41",
#         "database_time": "2022-02-27T18:46:52.261496000Z",
#         "side": "sell"
#     },
#     {
#         "market": "coinbase-btc-usd-spot",
#         "time": "2022-02-28T18:46:51.992040000Z",
#         "coin_metrics_id": "287721207",
#         "amount": "0.00080013",
#         "price": "38963.41",
#         "database_time": "2022-02-27T18:46:52.261496000Z",
#         "side": "sell"
#     },
#     {
#         "market": "coinbase-btc-usd-spot",
#         "time": "2022-02-29T23:58:51.992040000Z",
#         "coin_metrics_id": "287721207",
#         "amount": "0.00080013",
#         "price": "38963.41",
#         "database_time": "2022-02-28T18:46:52.261496000Z",
#         "side": "sell"
#     }
# ]


url = 'https://community-api.coinmetrics.io/v4/timeseries/market-trades?markets=coinbase-btc-usd-spot'
response = requests.get(url)

data = response.text
parse_data = json.loads(data)

# trades_in_range = []
object_key = parse_data.get('data')
# print(object_key)

next_page = parse_data.get('next_page_url')

fetch_next_page = requests.get(next_page)
data_from_next_page = fetch_next_page.text 
data_from_next_page = json.loads(data_from_next_page)

# print(data_from_next_page)



data_frame = pd.DataFrame.from_dict(object_key) # all of the results
start = "2022-03-02T18:00:02.319957000Z"
end = "2022-03-03T01:09:52.567835000Z"

#take object key iterate over and extract each
from dateutil import parser
# parser.isoparse('2019-08-28T14:34:25.518993Z')
# datetime.datetime(2019, 8, 28, 14, 34, 25, 518993, tzinfo=tzutc()) 

# setup trades_by_timeslot

trades_by_timeslot = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    11: [],
    12: [],
    13: [],
    14: [],
    15: [],
    16: [],
    17: [],
    18: [],
    19: [],
    20: [],
    21: [],
    22: [],
    23: []
}

for trade in object_key:
    # print(trade["database_time"])
    convert_datetime = parser.isoparse(trade["database_time"])
    # print(convert_datetime)
    # print(trade)
    if convert_datetime.hour in trades_by_timeslot: #checking if the hour is equal to one of the timeslots in list
        # print('true')
        date = convert_datetime.strftime('%Y-%m-%d')
        
        field_names = [trade["market"], trade["time"], trade["coin_metrics_id"], trade["amount"], trade["price"], trade["database_time"], trade["side"]]
        field_headers = ["market", "time", "coin_metrics_id", "amount", "price", "database_time", "side"]
        

        f = open(str(date) + ':' + str(convert_datetime.hour) + '.csv', 'w', newline='')
        writer = csv.DictWriter(f,
                        fieldnames = field_headers,
                    )
        writer.writeheader()
        f.close()
            
        # if item is not in key's list
        if trade not in trades_by_timeslot[convert_datetime.hour]: #linear time complexity nest if statement O(m+n)
            # above we a preventing duplicates
            found_home = trades_by_timeslot[convert_datetime.hour].append(trade)
            def append_to_file(file_name, list_of_trades):

                with open(str(file_name), 'a+') as trade_file:
                    # add_trades = csv.writer(trade_file)
                    trade_file.write([list_of_trades])
                    trade_file.close()
            append_to_file(str(date) + ':' + str(convert_datetime.hour) + '.csv', trades_by_timeslot[convert_datetime.hour])

        # looping through n times
        else:
            print('not in time loop')

print(trades_by_timeslot)

keys = trades_by_timeslot[convert_datetime.hour]

# print(date)

# for keys in trades_by_timeslot:
    # print(str(date) + ':' + str(keys) + '.csv')
    


        
# print(value)
    





# is_true = start in data_frame["database_time"]
# print(is_true)

# mask = (data_frame["database_time"] >= start) & (data_frame["database_time"] <= end)
# print(data_frame["database_time"])
# # print(data_frame["database_time"] > start)
# # print(data_frame["database_time"] <= end)

# # print(mask)
# df = data_frame.loc[mask]


# while data_from_next_page:
#     next_page = data_from_next_page
#     df

# for label, content in enumerate(df):
#     print(label, content)





# for each time slot make a list

#make a list of lists when each list within the parent list will be a time 





# trades_in_range.append(df)
# trades_in_range = next_page_url(next_page, trades_in_range)


# def next_page_url(url, trades_in_range):
#     if url != '':
#         response = requests.get(url)
#         resp_json = response.json()
#         trades_in_range.append(resp_json)
#         if resp_json.get("next_page_url") != '':
#             return next_page_url(resp_json.get("next_page_url"), trades_in_range)
#         return trades_in_range

# back_to_dictionary = df.to_json()
# print(back_to_dictionary)
# push = trades_in_range.append(back_to_dictionary) 
# print(push)


# #Discover API url filtered to movies >= 2004 and containing Drama genre_ID: 18
# discover_api = 'https://api.themoviedb.org/3/discover/movie? 
# api_key=['my api key']&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=>%3D2004&with_genres=18'

# discover_api = requests.get(discover_api).json()
# most_popular_films = discover_api["results"]
# while discover_api["next_url"]:
#     discover_api = requests.get(discover_api["next_url"]).json()
#     most_popular_films.extend(discover_api["results"])

# #printing movie_id and movie_title by popularity desc
# for i, film in enumerate(most_popular_films):
#     print(i, film['id'], film['title'])




    # print(start_date in trade["database_time"])

    # start = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f%z")
    # end = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f%z")



    # if trade["database_time"] in pd.date_range(start, end):
    #     trades_in_range.append(datetime.date.fromisoformat(trade["database_time"]) > datetime.date.isoformat(start) & datetime.isoformat(end))
        
    # above this is returning a boolean but I want it to return data
    # if trade["database_time"] in pd.date_range(start_date, end_date):
    #     list_of_trades = trade["databse_time"] > start_date & trade["database_time"] <= end_date
# print(trades_in_range)



# print(list_of_trades)

# print(df)

# making a get request to the url to retreive market trade data
# response = requests.get(url)
# x = response.json()
# parsed_data = x.get("data")

# df = pd.DataFrame(parsed_data["database_time"])

# print(df)


















# first way of doing it without pandas *************


# stringify_data = response.text

# parse_data = json.loads(stringify_data)

# market_trade_dictionary = parse_data.get("data")


# def search(database_time, dictionary):
#     # below we want to return element for each element in dictionary if the database time is our specified time return the object with that matching time 
#     times = [time for time in dictionary if time["database_time"] == database_time]
#     return times

# # we want to return all matching objects with the same characters in database time

    
# search = search("2022-02-27T02:32:56.493772000Z", market_trade_dictionary)


# new_json = json.dumps(search, indent=4, sort_keys=True)

# print(new_json)

# ************************

# 1. extract data ranging from beginning of trading hours to end of trading hours(24 hrs)
# A. only data that we want cant really get data from past 4 days but can get data from 24hrs so will use that
# B. iterate through and only get specified data

# 2. save json data to json file

# 3. convert it to a csv file(for each trading hour it must be in a separate file)

# 4. write clean easy to read instructions for the client on how to use the python script and files

# 5. clean up my code by making sure Im using proper conventions and remove any unused modules
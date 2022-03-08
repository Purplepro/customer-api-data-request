import csv
import requests
import json
from dateutil import parser




url = "https://community-api.coinmetrics.io/v4/timeseries/market-trades?markets=coinbase-btc-usd-spot&start_time=2022-03-07&end_time=2022-03-07&page_size=10000&paging_from=start" 

response = requests.get(url)
data = response.text
parse_data = json.loads(data)
object_key = parse_data.get("data")

#take object key iterate over and extract each

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



def collect_trades(trades):

    # print(request_data)
    # next_page = trades.get("next_page_url")
    # print(next_page)
    
        
            
    for trade in trades: #looping through list of dictionaries
        #for each next page url get data list
        # print(trade["database_time"])

        convert_datetime = parser.isoparse(trade["time"]) #parsing iso816 time so python can read it
        # print(convert_datetime)
        # print(trade)





        if convert_datetime.hour in trades_by_timeslot: #checking if the hour is equal to one of the timeslots in list
            # print('true') 
            date = convert_datetime.strftime("%Y-%m-%d") #changing the timezone format to just the date without time
            # I am doing this so I can name the file after the hour for readability 
            
                
            # if item is not in key's list
            if trade not in trades_by_timeslot[convert_datetime.hour]: #linear time complexity nested if statement O(m+n) = O(n)
                # above we are preventing duplicates              
                found_home = trades_by_timeslot[convert_datetime.hour].append(trade)
                # next_page_trades = trades_by_timeslot[convert_datetime.hour].extend(next_pages["data"])

                #above we are appending new trades to one of the specified lists in trades_by_timeslot dictionary


            with open(str(date) + ":" + str(convert_datetime.hour) + ".csv", "w", newline="") as create_file:
                field_headers = ["market", "time", "coin_metrics_id", "amount", "price", "database_time", "side"]
                writer = csv.DictWriter(create_file,
                                fieldnames = field_headers,
                            )
                writer.writeheader()
                create_file.close()





                for key in trades_by_timeslot[convert_datetime.hour]:
                    key = [key["market"], key["time"], key["coin_metrics_id"], key["amount"], key["price"], key["database_time"], key["side"]]
                    



                    def append_to_file(file_name, list_of_trades):
                        with open(str(file_name), "a", newline="") as trade_file:
                            append_trades = csv.writer(trade_file)
                            append_trades.writerow(list_of_trades)
                            
                        

                    append_to_file(str(date) + ":" + str(convert_datetime.hour) + ".csv", key)


                        


        else:
            print("can't generate file because this list's time stamp is not in time loop")

collect_trades = collect_trades(object_key)
print(collect_trades)
        

print(trades_by_timeslot)


# ************************

# 1. extract data ranging from beginning of trading hours to end of trading hours(24 hrs)
# A. only data that we want cant really get data from past 4 days but can get data from 24hrs so will use that
# B. iterate through and only get specified data(computer can't take all data because its so much data)

# 2. save json data to json file

# 3. convert it to a csv file(for each trading hour it must be in a separate file)

# 4. write clean easy to read instructions for the client on how to use the python script and files

# 5. clean up my code by making sure Im using proper conventions and remove any unused modules
from urllib.request import urlopen
import datetime
import json


def top_marketcap():
    """
    Retrieves json formatted data from open source.
    Prints values with keyword 'name' based on their
    market cap rank at the moment.

    return: json formatted data of currencies
    """

    print("\nHere are top 10 currencies by market cap at the time:")

    url = ("https://api.coingecko.com/api/v3/coins/"+
            "markets?vs_currency=eur&order=market_cap_desc"+
            "&per_page=10&page=1&sparkline=false")
            
    response = urlopen(url)

    json_data = json.loads(response.read())

    for item in json_data:
        print(f"{item['market_cap_rank']}. {item['name']}" )

    return json_data




def current_data_id(id):
    """
    Takes id as parameter which is used for url. Reads data
    and turns it into json format.

    @param id: Id of a currency based on goingecko's database.
    return: json formatted data of currency
    """
    url = ("https://api.coingecko.com/api/v3/coins/" + id)
            
    response = urlopen(url)

    json_data = json.loads(response.read())

    return json_data

    
def data_by_range(dates, key_word, currency):
    """
    Retrieves and returns data from open source
    based on currency and chosen dates.

    @param dates: Pair of dates
    @param key_word: Filter to search wanted info
    @param currency: Id of a currency based on goingecko's database.
    return: list of pairs (dates, values). 
    """


    url = ("https://api.coingecko.com/api/v3/coins/" + currency +
            "/market_chart/range?vs_currency=eur&from=" +
            str(dates[0]) + "&to=" + str(dates[1]))

    response = urlopen(url)

    json_data = json.loads(response.read())

    list = json_data[key_word]

    return data_per_day(list)
    

def data_per_day(json_data):
    """
    Parameter json_data includes data from every hour and function
    limits that to only to last value of a date.

    @param json_data: json formatted list
    returns: Filtered list with only 1 value per day. 
    """

    data_of_day = []

    for pair in json_data:


        dt = datetime.datetime.utcfromtimestamp(pair[0]/1000)

        hour = int(dt.strftime("%H"))
        min = int(dt.strftime("%M"))

        #Find the data closest to midnight/Last result of the day 
        if (hour == 0 and min < 29) or (hour == 23 and min > 31):
            data_of_day.append(pair)

    return data_of_day
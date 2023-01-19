import json_read
import dates
from operator import itemgetter


def current_data():
    """
    Prints out most popular currencies at the time and user picks one. 
    Statistics of chosen currency is shown

    """
    while True:

        list = json_read.top_marketcap()

        user_input = input(f"\nChoose currency or 'g' to go back: ")

        if (user_input == 'g'):
            break

        for item in list:
            if (user_input == str(item['market_cap_rank'])):
                
                data = json_read.current_data_id(item['id'])

                print("\n"+10*"*")
                print(f"Here is current data of {data['name']}:\n")
                print(f"Price (€): {data['market_data']['current_price']['eur']}")
                print(f"Market cap (€): {data['market_data']['market_cap']['eur']}")
                print(f"Total volume (€): {data['market_data']['total_volume']['eur']}")
                print(f"Highest last 24h (€): {data['market_data']['high_24h']['eur']}")
                print(f"Lowest last 24h (€): {data['market_data']['low_24h']['eur']}")
                print(10*"*"+"\n")
                return
                
        else:
            print("Something went wrong, try again\n")
    return



def find_minmax(list):
    """
    Uses itemgetter to find out highest and lowest value of list of pairs'
    second value. Turns unix formatted date into dd.mm.yyyy form and prints
    results

    @param list: List of pairs [(date, price)] 
    """

    #[date 'dd.mm.yyyy', highest/lowest value]
    date_max = [dates.unix_to_date(max(list, key=itemgetter(1))[0]),
                max(list, key=itemgetter(1))[1]]
    date_min = [dates.unix_to_date(min(list, key=itemgetter(1))[0]),
                min(list, key=itemgetter(1))[1]]

    print(f"\nHighest price (€): {round(date_max[1],2)} ({date_max[0]})")
    print(f"Lowest price (€): {round(date_min[1],2)} ({date_min[0]})")
    return



def highest_growth(list):
    """
    Function goes through list of pairs, which includes dates and prices.
    It runs 2 for loops to find out when a person should have bought and sold 
    a currency to have the best profit percentage.

    @param list: List of pairs [(date, price)] 
    """
    highest_percentage = 0
    result = []

    #Loops list starting from every day
    for i in range(0, len(list)):

        #Loops list starting from every day after previous loop
        for j in range(i, len(list)):

            #Calculates percentage
            current_percentage = list[j][1] / list[i][1]*100

            if (current_percentage > highest_percentage):

                highest_percentage = current_percentage
                
                #If new highest percentage is found, result is updated.
                result = [float(list[i][0]), #date
                          float(list[j][0]), #date
                          float(highest_percentage)-100]

    #result: [date1, date2, percentage]
    result[0] = dates.unix_to_date(result[0])
    result[1] = dates.unix_to_date(result[1])
    
    print(f"Highest growth was from {result[0]} to {result[1]} by {round(result[2],2)}%")
    print(10*'*'+'\n')

    return



def data_between_dates():
    """
    Prints out most popular currencies at the time and user picks one. 
    Asks 2 dates from user and data is limited between those dates. 
    Prints statistics.
    """

    #Prints currencies and retrieves data from open source, which is
    # set to 'data'
    data = json_read.top_marketcap()

    user_input = input(f"\nChoose currency or 'g' to go back: ")

    if (user_input == 'g'):
        return

    #Goes through retrieved data
    for item in data:

        #if picked currency comes up, if statement is true.
        if (user_input == str(item['market_cap_rank'])):

            #Currency id filtered from json format
            currency = item['id']

            picked_dates = dates.ask_dates()

            if (picked_dates == ["",""]):
                return 
            
            #prices: list of pairs (dates, values)
            prices = json_read.data_by_range(picked_dates, "prices", currency)
            
            print(f"\nData between {dates.unix_to_date(picked_dates[0])} "+
                  f"- {dates.unix_to_date(picked_dates[1])} for {item['name']}")
            
            find_minmax(prices)
            highest_growth(prices)




def main():
    """
    Runs while loop asking user to pick one of 3 options. 
    """

    print('\n'+5*'*'+'Cryptocurrency API project'+5*'*'+'\n')


    while True:

        print('1. Current statistics of chosen currency')
        print('2. Statistics between chosen dates for chosen currency')
        print('Enter "g" to guit\n')

        user_input = input(f"Choose one option: ")

        if (user_input == "1"):
            current_data()

        elif (user_input == "2"):
            data_between_dates()

        elif (user_input == "g"):
            print('Bye!\n')
            break
            
        else:
            print('Something went wrong, try again\n')
            continue
    
    return 0


if __name__ == "__main__":
    main()
import datetime
import time




def ask_dates():
    """
    Asks date from user in 'dd.MM.yyyy' format and turns then into unix format.
    In case user gives incorrect input form, it will run the function again.

    return: pair of dates in unix format
    """

    print("Enter dates in format 'dd.MM.yyyy' or leave empty to go to beginning")

    first_input = input("From: ")
    if (first_input == ""): 
        return ["",""]

    second_input = input("To: ")
    if (second_input == ""): 
        return ["",""]


    try:
        from_unix = int(time.mktime(datetime.datetime.strptime(
                                first_input, "%d.%m.%Y").timetuple()))

        to_unix = int(time.mktime(datetime.datetime.strptime(
                                second_input, "%d.%m.%Y").timetuple()))

    except ValueError:
        print("Sorry, that is in the incorrect format. Try again.")
        return ask_dates()

    except OverflowError as e:
        print('Year out of range. Try again.')
        return ask_dates()


    if (from_unix > time.time() or to_unix > time.time()):
        print("There's no data from future.. yet. Try again.")
        return ask_dates()

    if (from_unix > to_unix):
        print("'From date' was set earlier than 'to date', dates switched.")
        return [to_unix, from_unix]

    return [from_unix, to_unix]

        

def unix_to_date(unix):
    """
    Turns unix formatted date into 'dd.MM.yyyy' format and returns it

    @param unix: date in unix format
    return: date in 'dd.MM.yyyy' format
    """
    return time.strftime("%d.%m.%Y", time.localtime(int(unix)/1000))

import re
import requests

# Make a regular expression for validating correct format of an Email
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

latest_date=[]
customer_list=[]
shipdate_Status_dict = {}
shipdate_Dhltracking_dict = {}
shipdate_Orderid_dict = {}

# Function for validating an Email format
def check(email):
    # pass the regular expression and the string in search() method
    if (re.search(regex, email)):
        return True
    else:
        return False

#Function to check the availabilty of user input in customer database
def verifyUsersExistence(userid):
    cust_api_url = "https://demo7609961.mockable.io/orders/"
    parameter = {"email": userid}
    r = requests.get(url=cust_api_url, params=parameter)
    data = r.json()
    customer_list = data["customer"]["email"]

    if(userid in customer_list):
        return True
    else:
        return False

#Function to get the status of placed order from the Shop API
def fetch_orders(email):
        shop_api_url = "https://demo7609961.mockable.io/orders/"

        #parameters to be sent to the API
        my_customer = {"email": email}

        #GET request and saving the response as response object
        r = requests.get(url = shop_api_url, params = my_customer)

        # extracting data in json format
        data = r.json()
        #print(data)

        for i in data["orders"]:
              shipdate_Dhltracking_dict.update({i['date'] : i['dhl_tracking_id']})
              shipdate_Status_dict.update({i['date'] : i['status']})
              shipdate_Orderid_dict.update({i['date']: i['order_id']})

        for i in sorted(shipdate_Status_dict, reverse=True):
            latest_date.append(i)

        print("Order-id {} is your latest order. Your order was placed on:{}, DHL tracking number is {} and current status is {} ".format(shipdate_Orderid_dict[latest_date[0]],latest_date[0],shipdate_Dhltracking_dict[latest_date[0]],shipdate_Status_dict[latest_date[0]]))
        DHL_status(shipdate_Dhltracking_dict[latest_date[0]])

#Function to extract information from DHL API to get the current status of placed order

def DHL_status(dhl_tracking_id):
    dhl_api_url = "https://demo7609961.mockable.io/dhl/status/"
    dhl_api_key = "dhl_tracking_id"
    r2 = requests.post(url=dhl_api_url, data=dhl_api_key)

    # extracting response text
    dhl_api_key = r2.text

    #Method to parse the xml content into user readable format

    m1 = re.search('<status>(.+?)</status>', dhl_api_key)
    m2 = re.search('<extraInfo>(.+?)</extraInfo>', dhl_api_key)
    m3 = re.search('<shipmentDate>(.+?)</shipmentDate>', dhl_api_key)
    m4 = re.search('<lastUpdate>(.+?)</lastUpdate>', dhl_api_key)

    if m1:
        found = m1.group(1)+"\tto\t"
    if m2:
        found += m2.group(1)+"\nAdditional Information:\tShipment date was on "
    if m3:
        found += m3.group(1)+" and status last updated on\t"
    if m4:
        found += m4.group(1)

    print("Current Status of your order is " + found)



print(
        "############ Welcome to chatbot automation ########### \nPlease provide your email id to know the status of your orders")
choice = input("Enter your email Id ")  #Taking user input as an email
if check(choice):
    # print("Valid Email")
    if verifyUsersExistence(choice):
        #print("Customer Found")
        fetch_orders(choice)
    else:
        print("Customer does not exist!")
else:
    print("Invalid Email!")

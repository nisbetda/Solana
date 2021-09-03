import csv # used to save the file in CSV format
import os
import pandas as pd # dataframe to hold the data
import pprint # makes it pretty
import re 
import requests # access HTTP requests

# Functions:
#  getDynamicAPI()
#  saveData(dataset)
#  checkItems(api_link)

# Make this whole code into a function and use the collection name as the argument
 


# List of Solanart Collections (maybe turn into a menu)
solanart_collections = ["sollamasgraves", "sollamas-gen2", "aurory", "degenape", "boldbadgers"]

#collection_name = "sollamas-gen2"  # change commentfor different collection
collection_name = "sollamasgraves" #(Sollamas)
# collection_name = "aurory" #(Aurory)
# collection_name = "degenape" #(Degen Ape)
# collection_name = "boldbadgers" #(Bold Badgers)

# store the attributes in a dictionary object
attribute_database = {}

# the file name is the collection name
output_file = os.getcwd() + '/{}.csv'.format(collection_name)

# Gets the API subdomain from the website (not an offical API, so no subdomain)
def getDynamicAPI():
    print("Getting dynamic api link. Please wait ...")
    link = "https://solanart.io/collections/{}".format(collection_name)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return ""

    custom_js_link = "https://solanart.io" + \
        resp.split('<script src="')[1].split('"')[0]
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(custom_js_link, headers=headers).text
    except:
        print("Failed to open {}".format(link))
        return ""

    # Parse the API link from the javascript code
    api_link = re.findall(r'REACT_APP_API_NETWORK:"(.+?)"', resp)[0]
    return api_link

# Saves the data into two columns: the attribute and floor price (add a third column to show the number of NFTs listed for each, this is shown in the terminal)
def saveData(dataset):
    with open(output_file, mode='a+', encoding='utf-8', newline='') as csvFile:
        fieldnames = ["Attribute Name", "Lowest Price"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow(
            {"Attribute Name": dataset[0], "Lowest Price": dataset[1]})

# Finds the floor
def checkItems(api_link):
    link = "{}/nft_for_sale?collection={}".format(
        api_link, collection_name)
    # HTTP header to make sure the website accepts our request
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    # make the request from the website and convert the data into a JSON file
    try:
        # print(resp) will show all the data collected
        resp = requests.get(link, headers=headers).json()
    except:
        print("Failed to open {}".format(link))
    # all the unique names of the attriutes from Solanart
    attribute_set = set()

    

    # get the price for the individual attributes
    for item in resp:
        # gets the list of attributes (comma seperated)
        if item.get('attributes') is None:
            continue
        # seperate the attributes
        all_attributes = item.get('attributes').split(',')
        for attribute in all_attributes:
            if attribute.isdigit():
                continue
            attribute_set.add(attribute)

    # alphabetically sort the attributes  
    attribute_set = sorted(list(attribute_set))

    # manually added the collection name
    attribute_set.append("sollamasgen2")

    # loop through the attribute_set and get the lowest price for each attribute
    for attribute_name in attribute_set:
        if attribute_database.get(attribute_name) is None:
            attribute_database[attribute_name] = []

        for item in resp:
            if item.get('attributes') is None:
                continue
            all_attributes = item.get('attributes').split(',')
            if attribute_name in all_attributes:
                attribute_database[attribute_name].append(item.get('price'))
                attribute_database[attribute_name] = sorted(
                    attribute_database[attribute_name])
            if attribute_name == "sollamasgen2" and item.get('type') == attribute_name:
                attribute_database[attribute_name].append(item.get('price'))
                attribute_database[attribute_name] = sorted(
                    attribute_database[attribute_name])

    # sorts by lowest price to Highest Price in order to find the price floor
    for attribute_name in attribute_set:
        try:
            print("{}: {} [total items matched: {}]".format(attribute_name,
                                                            attribute_database.get(attribute_name, [''])[0], len(attribute_database.get(attribute_name))))
            saveData([attribute_name, attribute_database.get(
                attribute_name, [''])[0]])
        except:
            pass

# This is where the program executes
if __name__ == "__main__":
    # deletes the previous file
    if os.path.exists(output_file):
        os.remove(output_file)
    api_link = getDynamicAPI()
    checkItems(api_link)
        


# Convert CSV to Excel file format
# read_file = pd.read_csv (r"{}.csv".format(collection_name))
# read_file.to_excel (r'{}.xlsx'.format(collection_name), index = None, header=True) #will need to change the file name to something that is based on the collection name

# Create a DataFrame to hold the price floor data
# pprint(read_file)

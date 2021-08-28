import requests
import csv
import os
import re


attribute_database = {}
collection_name = "solpunks"  # you can easily change the collection name here
output_file = os.getcwd() + '/SolPunks_attribute_floor.csv'


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
    api_link = re.findall(r'REACT_APP_API_NETWORK:"(.+?)"', resp)[0]
    return api_link


def saveData(dataset):
    with open(output_file, mode='a+', encoding='utf-8', newline='') as csvFile:
        fieldnames = ["Attribute Name", "Lowest Price"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow(
            {"Attribute Name": dataset[0], "Lowest Price": dataset[1]})


def checkItems(api_link):
    link = "{}/nft_for_sale?collection={}".format(
        api_link, collection_name)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).json()
    except:
        print("Failed to open {}".format(link))
    attribute_set = set()
    for item in resp:
        if item.get('attributes') is None:
            continue
        all_attributes = item.get('attributes').split(',')
        for attribute in all_attributes:
            if attribute.isdigit():
                continue
            attribute_set.add(attribute)
    attribute_set = sorted(list(attribute_set))
    attribute_set.append("sollamasgen2")
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
    for attribute_name in attribute_set:
        try:
            print("{}: {} [total items matched: {}]".format(attribute_name,
                                                            attribute_database.get(attribute_name, [''])[0], len(attribute_database.get(attribute_name))))
            saveData([attribute_name, attribute_database.get(
                attribute_name, [''])[0]])
        except:
            pass


if __name__ == "__main__":
    if os.path.exists(output_file):
        os.remove(output_file)
    api_link = getDynamicAPI()
    if api_link == "":
        print("Dynamic API could not be found! Try later!")
    else:
        checkItems(api_link)

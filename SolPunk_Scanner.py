import requests
import csv
import os


attribute_database = {}
output_file = os.getcwd() + '/SolPunk_price_floor.csv'


def saveData(dataset):
    with open(output_file, mode='a+', encoding='utf-8', newline='') as csvFile:
        fieldnames = ["Attribute Name", "Lowest Price"]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        if os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({"Attribute Name": dataset[0], "Lowest Price": dataset[1]})


def checkItems():
    link = "https://83c6ddv6zu.medianet.work/nft_for_sale?collection=solpunks"
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
            saveData([attribute_name, attribute_database.get(attribute_name, [''])[0]])
        except:
            pass


if __name__ == "__main__":
    if os.path.exists(output_file):
        os.remove(output_file)
    checkItems()

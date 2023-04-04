import json


with open("data.json", "r") as write_file:
    # returns JSON object as 
    # a dictionary
    data = json.load(write_file)
    
    # Iterating through the json
    # list
    for i in data:
        print(data[i])

data = {
    "test erserserstring": "newestasdasderest shit"
}

with open("data.json", "w") as write_file:
    json.dump(data, write_file) 
    print("i get heres")
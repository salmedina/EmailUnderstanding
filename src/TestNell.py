'''
Created on Jun 29, 2016

@author: zhongzhu
'''

import json

import requests


literal = "Jon Snow"
params = {"lit1":literal, "predicate":"*", "agent":"KB"}
response = requests.get("http://rtw.ml.cmu.edu/rtw/api/json0", params=params)
print("result is " + response.text)
result = response.json()
 
print("NELL:")
print("The category of \"" + literal + "\" is \"" + result["items"][0]["predicate"] + "\" with score " + str(result["items"][0]["justifications"][0]["score"]))

sentence = "Jon Snow is a fictional character in the A Song of Ice and Fire series of fantasy novels by American author George R. R. Martin."
data = {"action":"plaindoc", "text":sentence, "format":"raw"}
response = requests.post("http://rtw.ml.cmu.edu/rtw/api/mod2015", data=data)
print(response.text + "\n")
print("\nmicroreader (Named entities):")
for line in response.text.split("\n"):
    item = json.loads(line)
    if item["slot"] == "ner" and item["value"] != "O":
        print(sentence[item["spanStart"]:item["spanEnd"]] + " => " + item["value"])
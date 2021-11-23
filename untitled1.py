import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
import numpy as np
import re
import argparse
import os
import os.path as osp
import pandas as pd
from time import sleep

def is_retweet(entry):
        return 'retweeted_status' in entry.keys()
    
def get_source(entry):
    if '<' in entry["source"]:
        return entry["source"].split('>')[1].split('<')[0]
    else:
        return entry["source"]
    
def clean_tweet(tweet):
    if type(tweet) == np.float:
        return ""
    temp = tweet.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
    temp = temp.split()
    #temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputfile", help="Output file name with extension")
    parser.add_argument("-i", "--inputfile", help="Input file name with extension")
    parser.add_argument("-k", "--keyfile", help="Json api key file name")
    parser.add_argument("-c", "--idcolumn", help="tweet id column in the input file, string name")
    parser.add_argument("-m", "--mode", help="Enter e for extended mode ; else the program would consider default compatible mode")


    args = parser.parse_args()
    if args.inputfile is None or args.outputfile is None:
        parser.error("please add necessary arguments")
        
    if args.keyfile is None:
        parser.error("please add a keyfile argument")

    with open(args.keyfile) as f:
        keys = json.load(f)

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)
    
    if api.verify_credentials() == False: 
        print("Your twitter api credentials are invalid") 
        sys.exit()
    else: 
        print("Your twitter api credentials are valid.") 
    
    
    output_file = args.outputfile
    open(output_file, 'a')
    hydration_mode = args.mode

    output_file = args.outputfile
    hydration_mode = args.mode

    output_file_noformat = output_file.split(".",maxsplit=1)[0]
    print(output_file)
    output_file = '{}'.format(output_file)
    output_file_short = '{}_short.json'.format(output_file_noformat)
    print('creating minimized json master file')
    print(output_file)
    with open(output_file_short, 'w') as outfile:
        with open(args.inputfile) as json_data:
            for tweet in json_data:
                data = json.loads(tweet) 
                if hydration_mode == "e":
                    text = data["full_text"]
                else:
                    text = data["text"] 
                    user=data["user"]
                    place = data["place"]
                    print(data["place"])
                    if place is None:
                        continue
                    t = {
                        "created_at": data["created_at"],
                        "text": text,
                        "location": user["location"],
                        "place":place["full_name"],
                        "clean-text": clean_tweet(text)
                    }
                    json.dump(t, outfile)

                    outfile.write('\n')
                
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    fields = ["created_at","text","clean-text", "location","place"]                
    f.writerow(fields)  
    print(outfile)
    with open(output_file_short) as master_file:
        for tweet in master_file:
            data = json.loads(tweet)            
            f.writerow([ data["created_at"],data["text"].encode('utf-8'),
                        data["clean-text"],
                        data["location"],data["place"]])
    
    print("done")

# main invoked here    
main()
import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
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
                    if place is None:
                        continue
                    t = {
                        "created_at": data["created_at"],
                        "text": text,
                        "location": user["location"],
                        "place":place["full_name"],
                        "source": get_source(data),
                    }
                    json.dump(t, outfile)

                    outfile.write('\n')
                
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    fields = ["source", "text","location","place" ,"in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]                
    f.writerow(fields)  
    print(outfile)
    with open(output_file_short) as master_file:
        for tweet in master_file:
            data = json.loads(tweet)            
            f.writerow([data["favorite_count"], data["source"], data["text"].encode('utf-8'),
                        data["location"],data["place"], data["in_reply_to_screen_name"], 
                        data["is_retweet"], data["created_at"], data["retweet_count"],     data["id_str"].encode('utf-8')])
    
    print("done")

# main invoked here    
main()
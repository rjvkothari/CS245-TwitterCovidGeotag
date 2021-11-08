#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   /$$$$$$  /$$      /$$ /$$      /$$ /$$$$$$$$
#  /$$__  $$| $$$    /$$$| $$$    /$$$|__  $$__/
# | $$  \__/| $$$$  /$$$$| $$$$  /$$$$   | $$   
# |  $$$$$$ | $$ $$/$$ $$| $$ $$/$$ $$   | $$   
#  \____  $$| $$  $$$| $$| $$  $$$| $$   | $$   
#  /$$  \ $$| $$\  $ | $$| $$\  $ | $$   | $$   
# |  $$$$$$/| $$ \/  | $$| $$ \/  | $$   | $$   
#  \______/ |__/     |__/|__/     |__/   |__/  
#
#
# Developed during Biomedical Hackathon 6 - http://blah6.linkedannotation.org/
# Authors: Ramya Tekumalla, Javad Asl, Juan M. Banda
# Contributors: Kevin B. Cohen, Joanthan Lucero

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
    hydration_mode = args.mode

    output_file_noformat = output_file.split(".",maxsplit=1)[0]
    print(output_file)
    output_file = '{}'.format(output_file)
    output_file_short = '{}_short.json'.format(output_file_noformat)
    compression = zipfile.ZIP_DEFLATED    
    ids = []
    
    if '.tsv' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile, sep='\t')
        print('tab seperated file, using \\t delimiter')
    elif '.csv' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile)
    elif '.txt' in args.inputfile:
        inputfile_data = pd.read_csv(args.inputfile, sep='\n', header=None, names= ['tweet_id'] )
        print(inputfile_data)
    
    if not isinstance(args.idcolumn, type(None)):
        inputfile_data = inputfile_data.set_index(args.idcolumn)
    else:
        inputfile_data = inputfile_data.set_index('tweet_id')
    
    ids = list(inputfile_data.index)
    print('total ids: {}'.format(len(ids)))

    start = 0
    end = 100
    limit = len(ids)
    i = int(math.ceil(float(limit) / 100))

    last_tweet = None
    if osp.isfile(args.outputfile) and osp.getsize(args.outputfile) > 0:
        with open(output_file, 'rb') as f:
            #may be a large file, seeking without iterating
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        last_tweet = json.loads(last_line)
        start = ids.index(last_tweet['id'])
        end = start+100
        i = int(math.ceil(float(limit-start) / 100))

    print('metadata collection complete')
    print('creating master json file')
    fields =[
	'created_at',
	'id',
	'id_str',
	'text',
	'truncated',
	'source',
	'in_reply_to_status_id',
	'in_reply_to_status_id_str',
	'in_reply_to_user_id',
	'in_reply_to_user_id_str',
	'in_reply_to_screen_name',
	'geo',
	'coordinates',
	'place',
	'contributors',
	'is_quote_status',
	'retweet_count',
	'favorite_count',
	'favorited',
	'retweeted',
	'lang',
	'entities.hashtags',
	'entities.symbols',
	'entities.user_mentions',
	'entities.urls',
	'user.id',
	'user.id_str',
	'user.name',
	'user.screen_name',
	'user.location',
	'user.description',
	'user.url',
	'user.entities.description.urls',
	'user.protected',
	'user.followers_count',
	'user.friends_count',
	'user.listed_count',
	'user.created_at',
	'user.favourites_count',
	'user.utc_offset',
	'user.time_zone',
	'user.geo_enabled',
	'user.verified',
	'user.statuses_count',
	'user.lang',
	'user.contributors_enabled',
	'user.is_translator',
	'user.is_translation_enabled',
	'user.profile_background_color',
	'user.profile_background_image_url',
	'user.profile_background_image_url_https',
	'user.profile_background_tile',
	'user.profile_image_url',
	'user.profile_image_url_https',
	'user.profile_banner_url', 'user.profile_link_color',
	'user.profile_sidebar_border_color',
	'user.profile_sidebar_fill_color',
	'user.profile_text_color',
	'user.profile_use_background_image',
	'user.has_extended_profile',
	'user.default_profile',
	'user.default_profile_image',
	'user.can_media_tag',
	'user.followed_by',
	'user.following',
	'user.follow_request_sent',
	'user.notifications',
	'user.translator_type',
	'user.entities.url.urls',
	'possibly_sensitive',
	'entities.media',
	'extended_entities.media',
	'place.id',
	'place.url',
	'place.place_type',
	'place.name',
	'place.full_name',
	'place.country_code',
	'place.country',
	'place.contained_within',
	'place.bounding_box.type',
	'place.bounding_box.coordinates',
	'quoted_status_id',
	'quoted_status_id_str',
	'quoted_status.created_at',
	'quoted_status.id',
	'quoted_status.id_str',
	'quoted_status.text',
	'quoted_status.truncated',
	'quoted_status.entities.hashtags',
	'quoted_status.entities.symbols',
	'quoted_status.entities.user_mentions',
	'quoted_status.entities.urls',
	'quoted_status.source',
	'quoted_status.in_reply_to_status_id',
	'quoted_status.in_reply_to_status_id_str',
	'quoted_status.in_reply_to_user_id',
	'quoted_status.in_reply_to_user_id_str',
	'quoted_status.in_reply_to_screen_name',
	'quoted_status.user.id',
	'quoted_status.user.id_str',
	'quoted_status.user.name',
	'quoted_status.user.screen_name',
	'quoted_status.user.location',
	'quoted_status.user.description',
	'quoted_status.user.url',
	'quoted_status.user.entities.url.urls',
	'quoted_status.user.entities.description.urls',
	'quoted_status.user.protected',
	'quoted_status.user.followers_count',
	'quoted_status.user.friends_count',
	'quoted_status.user.listed_count',
	'quoted_status.user.created_at',
	'quoted_status.user.favourites_count',
	'quoted_status.user.utc_offset',
	'quoted_status.user.time_zone',
	'quoted_status.user.geo_enabled',
	'quoted_status.user.verified',
	'quoted_status.user.statuses_count',
	'quoted_status.user.lang',
	'quoted_status.user.contributors_enabled',
	'quoted_status.user.is_translator',
	'quoted_status.user.is_translation_enabled',
	'quoted_status.user.profile_background_color',
	'quoted_status.user.profile_background_image_url',
	'quoted_status.user.profile_background_image_url_https',
	'quoted_status.user.profile_background_tile',
	'quoted_status.user.profile_image_url',
	'quoted_status.user.profile_image_url_https',
	'quoted_status.user.profile_banner_url',
	'quoted_status.user.profile_link_color',
	'quoted_status.user.profile_sidebar_border_color',
	'quoted_status.user.profile_sidebar_fill_color',
	'quoted_status.user.profile_text_color',
	'quoted_status.user.profile_use_background_image',
	'quoted_status.user.has_extended_profile',
	'quoted_status.user.default_profile',
	'quoted_status.user.default_profile_image',
	'quoted_status.user.can_media_tag',
	'quoted_status.user.followed_by',
	'quoted_status.user.following',
	'quoted_status.user.follow_request_sent',
	'quoted_status.user.notifications',
	'quoted_status.user.translator_type',
	'quoted_status.geo',
	'quoted_status.coordinates',
	'quoted_status.place',
	'quoted_status.contributors',
	'quoted_status.is_quote_status',
	'quoted_status.retweet_count',
	'quoted_status.favorite_count',
	'quoted_status.favorited',
	'quoted_status.retweeted',
	'quoted_status.possibly_sensitive',
	'quoted_status.lang',
	'quoted_status.entities.media',
	'quoted_status.extended_entities.media',
	'quoted_status.place.id',
	'quoted_status.place.url',
	'quoted_status.place.place_type',
	'quoted_status.place.name',
	'quoted_status.place.full_name',
	'quoted_status.place.country_code',
	'quoted_status.place.country',
	'quoted_status.place.contained_within',
	'quoted_status.place.bounding_box.type',
	'quoted_status.place.bounding_box.coordinates',
	'geo.type',
	'geo.coordinates',
	'coordinates.type',
	'coordinates.coordinates',
	'quoted_status.quoted_status_id',
	'quoted_status.quoted_status_id_str']
    try:
        with open(output_file, 'a') as outfile:
            for go in range(1):
                print('currently getting {} - {}'.format(start, end))
                sleep(6)  # needed to prevent hitting API rate limit
                id_batch = ids[start:end]
                start += 100
                end += 100       
                backOffCounter = 1
                while True:
                    try:
                        if hydration_mode == "e":
                            tweets = api.lookup_statuses(id_batch,tweet_mode = "extended")
                        else:
                            tweets = api.lookup_statuses(id_batch,include_entities=fields)
                            
                        break
                    except tweepy.TweepError as ex:
                        print('Caught the TweepError exception:\n %s' % ex)
                        sleep(30*backOffCounter)  # sleep a bit to see if connection Error is resolved before retrying
                        backOffCounter += 1  # increase backoff
                        continue
                for tweet in tweets:
                    json.dump(tweet._json, outfile)
                    outfile.write('\n')
    except:
        print('exception: continuing to zip the file')

    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(output_file_noformat), mode='w')
    zf.write(output_file, compress_type=compression)
    zf.close()


    def is_retweet(entry):
        return 'retweeted_status' in entry.keys()

    def get_source(entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]
    
    
    print('creating minimized json master file')
    with open(output_file_short, 'w') as outfile:
        with open(output_file) as json_data:
            for tweet in json_data:
                data = json.loads(tweet) 
                if hydration_mode == "e":
                    text = data["full_text"]
                else:
                    text = data["text"] 
                    user=data["user"]
                t = {
                    "created_at": data["created_at"],
                    "text": text,
                    "location": user["location"],
                    "in_reply_to_screen_name": data["in_reply_to_screen_name"],
                    "retweet_count": data["retweet_count"],
                    "favorite_count": data["favorite_count"],
                    "source": get_source(data),
                    "id_str": data["id_str"],
                    "is_retweet": is_retweet(data)
                }
                json.dump(t, outfile)
                
                outfile.write('\n')
                
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    fields = ["favorite_count", "source", "text","location", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]                
    f.writerow(fields)       
    with open(output_file_short) as master_file:
        for tweet in master_file:
            data = json.loads(tweet)            
            f.writerow([data["favorite_count"], data["source"], data["text"].encode('utf-8'),
                        data["location"], data["in_reply_to_screen_name"], 
                        data["is_retweet"], data["created_at"], data["retweet_count"],     data["id_str"].encode('utf-8')])
    

# main invoked here    
main()

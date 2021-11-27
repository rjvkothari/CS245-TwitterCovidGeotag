import io
import pickle
import sys
import os
from os import path, makedirs
from tensorflow import keras
import pandas as pd

sys.path.insert(0, path.abspath('../../'))

_dirname = path.dirname(path.abspath(__file__))

_TWITTER_PARSED_TEST_DATA = 'twus_test.pickle'
_TWITTER_PARSED_DEV_DATA = 'twus_dev.pickle'
_TWITTER_PARSED_TRAIN_DATA = 'twus_train.pickle'

_TWITTER_PARSED_TEST_DATA_DROPBOX = "https://dl.dropbox.com/s/kg09i1z32n12o98/twus_dev.pickle"
_TWITTER_PARSED_DEV_DATA_DROPBOX = "https://dl.dropbox.com/s/ze4ov5j30u9rf5m/twus_test.pickle"
_TWITTER_PARSED_TRAIN_DATA_DROPBOX = "https://dl.dropbox.com/s/0d4l6jmgguzonou/twus_train.pickle"
_TWITTER_CSV_DEV_DATA_DROPBOX = "https://dl.dropbox.com/s/8drqqugn5fw7zbx/twus_dev.csv"
_TWITTER_CSV_DEV_DATA_MD5 = "4e60b193ae5f4232c80d6e5f27b8c94e"

temp_dev_data = keras.utils.get_file(_TWITTER_PARSED_DEV_DATA, _TWITTER_PARSED_DEV_DATA_DROPBOX)
temp_test_data = keras.utils.get_file(_TWITTER_PARSED_TEST_DATA, _TWITTER_PARSED_TEST_DATA_DROPBOX)
temp_train_data = keras.utils.get_file(_TWITTER_PARSED_TRAIN_DATA, _TWITTER_PARSED_TRAIN_DATA_DROPBOX)

print("Loading dev set")
with open(temp_dev_data, 'rb') as handle:
    dev_data = pickle.load(handle)

print("Loading test set")
with open(temp_test_data, 'rb') as handle:
    test_data = pickle.load(handle)

print("Loading train set")
with open(temp_train_data, 'rb') as handle:
    train_data = pickle.load(handle)


dev_df = pd.DataFrame(dev_data, columns=['username', 'tweets', 'state', 'region', 'state_name', 'region_name'])
test_df = pd.DataFrame(test_data, columns=['username', 'tweets', 'state', 'region', 'state_name', 'region_name'])
train_df = pd.DataFrame(train_data, columns=['username', 'tweets', 'state', 'region', 'state_name', 'region_name'])

print("Saving all as CSV")
print("Training set size:", len(train_df))
print("Testing set size:", len(test_df))
print("Dev set size:", len(dev_df))

train_df.to_csv("TRAININGDATA.csv")
test_df.to_csv("TESTINGDATA.csv")
dev_df.to_csv("DEVDATA.csv")



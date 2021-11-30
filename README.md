# CS245-TwitterCovidGeotag
CS245 - Covid twitter geotag 

Use Twitter retriever in jupyter labs to quickly process data. 
Update the API_keys.json with your keys
Currently set to use only 100 at a time. Line 285 in Get_metadata.py - switch 1 to i for all the tweets

## Datasets

**CMU Data**
| | # Users | # Tweets | # Tweets/User |
|-|-|-|-|
| Train | 5,685 | 219,608 | 38.63 |
| Dev | 1,895 | 74,347 | 39.23 |
| Test | 1,895 | 74,192 | 39.15 |

**NA Data**
| | # Users | # Tweets | # Tweets/User |
|-|-|-|-|
| Train | 410,336 | 34,460,594 | 83.98 |
| Dev | 9.533 | 788,860 | 82.58 |
| Test | 9.546 | 818,596 | 85.75 |

## Results

**Expt Setup:** Train on CMU data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | Low-Tweet | Normal-Tweet |
|---|---|---|
| CNN | 9.3 |  |
| RNN | 6.88 |   |
| Fasttext | 6.88 |   |
| BiLSTM-Relation | 6.88 |   |

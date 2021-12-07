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

**Partially Filtered COVID data (PFC)**
| | # Users | # Tweets | # Tweets/User |
|-|-|-|-|
| Train | 2,000 | 97,421 | 48.71 |
| Dev | 1,000 | 48,684 | 48.68 |
| Test | 1,636 | 79,405 | 48.54 |

**Low-Tweet COVID data (LTC)**
| | # Users | # Tweets | # Tweets/User |
|-|-|-|-|
| Test | 1,257 | 12.557 | 9.99 |

## Results

**Baseline Setup:** Train on PFC train data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | LTC | PFC |
|---|---|---|
| CNN | 7.7 | 6.78 |
| RNN |  |  |
| Fasttext | 6.84 | 10.24 |
| BiLSTM-Relation |  |  |
| Stacked LSTM | 7.8 | 7.1 |

**Expt Setup 1:** Train on CMU data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | LTC | PFC |
|---|---|---|
| CNN | 9.3 | 7.53 |
| RNN | 8.88 | 10.1  |
| Fasttext | 6.88 | 4.57 |
| BiLSTM-Relation | 6.95 | 6.53 |
| Stacked LSTM | 7.31 | 6.72 |

**Expt Setup 2:** Train on NA data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | LTC | PFC |
|---|---|---|
| CNN | 7.7 | 8.45 |
| RNN | 13.36 | 9.19 |
| Fasttext |  |  |
| BiLSTM-Relation |  |  |
| Stacked LSTM |  | 8.7 |

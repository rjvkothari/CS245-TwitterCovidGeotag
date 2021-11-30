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
| CNN |  |  |
| RNN |  |   |
| Fasttext |  |   |
| BiLSTM-Relation |  |   |

**Expt Setup 1:** Train on CMU data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | LTC | PFC |
|---|---|---|
| CNN | 9.3 |  |
| RNN | 6.88 |   |
| Fasttext | 6.88 |   |
| BiLSTM-Relation | 6.88 |   |

**Expt Setup 2:** Train on NA data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | LTC | PFC |
|---|---|---|
| CNN |  |  |
| RNN |  |   |
| Fasttext |  |   |
| BiLSTM-Relation |  |   |

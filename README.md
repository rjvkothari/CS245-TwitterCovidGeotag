# CS245-TwitterCovidGeotag
CS245 - Covid twitter geotag 

Use Twitter retriever in jupyter labs to quickly process data. 
Update the API_keys.json with your keys
Currently set to use only 100 at a time. Line 285 in Get_metadata.py - switch 1 to i for all the tweets

## Datasets

**CMU Data**
| | # Users | # Tweets |
|-|-|-|
| Train | 5,685 | 219,608 |
| Dev | 1,895 | 74,347 |
| Test | 1,895 | 74,192 |

## Results

**Expt Setup:** Train on CMU data. Testing on COVID-related datasets. Evaluation metric is accuracy (reported in percentage).

| Model Name | Low-Tweet | Normal-Tweet |
|---|---|---|
| CNN | 9.3 |  |
| RNN | 6.88 |   |
| Fasttext | 6.88 |   |
| BiLSTM-Relation | 6.88 |   |

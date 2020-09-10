## Information-Retrieval-CSE-535-University-at-Buffalo-New-York

### Project 1 : Data Crawling from Twitter

#### Data Crawling (Tweets) of fifteen influential personalities (5 from each of the 3 chosen countries: India, USA and Brazil) from Twitter

**Tweets posted by the personalities and their replies in a given time frame of 5 days**

The folder contains files that perform the following tasks:

*Fetching tweets from Twitter API using Twitter Developer platform
*Fetching replies of followers for the particular tweet
*JSON Parser to parse the response file and modifying fields based on the requirement
*Datetime util to get the data in the desired time frame

**Other information:**

[1] TWARC command is also used to fetch tweets from command prompt using the command:

                         _twarc sample > tweets.json_
                         
[2] The json dump after being formatted has been uploaded to Apache Solr for grading and model evaluation purposes.

[3] Document indexing has been performed using Solr.

### Project 2: Document Ranking by calculating TF-IDF 

### Project 3: Document model evaluation using TREC and comparing which model performed the best out of BMR25, DFR and LM

The folder contains files that perform the following tasks:

*We developed a python script which parses the queries in the query text file sequentially and returns the query results into a new text file for each of the models by running the query url.
*JSON to TREC evaluating script

# Sentiment Analysis API

- Individual Opinion Polarity was computed by processing the review line by line
and pairing the nouns with corresponding adjectives. The weight of the
identified nouns were averaged to evaluate the sentiment of the review.
- Modified TF-IDF Algorithm was used for feature selection in the reviews which
aimed to differentiate the most significant features of opinions from the
irrelevant content.
- Pandas and NLTK Python Libraries were used for sentiment analysis.
- Added support for clustering of reviews along with generating summarized text for each of these clusters.
- Clustered reviews can be visualized using D3 library supporting flare.json format.
- The entire Sentiment Analysis Engine was extended as a Flask API which can be queried externally.


from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.naive_bayes import BernoulliNB
import json 


with open("imdb_labelled.txt", "r") as text_file:
    lines = text_file.read().split('\n')
    
with open("amazon_cells_labelled.txt", "r") as text_file:
    lines += text_file.read().split('\n')
    
with open("yelp_labelled.txt", "r") as text_file:
    lines += text_file.read().split('\n')
    

lines = [line.split("\t") for line in lines if len(line.split("\t"))==2 ]

train_documents = [line[0] for line in lines]


train_labels = [int(line[1]) for line in lines ]

count_vectorizer = CountVectorizer()
train_documents = count_vectorizer.fit_transform(train_documents)

classifier = BernoulliNB()
classifier.fit(train_documents, train_labels)


def getPrediction(comment):
    result = classifier.predict(count_vectorizer.transform([comment]))
    value = result.item()

    if (value == 1):
        interpretation = "Positive "

    else:
        interpretation = "Negative"

    Body = {

        "Comment": comment,
        "Value" : value,
        "Interpretation": interpretation
    }
    return Body



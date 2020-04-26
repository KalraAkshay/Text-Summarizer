# Creating an Article Summarizer

# importing libraries
import bs4
import urllib.request
import re
import nltk
nltk.download('stopwords')
import heapq

# Getting the data from web
source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Global_warming').read()
soup = bs4.BeautifulSoup(source, 'lxml')

text = ""
for paragraph in soup.find_all('p'):
    text = text + paragraph.text

# pre-processing the text
text = re.sub(r"\[[0-9]*\]", " ", text)
text = re.sub(r"\s+", " ", text)
clean_text = text.lower()
clean_text = re.sub(r"\W", " ", clean_text)
clean_text = re.sub(r"\d", " ", clean_text)
clean_text = re.sub(r"\s+", " ", clean_text)

# Tokenization
sentences = nltk.sent_tokenize(text)
stop_words = nltk.corpus.stopwords.words('english')

# Creating a Histogram
word2count = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] = word2count[word]+1

# Creating a weighted Histogram
for key in word2count.keys():
    word2count[key] = word2count[key]/max(word2count.values())

# Calculating the scores
sent2score ={}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' ')) < 25:
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] = sent2score[sentence] + word2count[word]

# Getting the summary
best_sentences = heapq.nlargest(5, sent2score, key=sent2score.get)
print("---------Summary-------------------")

for sentence in best_sentences:
    print(sentence)
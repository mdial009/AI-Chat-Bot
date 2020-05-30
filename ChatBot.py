# Description: This is a "Smart" Chat Bot Program

# Import the Libraries
import nltk
from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
import sys

warnings.filterwarnings("ignore")

# Download's The Punkt Package
nltk.download("punkt", quiet=True)

# Get the Article
# article = input("Enter A URL: ")
#Example URl "https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521"

article = Article(input("Enter A URL: "))
article.download()
article.parse()
article.nlp()
corpus = article.text

# Print The Articles Text
# print(corpus)

# Tokenization
text = corpus
sentence_list = nltk.sent_tokenize(text)  # Give Us A List Of Sentences
# Print The List Of Sentences
# print(sentence_list)

# A Function To Return A Random Greeting Response To A Users Greeting
def greeting_response(text):
    text = text.lower()

    # Bots Greeting Response
    bot_greetings = ["howdy", "hi", "hey", "hello", "hola"]
    # Users Greeting
    user_greetings = ["hi", "hey", "hello", "hola", "greetings", "wassup"]

    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # Swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index


# Create The Bots Response
def bot_response(user_input):
    user_input = user_input.upper()
    sentence_list.append(user_input)
    bot_response = ""
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + " " + sentence_list[index[i]]
            response_flag = 1
            j = j + 1
        if j > 2:
            break

        if response_flag == 0:
            bot_response = bot_response + " " + "I apologize, I don't understand."
        sentence_list.remove(user_input)

        return bot_response


# Start The Chat
print(
    "T. O. Morrow: Hi I am T. O. Morrow or T. O. Bot for short. I can answer all your questions about anything. If you want to exit, type exit/see you later/bye/quit/break."
)

exit_list = ["exit", "see you later", "bye", "quit", "break"]

while True:
    user_input = input()
    if user_input.lower() in exit_list:
        print("T. O. Morrow: Chat with you later buddy!")
    else:
        if greeting_response(user_input) != None:
            print("T. O. Morrow:" + greeting_response(user_input))
        else:
            print("T. O. Morrow: " + bot_response(user_input))
    if user_input in exit_list:
        sys.exit()

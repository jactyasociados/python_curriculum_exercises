#!/usr/bin/env python3

import csv
from datetime import datetime, timezone
import itertools
import json

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup

import pandas as pd

# Requests is a Python HTTP library
import requests

# lxml is a Python library which allows for easy handling of XML and HTML files.
import lxml


class GoogleNewsHeadlines(object):
    """The GoogleNewsHeadlines class creates and object by collecting the news
    headlines found on www.news.google.com. The methods provide different
    formates to view the data"""

    # This list is to filter out any words (str) that are single letters
    alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                'q','r','s','t','u','v','w','x','y','z']

    # This list is to filter out any numbers that may appear in the text
    string_numbers_list = ['0','1','2','3','4','5','6','7','8','9']

    # This list is to filter out and punctuation from the word_count function
    punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
                   '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']

    # This list is to filter out any unwanted words from the word_count function
    ignore_word_list = ['', 'a', 'about', 'after', 'all', 'amid', 'an', 'and', 
                        'are', 'as', 'at', 'be', 'but', 'by', 'can', 'could', 
                        'during', 'for', 'from', 'get', 'gets', 'has', 'have', 
                        'he', 'his', 'how', 'if', 'in', 'is', 'it', 'it\'s', 
                        'new', 'news', 'not', 'of', 'on', 'or', 'out', 'says', 
                        'takes', 'than', 'that', 'the', 'this', 'to', 'was', 
                        'will', 'what', 'when', 'with', 'who', 'why', 'won\'t',]

    # This lambda funciton is used to check if a word (str) is unicode
    isascii = lambda self, s: len(s) == len(s.encode())


    #  __init__ uses Requests and BeautifulSoup to collect all of the google
    #  news headlines 
    def __init__(self):
        super(GoogleNewsHeadlines, self).__init__()
        r = requests.get('https://news.google.com/')
        soup = BeautifulSoup(r.text, 'lxml')
        self.source = soup.findAll(True, {'class':['DY5T1d', 'wEwyrc']})
        self.timestamp = datetime.now(timezone.utc)
        

    def _clean_word_list(self, word_list):
        clean_word_list = []
        for word in word_list:
            if word[0] in self.punctuation_list:
                word = word.replace(word[0], '')
            elif word[-1] in self.punctuation_list:
                word = word.replace(word[-1], '')
            if (word not in self.ignore_word_list and
                word not in self.punctuation_list and
                word not in self.alphabet_list and 
                word not in self.string_numbers_list and
                self.isascii(word) == True):
                clean_word_list.append(word.lower())
        return clean_word_list


    def pandas_dataframe(self):
        results = []
        iter_source =  iter(self.source)
        num_of_headlines = len(self.source) / 2
        for headline in iter_source:
            href = headline.__getitem__('href')
            url = 'https://news.google.com' + href
            org = next(iter_source)
            results.append(
                [headline.text,
                url,
                org.text, 
                num_of_headlines,
                self.timestamp,]
                )
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        colNames = ['headline',
                    'url',
                    'organization',
                    'count',
                    'timestamp',
                    ]
        df = pd.DataFrame(data = results, columns = colNames)
        return df


    def pd_as_dict(self):
        df = self.pandas_dataframe()
        return df.to_dict(orient='index')


    def pd_as_json(self):
        df = self.pandas_dataframe()
        df = df.rename(columns={'timestamp': 'unix_timestamp'})
        return df.to_json(orient='index')


    def pd_as_table_schema_json(self):
        df = self.pandas_dataframe()
        df['timestamp'] = pd.to_datetime(df.timestamp.astype(str), errors='coerce')
        df = df.rename(columns={'timestamp': 'pandas_timestamp'})
        return df.to_json(orient='table')


    def pd_to_csv(self):
        data_dict = self.pandas_dataframe()
        data_dict.to_csv('google_news_headlines.csv', index=False)


    def pd_word_count(self):
        df = self.pandas_dataframe()
        word_list = [x.lower().split() for x in df['headline']]
        word_list = list(itertools.chain.from_iterable(word_list))
        word_list = self._clean_word_list(word_list)

        colNames = ['word']
        df = pd.DataFrame(data = word_list, columns = colNames)
        df = df.dropna(subset=['word'])

        new_list = []
        word_count = df.shape[0]
        x = 1
        while x <= df.shape[0]:
            word = df['word'].value_counts().idxmax()
            count = df['word'].value_counts().max()
            new_list.append([word, count, self.timestamp, word_count])
            df = df[df.word != word]
            x += 1
            
        colNames = ['word','count','timestamp','word_count']
        return pd.DataFrame(data = new_list, columns = colNames)


    def pd_word_count_as_dict(self):
        df = self.pd_word_count()
        return df.to_dict(orient='index')


    def pd_word_count_as_json(self):
        df = self.pd_word_count()
        df = df.rename(columns={'timestamp': 'unix_timestamp'})
        return df.to_json(orient='index')


    def pd_word_count_as_table_schema_json(self):
        df = self.pd_word_count()
        df['timestamp'] = pd.to_datetime(df.timestamp.astype(str), errors='coerce')
        df = df.rename(columns={'timestamp': 'pandas_timestamp'})
        return df.to_json(orient='table')


    def pd_word_count_to_csv(self):
        data_dict = self.pd_word_count()
        data_dict.to_csv('google_news_headlines_word_count.csv', index=False)
        


def main():
    pass
    data = GoogleNewsHeadlines()
    response = 0
    print('''
Welcome to the Google News Headlines project by Michael Delgado.

This project gathers all Google News headlines and related news organizations.

You can view the data in a few different formats. 

        ''')
    while response != 11:
        print('''
Select an option:
[1] View data as a Pandas Dataframe
[2] View Pandas Dataframe as a Python dictionary
[3] View Pandas Dataframe as a JSON
[4] View Pandas DataFrame as table schema json
[5] View Pandas DataFrame Word Count
[6] View Pandas Dataframe Word Count as a Python dictionary
[7] View Pandas Dataframe Word Count as a JSON
[8] View Pandas DataFrame Word Count as table schema json

[9] Save Pandas Dataframe to csv 
[10] Save Pandas Dataframe Word Count to csv

[11] Exit program
            ''')
        response = input('Please enter your selection: ')

        if response in ['1','2','3','4','5','6','7','8','9','10','11']:
            if response == '1':
                print(data.pandas_dataframe())
            if response == '2':
                print(data.pd_as_dict())
            if response == '3':
                print(data.pd_as_json())
            if response == '4':
                print(data.pd_as_table_schema_json())
            if response == '5':
                print(data.pd_word_count())
            if response == '6':
                print(data.pd_word_count_as_dict())
            if response == '7':
                print(data.pd_word_count_as_json())
            if response == '8':
                print(data.pd_word_count_as_table_schema_json())
            if response == '9':
                print(data.pd_to_csv())
            if response == '10':
                print(data.pd_word_count_to_csv())
            if response == '11':
                print('''
Thank you for using the Google News Headlines project by Michael Delgado.
Goodbye for now!
                    ''')
                break
        else:
            print('''
< Error: Invalid Selection >

Please try again.
                ''')



if __name__ == '__main__':
    main()



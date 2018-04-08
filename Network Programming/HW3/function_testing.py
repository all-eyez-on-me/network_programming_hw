from flask import Flask
from flask import request
from flask import render_template, jsonify
from flask import current_app
import pandas as pd
import nltk


movies = pd.read_csv('imdb_top1000.csv')
def sort_index(series):
    rows = len(series.index)
    title_list = series
    title_split_list = []
    for i in range(rows):
        title_split_list.append(nltk.word_tokenize(title_list[i]))
    title_index = {}
    i = 0
    for title_split in title_split_list:
        for split_element in title_split:
            if split_element in title_index.keys():
                title_index[split_element].append(i)
            else:
                title_index[split_element] = [i]
        i = i + 1
    return title_index

def sort_by_attribute(index_list, sort_by, order):
    parse_pd = movies.loc[index_list,:]
    print(parse_pd)
    return parse_pd.sort_values(by = sort_by,
                                ascending= order)

title_index = sort_index(movies['Title']);
actor_index = sort_index(movies['Actors']);

def search_type(frame):
    return {"Actors": frame["Actors"],
           "Director": frame["Director"],
           "Genre": frame["Genre"],
           "Rating": float(frame["Rating"]),
           "Revenue (Millions)": float(frame["Revenue (Millions)"]),
           "Title": frame["Title"],
           "Year": int(frame["Year"]),
           "id": int(frame["Rank"]) - 1}

def search(query, attribute, sortby, order, ):
# Retrieve values of a and b from query string
    query = query.lower()
    sortby = sortby.capitalize()
    order = order.capitalize()
    attribute = attribute.capitalize()
    if not attribute in ['Title', 'Actor','Both']:
        return 0
    if not sortby in ['Year', 'Revenue','Rating']:
        return 0
    if not order in ['Ascending', 'Descending']:
        return 0
    if attribute == 'Title':
        if query in title_index.keys():
            index_list = title_index[query]
        else:
            return 0
    elif attribute == 'Actor':
        if query in actor_index.keys():
            index_list = actor_index[query]
        else:
            return 0
    else:
        if query in actor_index.keys() or query in title_index.keys():
            index_list = title_index[query]+actor_index[query]
        else:
            return 0
    sort_index = sorted(index_list,  key=lambda x:movies[sortby][x])

    result_list = []
    for index in sort_index:
        result_list.append(search_type(movies.loc[index]))
    return result_list






if __name__ == '__main__':

    #print(title_index)
    #print(actor_index)
    #print(sort_by_attribute(title_index['of'],'Rank', True), )
    #print(title_index['123'])
    result = search('of','Title', 'rating', 'ascending')
    print(result)

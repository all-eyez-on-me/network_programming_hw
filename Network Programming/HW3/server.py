from flask import Flask
from flask import request
from flask import jsonify
from flask import current_app
import pandas as pd
import nltk
import datetime
import time
from sys import argv

def sort_index(series):
    rows = len(series.index)
    title_list = series
    title_split_list = []
    for i in range(rows):
        tmp_list = nltk.word_tokenize(title_list[i])
        title_split_list.append([element.lower() for element in tmp_list])
    title_index = {}
    i = 0
    for title_split in title_split_list:
        for split_element in title_split:
            if split_element in title_index.keys():
                title_index[split_element.lower()].append(i)
            else:
                title_index[split_element.lower()] = [i]
        i = i + 1
    return title_index


app = Flask('__name__')
movies = pd.read_csv('imdb_top1000.csv')
movies = movies.fillna(0)
movies.insert(0, 'comments', [list() for x in range(len(movies.index))])
app.title_index = sort_index(movies['Title'])
app.actor_index = sort_index(movies['Actors'])
app.movies = movies
app.time_now = time.time()


def search_type(frame):
    return {"Actors": frame["Actors"],
           "Director": frame["Director"],
           "Genre": frame["Genre"],
           "Rating": float(frame["Rating"]),
           "Revenue (Millions)": float(frame["Revenue (Millions)"]),
           "Title": frame["Title"],
           "Year": int(frame["Year"]),
           "id": int(frame["Rank"]) - 1}

def get_type(frame):
    return {"Actors": frame["Actors"],
            "Description":frame["Description"],
            "Director": frame["Director"],
            "Genre": frame["Genre"],
            "Metascore":float(frame["Rating"]),
            "Rank":float(frame["Rank"]),
            "Rating": float(frame["Rating"]),
            "Revenue (Millions)": float(frame["Revenue (Millions)"]),
            "Runtime(Minutes)": float(frame["Runtime (Minutes)"]),
            "Votes": float(frame["Votes"]),
            "Title": frame["Title"],
            "Year": int(frame["Year"]),
            "comments": frame["comments"],
            "id": int(frame["Rank"]) - 1}
def comment_type(frame):
    return {"Actors": frame["Actors"],
            "Description":frame["Description"],
            "Director": frame["Director"],
            "Genre": frame["Genre"],
            "Metascore":float(frame["Rating"]),
            "Rank":float(frame["Rank"]),
            "Rating": float(frame["Rating"]),
            "Revenue (Millions)": float(frame["Revenue (Millions)"]),
            "Runtime(Minutes)": float(frame["Runtime (Minutes)"]),
            "Votes": float(frame["Votes"]),
            "Title": frame["Title"],
            "Year": int(frame["Year"]),
            "comments": frame["comments"],
            "id": int(frame["Rank"]) - 1}

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("query",  type=str)
    attribute = request.args.get("attribute", type=str).capitalize()
    sortby = request.args.get("sortby",  type=str).capitalize()
    order = request.args.get("order",  type=str).capitalize()
    if not attribute in ['Title', 'Actor','Both']:
        result ={"attribute":"Wrong"}
        return jsonify(result)
    if not sortby in ['Year', 'Revenue','Rating']:
        result ={"sortby":"Wrong"}
        return jsonify(result)
    if not order in ['Ascending', 'Descending']:
        result ={"order":"Wrong"}
        return jsonify(result)
    if attribute == 'Title':
        if query in current_app.title_index.keys():
            index_list = current_app.title_index[query]
        else:
            result = {"title": "cannot find"}
            return jsonify(result)
    elif attribute == 'Actor':
        if query in current_app.actor_index.keys():
            index_list = current_app.actor_index[query]
        else:
            result = {"actor": "cannot find"}
            return jsonify(result)
    else:
        if query in current_app.actor_index.keys() or query in current_app.title_index.keys():
            index_list = current_app.title_index[query]+current_app.actor_index[query]
        else:
            result = {"actor_title": "cannot find"}
            return jsonify(result)
    if order == "Ascending":
        sort_index = sorted(index_list,  key=lambda x:movies[sortby][x])
    else:
        sort_index = sorted(index_list, key=lambda x: movies[sortby][x],reverse=True)

    if(len(sort_index)>10):
        sort_index = sort_index[:10]
    result_dict = {'movies':[]}
    for index in sort_index:
        result_dict['movies'].append(search_type(movies.loc[index]))
    return jsonify(result_dict)


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_get(movie_id):
    if int(movie_id) >= len(current_app.movies.index) or int(movie_id)<0:
        result ={"Warning":"Error movie_id"}
        return jsonify(result)
    else:
        print(len(current_app.movies.index)-1)
        movie_result = current_app.movies.loc[int(movie_id)]
        return_type = get_type(movie_result)
        return jsonify(return_type)

@app.route('/comment', methods=['POST'])
def write_comment():
    user_name = request.form.get("user_name")
    movie_id = int(request.form.get("movie_id"))
    comment = request.form.get("comment")
    time_stamp = datetime.datetime.fromtimestamp(current_app.time_now).strftime('%Y-%m-%d %H:%M:%S')
    comment_dict = {"comment":comment,
                    "timestampe":time_stamp,
                    "user_name":user_name}
    #wat = current_app.movies.loc[movie_id, "comments"]
    if not current_app.movies.loc[movie_id, "comments"]:
        current_app.movies.loc[movie_id, "comments"] = [comment_dict]
        comment_list = [comment_dict]
    else:
        current_app.movies.loc[movie_id, "comments"].append(comment_dict)
    result = comment_type(current_app.movies.loc[movie_id])
    return jsonify(result)





if __name__ == '__main__':
    if len(argv)==2:
        app.run(host="localhost", port=int(argv[1]))
    else:
        print("Please provide correct argv of program")
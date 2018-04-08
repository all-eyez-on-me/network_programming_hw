import requests
from sys import argv
if __name__ == '__main__':


    if len(argv)==8:
        host = argv[1]
        port = argv[2]
        query = argv[4]
        attribute = argv[5]
        sortby = argv[6]
        order = argv[7]
        data={"query":query,
              "attribute":attribute,
              "sortby":sortby,
              "order":order}
        #print(data)
        resp = requests.get("http://%s:%s/search" % (host, port),
                            params=data)
    elif len(argv)== 5:
        host = argv[1]
        port = argv[2]
        movie_id = int(argv[4])
        resp = requests.get("http://%s:%s/movie/%d" % (host, port,movie_id))
    elif len(argv)==6:
        host = argv[1]
        port = argv[2]
        user_name = argv[4]
        movie_id =  argv[5]
        # host = "localhost"
        # port = 8080
        comment = input("What is your comment? <User inputs his/her comment here and press enter>")
        resp = requests.post("http://%s:%s/comment" % (host, port),
                          data={'user_name': user_name,
                                "movie_id": movie_id,
                                "comment": comment})
    else:
        print("please input correct argument")
        print("For example:")
        print("localhost 50000 search world title year descending")
        print("localhost 50000 movie 85")
        print("localhost 50000 comment albert 85")
    print(resp.text)
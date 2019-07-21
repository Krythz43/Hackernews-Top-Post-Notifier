import requests
import os
import pickle

http_proxy  = "http://172.16.2.30:8080"
https_proxy = "https://172.16.2.30:8080"

proxy = { 
          "http"  : http_proxy, 
          "https" : https_proxy,
        }

# link for Hackernews top pages
def get_top_post_ID():

    link="https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    r=requests.get(link,proxies=proxy)
    top_post=r.json()[0]
    return top_post

def get_top_post(top_post):

    link="https://hacker-news.firebaseio.com/v0/item/"+str(top_post)+".json?print=pretty"
    r=requests.get(link,proxies=proxy)
    title=r.json()["title"]
    link=r.json()["url"]
    return title,link



if __name__ == "__main__":
    prev_top_post=-1
    data_file="test.data"

    # try:
    #     fd = open(data_file, 'rb')
    #     dataset = pickle.load(fd)
    #     prev_top_post=dataset[0]
    # except:
    #     prev_top_post=-1

    top_post=get_top_post_ID()
    if prev_top_post==top_post:
        exit()
    
    dataset = [top_post]
    fw = open(data_file, 'wb')
    pickle.dump(dataset, fw)
    fw.close()

    os.environ['TOP_POST']=str(top_post)
    title,link=get_top_post(top_post)
    os.system('notify-send -u normal "New top post on HackerNews : '+title+' " "'+link+'" ')
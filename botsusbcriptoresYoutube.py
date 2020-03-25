import httplib2
from apiclient import discovery
import pandas as pd
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import client
from oauth2client import tools
client_secrets_file = "YOURCLIENTSECRET"

api_service_name = "youtube"
api_version = "v3"

scopes = ["https://www.googleapis.com/auth/youtube","https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

def getDataframe(valuesSettings):
    df = pd.DataFrame.from_records(valuesSettings)
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    #df['Division']=df['Division'].str.title()
    return df.reset_index(drop=True)

def get_authenticated_service():
  flow = flow_from_clientsecrets('./credentials/'+client_secrets_file,
    scope=scopes,
    message='')

  storage = Storage('./credentials/'+client_secrets_file+'python-quickstart.json')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, None)

  return discovery.build(api_service_name, api_version,
    http=credentials.authorize(httplib2.Http()))
def likeVideo(videoId,youtube):
    request = youtube.videos().rate(
        id=videoId,
        rating="like"
    )
    request.execute()
def commentVideo(videoId,textOriginal,youtube):
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
              "snippet": {
                "videoId": videoId,
                "topLevelComment": {
                  "snippet": {
                    "textOriginal": textOriginal
                  }
                }
              }
            }
        )

        response = request.execute()
        time.sleep(3)
    except Exception as e:
        print(e)

def getLast5Videos(channelId,youtube):
    pks=[]
    try:
      datapk=pd.read_csv("channeltovideo.csv", sep=';')
      datapkchannelIdchannelId=datapk[(datapk['channelId']==channelId)].reset_index(drop=True)
      pks=datapkchannelId['videoId'].tolist()
    except Exception as e:
      datapk=None
      pks=[]
    videos = []
    pageToken=''
    search_response = youtube.search().list(
    channelId=channelId,
    part="id,snippet",
    type="video",
    order='date',
    pageToken=pageToken,
    maxResults=5
  ).execute()
    pageToken=search_response.get("nextPageToken")
    print(pageToken)
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append(search_result)
    print(videos)
  
    return videos



def subscriptions(channel_id,youtube):
    add_subscription_response = youtube.subscriptions().insert(
      part='snippet',
      body={
        "snippet": {
          "resourceId": {
            "kind": 'youtube#channel',
            "channelId": channel_id
          }
        }

      }).execute()

    return add_subscription_response["snippet"]["title"]
    




#pip install -r requeriments.txt
#https://console.developers.google.com/apis/
if __name__ == "__main__":
    youtube = get_authenticated_service()
    likeVideo('Oyja_2i-p9I',youtube)




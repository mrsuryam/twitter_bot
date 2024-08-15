import tweepy 
import schedule
import time
import json
import os

class Tweeter():

    fileNum = None

    api = None
    client = None
    sessionKeys = None
    #initialize variables 
    def init():
        pass

    def getKeys(self):
        with open('config.json') as f:
            self.sessionKeys = json.load(f)
            print(self.sessionKeys)
        
        #apiKey = sessionKeys['apiKey']
        #apiKeySecret = sessionKeys['apiKeySecret']
        #accessToken = sessionKeys['accessToken']
        #accessTokenSecret = sessionKeys['accessTokenSecret']
        #path = sessionKeys['path']
        #totalFrames = sessionKeys['totalFrames']
        #movieName = sessionKeys['movieName']       

    def initAuth(self):

        apiKey = self.sessionKeys['apiKey']
        apiKeySecret = self.sessionKeys['apiKeySecret']
        accessToken = self.sessionKeys['accessToken']
        accessTokenSecret = self.sessionKeys['accessTokenSecret']

        auth = tweepy.OAuthHandler(apiKey, apiKeySecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        # Create client object
        self.client = tweepy.Client(
            consumer_key=apiKey,
            consumer_secret=apiKeySecret,
            access_token=accessToken,
            access_token_secret=accessTokenSecret
        )

        # Create API object
        self.api = tweepy.API(auth)


    def getFileNum(self):
        #for i in range(1, int(self.sessionKeys['totalFrames']) + 1):
        #    yield i
        with open('file') as f:
            return int(f.read())

    def updateFile(self):
        with open('file', "w") as f:
            num = str(self.fileNum + 1)
            f.write(num)

    def postTweet(self):
        movieName = self.sessionKeys['movieName'] 
        totalFrames = self.sessionKeys['totalFrames']

        self.fileNum = self.getFileNum()
        num = self.fileNum

        path = os.path.abspath(os.getcwd())

        fileName = path + "/images/frame (" + str(num) + ").jpg"
        print(fileName)
        if num >= int(self.sessionKeys['totalFrames']):
            return schedule.cancel_job
        try:
            id = self.api.simple_upload(fileName)
            m_id = [id.media_id]
            tw_text = "Frame " + str(num) + " of " + str(totalFrames) + " frames from " + movieName + ".!"
            #api.update_status("Hello Tweepy", media_ids=m_id)
            #api.update_status_with_media("Hello Tweepy", "/home/surya/twitter_bot/photo-1516117172878-fd2c41f4a759")
            self.client.create_tweet(text=tw_text, media_ids=m_id)
            print(tw_text)
            print("Tweeted.!")
            self.updateFile()

        except Exception as e:
            print(f"Failed to post tweet: {e}")

    def getTotalFrames(self):
        return int(self.sessionKeys['totalFrames'])

    def initNum(self):
        self.fileNum = self.getFileNum()
    


if __name__ == '__main__':

    tw = Tweeter()
    tw.getKeys()
    tw.initAuth()
    tw.initNum()
    tw.postTweet()
    tw.updateFile()
    schedule.every(30).minutes.do(tw.postTweet)
    #schedule.every(5).seconds.do(tw.postTweet)

    while True:
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        if not schedule.jobs:
            break
        time.sleep(1)
    
    print("Done with tweeting.!")


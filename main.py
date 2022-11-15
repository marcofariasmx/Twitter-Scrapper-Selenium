import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SeleniumClient(object):
    def __init__(self):
        #Initialization method. 
        self.chrome_options = webdriver.ChromeOptions()
        #self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('window-size=1920,1080')
        #self.chrome_options.add_argument('--no-sandbox')
        #self.chrome_options.add_argument('--disable-setuid-sandbox')

        # you need to provide the path of chromdriver in your system
        self.browser = webdriver.Chrome("D:/OneDrive/PythonPrograms/Twitter-Scrapper-Selenium/chromedriver.exe", options=self.chrome_options) #version 107

        #self.base_url = 'https://twitter.com/search?q='
        self.base_url = 'https://twitter.com/'

    def get_tweets(self, query):
        ''' 
        Function to fetch tweets. 
        '''

        try:
            self.browser.get(self.base_url+query)
            time.sleep(2)

            body = self.browser.find_element(By.TAG_NAME, 'body')

            tweet_contents = []

            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)

                timeline = self.browser.find_element(By.CSS_SELECTOR, "[aria-label='Timeline: Search timeline']")
                tweet_nodes = timeline.find_elements(By.CSS_SELECTOR, "[data-testid='tweetText'")

                for tweet in tweet_nodes:
                    tweet_contents += [tweet.text]

                #print(pd.DataFrame({'tweets': [tweet_node.text for tweet_node in tweet_nodes]}))

            tweet_contents = sorted(set(tweet_contents), key=tweet_contents.index) # To remove duplicates, whilst preserving the order of tweets
            
            return tweet_contents

        except:
            print("Selenium - An error occured while fetching tweets.")


    def get_tweets_specifics(self, query):
        ''' 
        Function to fetch tweets. 
        '''

        UserTags=[]
        TimeStamps=[]
        Tweets=[]
        Replys=[]
        reTweets=[]
        Likes=[]

        #try:
        self.browser.get(self.base_url+query)
        time.sleep(2)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        #timeline = self.browser.find_element(By.CSS_SELECTOR, "[aria-label='Timeline: Search timeline']")
        #aria-labelledby="accessible-list-1
        timeline = self.browser.find_element(By.CSS_SELECTOR, "[aria-labelledby='accessible-list-1']")
        tweet_contents = []

        UserTags=[]
        TimeStamps=[]
        Tweets=[]
        Replys=[]
        reTweets=[]
        Likes=[]

        articles = timeline.find_elements(By.XPATH,"//article[@data-testid='tweet']")
        while True:
            for article in articles:
                UserTag = timeline.find_element(By.XPATH,".//div[@data-testid='User-Names']").text
                UserTags.append(UserTag)
                
                TimeStamp = timeline.find_element(By.XPATH,".//time").get_attribute('datetime')
                TimeStamps.append(TimeStamp)
                
                Tweet = timeline.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
                Tweets.append(Tweet)
                
                Reply = timeline.find_element(By.XPATH,".//div[@data-testid='reply']").text
                Replys.append(Reply)
                
                reTweet = timeline.find_element(By.XPATH,".//div[@data-testid='retweet']").text
                reTweets.append(reTweet)
                
                Like = timeline.find_element(By.XPATH,".//div[@data-testid='like']").text
                Likes.append(Like)
            #timeline.execute_script('window.scrollTo(0,document.body.scrollHeight);')
            body.send_keys(Keys.PAGE_DOWN)
            #time.sleep(.5)
            Tweets2 = list(set(Tweets))
            if len(Tweets2) >= 3:
                break
            time.sleep(.5)


        print(len(UserTags),
        len(TimeStamps),
        len(Tweets),
        len(Replys),
        len(reTweets),
        len(Likes))

        userTags_clean=[]
        timeStamps_clean=[]
        tweets_clean=[]
        replys_clean=[]
        reTweets_clean=[]
        likes_clean=[]

        for i in range(len(Tweets)):
            if Tweets[i] not in tweets_clean:
                reTweets_clean.append(reTweets[i])
                userTags_clean.append(UserTags[i])
                timeStamps_clean.append(TimeStamps[i])
                tweets_clean.append(Tweets[i])
                replys_clean.append(Replys[i])
                likes_clean.append(Likes[i])


        print(len(userTags_clean),
        len(timeStamps_clean),
        len(tweets_clean),
        len(replys_clean),
        len(reTweets_clean),
        len(likes_clean))

        import pandas as pd

        df = pd.DataFrame(zip(UserTags,TimeStamps,Tweets,Replys,reTweets,Likes)
                        ,columns=['UserTags','TimeStamps','Tweets','Replys','reTweets','Likes'])

        df.head()

        df_clean = pd.DataFrame(zip(userTags_clean,tweets_clean,timeStamps_clean,replys_clean,reTweets_clean,likes_clean)
                        ,columns=['UserTags','Tweets','TimeStamps','Replys','reTweets','Likes'])


        df_clean.head()

        return df_clean

#        except:
#            print("Selenium - An error occured while fetching tweets.")

selenium_client = SeleniumClient()

# tweets_df = selenium_client.get_tweets('AI and Deep learning')

# for i in range(len(tweets_df)):
#     print(i+1, ') ', tweets_df[i])

# print('Number of tweets mined:', len(tweets_df))

#tweets_detailed_df = selenium_client.get_tweets_specifics('AI and Deep learning')

tweets_detailed_df = selenium_client.get_tweets_specifics('elonmusk')

print(tweets_detailed_df)
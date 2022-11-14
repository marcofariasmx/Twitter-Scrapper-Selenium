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
        #self.chrome_options.add_argument('--no-sandbox')
        #self.chrome_options.add_argument('--disable-setuid-sandbox')

        # you need to provide the path of chromdriver in your system
        self.browser = webdriver.Chrome("D:/OneDrive/PythonPrograms/Twitter-Scrapper-Selenium/chromedriver.exe", options=self.chrome_options)

        self.base_url = 'https://twitter.com/search?q='

    def get_tweets(self, query):
        ''' 
        Function to fetch tweets. 
        '''

        # try: 
        self.browser.get(self.base_url+query)
        time.sleep(2)

        #body = self.browser.find_element_by_tag_name('body')
        body = self.browser.find_element(By.TAG_NAME, 'body')

        tweet_contents = []

        for _ in range(10):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

            #timeline = self.browser.find_element_by_id('timeline')
            #timeline = self.browser.find_element(By.ID, 'timeline')
            "[aria-label=XXXX]"
            timeline = self.browser.find_element(By.CSS_SELECTOR, "[aria-label='Timeline: Search timeline']")
            #tweet_nodes = timeline.find_elements_by_css_selector('.tweet-text')
            #tweet_nodes = timeline.find_element(By.CSS_SELECTOR, '.tweetText')
            tweet_nodes = timeline.find_elements(By.CSS_SELECTOR, "[data-testid='tweetText'")
            #data-testid='tweetText'

            #print(timeline)

            print("tweet_nodes:")
            #print(tweet_nodes)
            
            for tweet in tweet_nodes:
               tweet_contents += [tweet.text]
               #tweet_contents.append([tweet.text])

            #print(pd.DataFrame({'tweets': [tweet_node.text for tweet_node in tweet_nodes]}))

        tweet_contents = sorted(set(tweet_contents), key=tweet_contents.index) # To remove duplicates, whilst preserving the order of tweets 
        
        for i in range(len(tweet_contents)):

            print(i+1, ') ', tweet_contents[i])
        
        #print(tweet_contents)
        #print(type(tweet_contents))
        print('len of list:', len(tweet_contents))
        return 'all finished'

        # except: 
        #     print("Selenium - An error occured while fetching tweets.")

selenium_client = SeleniumClient()

tweets_df = selenium_client.get_tweets('AI and Deep learning')

print(tweets_df)
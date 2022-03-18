import requests
from bs4 import BeautifulSoup
from .models import NbaNews
from telegram.bot import Bot
import re
from datetime import datetime



news_bot = Bot('5193285730:AAFiLtKTIiRqwGpupDk5FqdYblu39EPck20') 


def collectNews():
   news_response = requests.get('https://nba.udn.com/nba/cate/6754')
   soup = BeautifulSoup(news_response.content, 'lxml')
   all_news = soup.find('div', id='news_list_body').find_all('dt')


   for news in all_news:
      #titles
      title = news.find('h3').text      

      #newsurl
      news_url = f"https://nba.udn.com/{news.find('a').get('href')}"
      
      #imgurl
      img_src = news.find('img').get('data-src')
      img_src_split = img_src.split('&')  #get the original picture url
            
      #creator and create time   
      sub_news_response = requests.get(news_url)
      sub_soup = BeautifulSoup(sub_news_response.content, 'lxml')

      creator_info = sub_soup.find('div', class_='shareBar__info--author')
      post_time = creator_info.find('span').text  
      creator = creator_info.text.replace(post_time, '') 
      

      post_time_regex = re.compile(r'\d+')
      post_time = post_time_regex.findall(post_time)
      dateString = ','.join(post_time)
      dateFormatter = "%Y,%m,%d,%H,%M"
      post_time = datetime.strptime(dateString, dateFormatter)
  

      
      if not NbaNews.objects.filter(url=news_url):
         NbaNews.objects.create(url=news_url, title=title, imgsrc=img_src_split[0], creator=creator, post_time=post_time)
         news_bot.send_message('-648400651', f'{title}\n{news_url}')
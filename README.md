# TripAdvisor_Crawler
Using scrapy to scrape tripadvisor in order to get users' reviews and retaurant information.
for crawling restaurant information, it need to use selenium to select some button. in this project, we install driver for Edge (Version 85.0.564.68), If you want to use this dirver, please check your edge version.
it use python 2.

# Usage
because this project cannot crawler restaurant and user's review at once, we have to run this project 2 times, one for crawling retaurant information, one for user's review.

In file tripadvisorspider.py, line 30.

  If we want to crawler restaurant information, we will call the function parse_page in callback.
  
  If we want to crawler user's review, we will call the function parse_review in callback.
  
In the project's root folder type:

scrapy crawl tripadvisor

the reviews will be stored in a csv file

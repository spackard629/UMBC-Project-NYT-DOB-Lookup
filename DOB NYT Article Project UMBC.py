import requests
import csv
import pandas as pd

#Base URL for API
base_url = "https://api.nytimes.com/svc/archive/v1"
myapikey = "c4MXNVjLtJyqvT7VCvagW5RDW8DO5ejg"

#User Input birth month and year
year = input("Enter your 4-digit birth year: ")
month = input("Enter a digit indicating the month of the year that you were born (1-12): ")
day = input("Enter a digit indicating the day of the month you were born (1-31): ")

# Construct the URL
month_url = month + ".json"
url_parts = (base_url,year,month_url)
url = "/".join(url_parts)

# Setup the querystring
queryString = {"api-key" : myapikey}

# Call request and convert the JSON data to a Python dict
nytData = requests.get(url, params = queryString)

# Get the response data
pythonData = nytData.json()

#Print Copyright
print()
print(pythonData['copyright'])

# Print out the "hits" key to show the number of articles that were returned
response_dict = pythonData['response']

# by the NY Times Archive API
print()
print(f"There are {response_dict['meta']['hits']} NYT articles in month {month} of the year {year}.")

# Grab all the articles from the response_dict.
articles = response_dict['docs']

##Display number of articles on specific date
#create empty varaibles
dobArticles = []

#transform month and day to two digit varaible if not already 
if(len(month) < 2):
  month = "0" + month

if(len(day) < 2):
  day = "0" + day

#date of birth variable 
dob = year + "-" + month + "-" + day

# #loop through articles in birth month from NYT API
for article in articles:
  dayOfMonth = article["pub_date"].split('T')
  # print(dayOfMonth[0])
  if(dayOfMonth[0] == dob):
    dobArticles.append(article)

#print number of articles published on day of birth
print()
print(f'There were {len(dobArticles)} NYT articles published on your date of birth.')

##turn dobArticles into pandas 
dobarticles_df = pd.DataFrame(dobArticles)

#data set for front page headlines on dob
frontpage_df = dobarticles_df[dobarticles_df["print_page"] == "1"]

#creat list of front page headlines
headlines = frontpage_df["headline"]

headlinesList = headlines.to_list()

#print front page headlines from dob 
print()
print(f"There were {len(frontpage_df)} frontpage stories on your birthday: ")

#display all front page stories with url
urlList = []
i = 0
for d in frontpage_df.headline:
  mainheadline = d['main']
  print()
  print(mainheadline)
  print(frontpage_df.iloc[i].web_url)
  print()
  i += 1
  

import requests
import re

for i in range(1,1000):
    search = requests.get('http://www.taste.com.au/search-recipes/?q=++&sort=rating&order=desc&page={}'.format(i)).text
    for r in set(re.findall('http://www.taste.com.au/recipes/\d+/([\w\+]+)', search)):
        print (r)

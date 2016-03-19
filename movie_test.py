import requests
from bs4 import BeautifulSoup

def scrape_and_rate():
    page = 1
    movie_titles = []
    while page <= 1:
        url = 'http://www.amazon.com/s/ref=sr_pg_' + str(page) + '?fst=as%3Aoff&rh=n%3A2858778011%2Cn%3A2858905011%2Cp_85%3A2470955011%2Cp_n_theme_browse-bin%3A2650368011&page=' + str(page) + '&bbn=2858905011&ie=UTF8&qid=1458396963'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('h2', {'class': 'a-size-medium a-color-null s-inline  s-access-title a-text-normal'}):
            title = link.string
            #print (title)
            title = title.lower()
            title = title.replace (" ", "_")
            title = title.replace ("'", "")
            movie_titles.append(title)
        page += 1
    movie_titles
        
def scrape_and_rate_test():
    page = 1
    movie_titles = []
    while page <= 10:
        url = 'http://www.amazon.com/s/ref=sr_pg_' + str(page) + '?fst=as%3Aoff&rh=n%3A2858778011%2Cn%3A2858905011%2Cp_85%3A2470955011%2Cp_n_theme_browse-bin%3A2650368011&page=' + str(page) + '&bbn=2858905011&ie=UTF8&qid=1458396963'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('h2', {'class': 'a-size-medium a-color-null s-inline  s-access-title a-text-normal'}):
            title = link.string
            #print (title)
            title = title.lower()
            title = title.replace (" ", "_")
            title = title.replace ("'", "")
            movie_titles.append(title)
        page += 1
    movie_titles
    

    for title in movie_titles:
        try:
            url = 'http://www.rottentomatoes.com/m/' + title
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
            tom_rating = soup.find('span', {'class': 'meter-value superPageFontColor'}).span.string
            aud_rating = soup.find('div', {'class': 'meter-value'}).span.string
            int_tom = int(tom_rating)
            int_aud = int(aud_rating.replace ("%", ""))
            over_70 = []
            if (int_tom + int_aud)/2 > 70:
                over_70.append(title)
                #print 'THIS MOVIE HAS A COMPOSITE SCORE OF OVER 70'
                print 'the critic rating on ' + title + ' is ' + tom_rating + '%'
                print 'the audience rating on ' + title + ' is ' + aud_rating
                print ''
        except AttributeError:
            #print 'Unable to find info on ' + title +' this is due to a spelling discrepency between RT and Amazon'
            pass

scrape_and_rate_test()







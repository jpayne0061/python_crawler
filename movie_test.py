import requests
from bs4 import BeautifulSoup

class movie_scraper(object):
    def __init__(self, url, bs_name, bs_attrs, pages_to_scrape):
        self.url = url
        self.bs_name = bs_name
        self.bs_attrs = bs_attrs
        self.pages_to_scrape = pages_to_scrape

    def scrape(self):
        movie_url = self.url
        bs_name = self.bs_name
        bs_attrs = self.bs_attrs
        pages_to_scrape = self.pages_to_scrape
        page = 1
        movie_titles = []
        print '{0}Starting to scrape{1}'.format(8*'*', 8*'*')
        while page <= pages_to_scrape:
            str_page = str(page)
            print 'Scraping page {0} of {1}'.format(str_page, pages_to_scrape)
            print 'Gathered {0} movie titles'.format(str(len(movie_titles)))
            url = movie_url.format(str_page, str_page)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            for link in soup.findAll(bs_name, bs_attrs):
                title = link.string
                rotten_tomatoes_title = title.lower().replace (" ", "_").replace ("'", "")
                movie_titles.append(rotten_tomatoes_title)
            page += 1
        return movie_titles

class amazon(movie_scraper):
    def __init__(self):
        self.url = 'http://www.amazon.com/s/ref=sr_pg_{}?fst=as%3Aoff&rh=n%3A2858778011%2Cn%3A2858905011%2Cp_85%3A2470955011%2Cp_n_theme_browse-bin%3A2650368011&page={}&bbn=2858905011&ie=UTF8&qid=1458396963'
        self.bs_name = 'h2'
        self.bs_attrs = {'class': 'a-size-medium a-color-null s-inline  s-access-title a-text-normal'}
        self.pages_to_scrape = 10


def rotten_tomatoes_rate(movie_titles_list, rating_cutoff=70):
        
    for title in movie_titles_list:
        try:
            url = 'http://www.rottentomatoes.com/m/{0}'.format(title)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            tom_rating = soup.find('span', {'class': 'meter-value superPageFontColor'}).span.string
            aud_rating = soup.find('div', {'class': 'meter-value'}).span.string
            int_tom = int(tom_rating)
            int_aud = int(aud_rating.replace ("%", ""))
            if (int_tom + int_aud)/2 > rating_cutoff:
                formatted_title = title.replace('_', ' ').title()
                print '{0}: Critic {1}%, Audience {2}'.format(formatted_title, tom_rating, aud_rating)
        except AttributeError:
            #print 'Missing Lookup in Rotten Tomatoes: {0}'.format(url)
            pass

def main():
    amazon_list = amazon().scrape()
    rotten_tomatoes_rate(amazon_list)

if __name__ == '__main__':
    main()






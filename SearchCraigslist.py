from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import csv
import sys
import os

# Craigslist search URL
BASE_URL = ('http://seattle.craigslist.org/search/'
            '?sort=rel&areaID=11&subAreaID=&query={0}&catAbb=sss')


def parse_results(search_term, price_limit):
    results = []
    search_term = search_term.strip().replace(' ', '+')
    search_url = BASE_URL.format(search_term)
    soup = BeautifulSoup(urlopen(search_url).read())
    rows = soup.find('div', 'content').find_all('p', 'row')
    for row in rows:
        url = 'http://seattle.craigslist.org' + row.a['href']
        # price = row.find('span', class_='price').get_text()
        create_date = row.find('time').get('datetime')
        title = row.find_all('a')[1].get_text()

        # Check if the price is within range
        cost_string = row.find_all('span')[1].get_text()
        start_price = cost_string.find('$')
        end_price = cost_string.find('(')
        cost = cost_string[start_price:end_price]

        try:
            if int(cost[1:len(cost)]) < int(price_limit):
                results.append({'url': url, 'create_date': create_date,
                                'title': title, 'price': cost})
        except:
            continue
    return results


def write_results(results):
    """Writes list of dictionaries to file."""
    fields = results[0].keys()
    with open('results.csv', 'w') as f:
        dw = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        dw.writer.writerow(list(dw.fieldnames))
        dw.writerows(results)


def has_new_records(results):
    current_posts = [x['url'] for x in results]
    fields = results[0].keys()
    if not os.path.exists('results.csv'):
        return True

    with open('results.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames=fields, delimiter='|')
        seen_posts = [row['url'] for row in reader]

    is_new = False
    for post in current_posts:
        if post in seen_posts:
            pass
        else:
            is_new = True
    return is_new


def get_current_time():
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    try:
        TERM = sys.argv[1]
        PRICELIMIT = sys.argv[2]
    except:
        print("You need to include a search term\n")
        sys.exit(1)

    results = parse_results(TERM, PRICELIMIT)

    # Report whether or not there are new results
    if has_new_records(results):
        message = ("Hey - there are new Craigslist \
        posts for: {0}".format(TERM.strip()))
        print("[{0}] There are new results")
        write_results(results)
    else:
        print("[{0}] No new results, try again later".format(get_current_time()))

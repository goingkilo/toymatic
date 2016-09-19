
import urllib2
import json

products = 'https://affiliate-api.flipkart.net/affiliate/api/goingkilo.json'
products = 'http://affiliate-api.flipkart.net/affiliate/api/goingkilo.json'
deals = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/dotd/json'
offers = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/top/json'
search_product = 'https://affiliate-api.flipkart.net/affiliate/product/json?id='
search = 'https://affiliate-api.flipkart.net/affiliate/search/json?query=searchTerm&resultCount=Count1'
orders_report = 'https://affiliate-api.flipkart.net/affiliate/report/orders/detail/json?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd&status=<status>&offset=0'

def get(url):
    print url
    req = urllib2.Request(url)
    req.add_header('Fk-Affiliate-Id', 'goingkilo')
    req.add_header('Fk-Affiliate-Token', '1368e5baaf8e4bcdb442873d4aa8ef6e')
    resp = urllib2.urlopen(req)
    content = resp.read()
    return content
    
def pp(x):
    print json.dumps(x,indent=4)

def search_for(product,count = 100):
    return get( search.replace('searchTerm', product).replace( 'Count1', str(count)))


#pp( search_for( 'laptop', 10) )

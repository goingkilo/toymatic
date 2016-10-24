
import urllib2
import json
import time
import traceback
import logging


products = 'https://affiliate-api.flipkart.net/affiliate/api/goingkilo.json'
search_product = 'https://affiliate-api.flipkart.net/affiliate/product/json?id='
deals  = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/dotd/json'
offers = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/top/json'
dotd   = 'https://affiliate-api.flipkart.net/affiliate/offers/v1/dotd/json'
search = 'https://affiliate-api.flipkart.net/affiliate/search/json?query=searchTerm&resultCount=Count1'
orders_report = 'https://affiliate-api.flipkart.net/affiliate/report/orders/detail/json?startDate=yyyy-MM-dd&endDate=yyyy-MM-dd&status=<status>&offset=0'


def get(url):
    #print url
    req = urllib2.Request(url)
    req.add_header('Fk-Affiliate-Id', 'goingkilo')
    req.add_header('Fk-Affiliate-Token', '1368e5baaf8e4bcdb442873d4aa8ef6e')
    resp = urllib2.urlopen(req)
    content = resp.read()
    return content
    
def pp(x):
    print json.dumps(json.loads(x),indent=4)

def save_local(a,b):
    f = open( './json/' + a, 'w')
    f.write(b)
    f.close()


def search_for(product,count = 100):
    return get( search.replace('searchTerm', product).replace( 'Count1', str(count)))

def parse_categories(x):
    a = json.loads(x)
    groups = a[ 'apiGroups']['affiliate']['apiListings']
    ret = []
    for i in groups.keys():
        get = groups[i]['availableVariants']["v1.1.0"]['get']
        top = groups[i]['availableVariants']["v1.1.0"]['top']
        ret.append( [i,get,top])
    return ret
         
# returns list of categories [name, get url, top url]
def categories(local=True):
    if local:
        a = open('json/categories.json','r').read()
        return json.loads(a)
    a =  get( 'https://affiliate-api.flipkart.net/affiliate/api/goingkilo.json')
    save_local( 'categories.json', a)
    return parse_categories(a)

# returns list of dotd
def get_dotd():
    a = get( dotd)
    b = json.loads(a)
    return b['dotdList']    


# given categories, return list of p products
def product( cats, p):
    product = [x for x in cats if x[0] == p][0]
    get_url  = product[1]
    return get(get_url)
    
def load():
    c0 = open( 'json/categories.json','r')

    cats = json.load( c0)

    def get_in(x):
        for i in cats:
            if x == i[0]:
                return i
        return None

    c1 = open( 'json/cats.todo','rw').read().split()
    c2 = []
    counter  = 0
    for i in c1:
        try:
            row = get_in(i)
            print 'now doing', row
            g = get( row[1])
            save_local( row[0] + '_.json', g)
            time.sleep(1)    
            t = get( row[2])
            save_local( row[0] + '_t.json', t)
            time.sleep(1)    

            print 'done ', i
            c1.remove(i)
            c2.append(i)
            counter += 1
            if counter >= 9:
                print 'sleeping 10'
                time.sleep(10)
        except Exception as e:
            logging.error(traceback.format_exc())
            print 'sumpin sumpin fail quit'
            break
    
    done = open( 'json/cats.done','w')
    for i in c2:
        done.write(i)
        done.write('\n')
    done.close()




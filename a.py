from  yahoo_finance import Share
import datetime
import json
from datetime import timedelta
today = str(datetime.date.today())
seven_days_ago = str( datetime.date.today() - timedelta( days=7))
boa = Share('BAC')
data = boa.get_historical( seven_days_ago, today)
print data
f = open('stocks.json','w')
json.dump( data, f)
f.close()

import urllib2
import urllib

#from urllib import urlencode
#import urllib.urlencode


# connect using the unofficial airbnb api: http://airbnbapi.org/

searchLocation = urllib.pathname2url("Geneva, Switzerland")
numGuests = str(4)
resultsFile = open('workfile.txt', 'w')
results = []

for i in range(1):
	url = "https://api.airbnb.com/v2/search_results?"
	url += "client_id=3092nxybyb0otqw18e8nh5nty"
	# url += "&locale=en-US&currency=USD"
	url += "&_format=for_search_results_with_minimal_pricing"
	url += "&_limit=50"
	url += "&_offset=" + str(50 * i)
	url += "&fetch_facets=false"
	# url += "&guests=" + numGuests
	url += "&ib=false&ib_add_photo_flow=true"
	url += "&location=" + searchLocation
	# url += "&location=Lake%20Tahoe%2C%20CA%2C%20US"
	url += "&min_bathrooms=1&min_bedrooms=0&min_beds=1"
	url += "&min_num_pic_urls=10"
	url += "&price_max=210&price_min=40"
	# url += "&sort=1"
	# url += "&user_lat=37.3398634&user_lng=-122.0455164"

	req = urllib2.Request(url, headers={'User-Agent' : 'Magic Browser'})
	print i
	print url
	try:
		f = urllib2.urlopen(req)
		results.append(f.read())
		resultsFile.write(f.read())
	except:
		results.append("failure")
		resultsFile.write("failure")
print "DONE"
resultsFile.write("DONE")


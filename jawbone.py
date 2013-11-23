import urllib
import urllib2
import json
import pprint
import time
import commands
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
import datetime
from pytz import timezone
import pytz

username='myusername@emailserver.com'  # Add your username here
passwd='mypassword'                 # Add your password here
gval = []
tval = []
url = 'https://jawbone.com/user/signin/login'


params = urllib.urlencode({
  'email': username,
  'pwd': passwd,
  'service': 'nudge'
})
tokenresponse = urllib2.urlopen(url, params)
data = json.load(tokenresponse)   
token_num = data["token"]

bayarea = pytz.timezone('US/Pacific')             # Change your timezone if you need to
url = 'https://jawbone.com/nudge/api/v.1.33/users/@me/social?data=20131117&limit=20'
opener = urllib2.build_opener()
opener.addheaders.append(('x-nudge-token', token_num))
dataresponse = opener.open(url)
data = json.load(dataresponse)
for x in range(0, len(data["data"]["feed"])):
    if (data["data"]["feed"][x]["comments"]["items"]): 
        value = data["data"]["feed"][x]["comments"]["items"][0]["time_created"]
        tval = np.append(tval,datetime.datetime.fromtimestamp(value,bayarea))
        gval = np.append(gval, data["data"]["feed"][x]["comments"]["items"][0]["comment"].replace("\"",""))

# convert epoch to matplotlib float format
fds = dates.date2num(tval) # converted

# matplotlib date format object
hfmt = dates.DateFormatter('%Y-%m-%d')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(fds, gval,'ro' )
ax.xaxis.set_major_locator(dates.DayLocator())
ax.xaxis.set_major_formatter(hfmt)
ax.set_ylim( 80,180)
plt.xticks(rotation='vertical')
#plt.subplots_adjust(bottom=.3, right=0.8, top=0.9)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                    wspace=None, hspace=None)
for i,j in zip(fds,gval):
    ax.annotate(str(j),(i,j))
#Show the graph
plt.show()

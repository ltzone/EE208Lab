# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import sys
import os
import Queue
import threading
from threading import Thread
import time
import urllib
import urlparse
import json
import math
import numpy as np
import requests
import random
sku=str(11346312290)
shop="0000000000"
#url="https://review.suning.com/ajax/cluster_review_lists/general-30193816-000000011346312290-0000000000-total-1-default-10-----reviewList.htm?callback=reviewList"
url=r"https://review.suning.com/ajax/" \
        r"getClusterReview_labels/cluster-30193816-0000000" \
        r"{}-{}" \
        r"-----commodityrLabels.htm?".format(sku,shop)
headers = {'User-Agent':'Mozilla/5.0 '
                        '(Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML,'
                        ' like Gecko) Chrome/76.0.3809.132 '
                        'Safari/537.36'}
content = urllib2.urlopen(url).read()
print url
print content

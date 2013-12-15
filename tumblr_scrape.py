#!/usr/bin/python

import requests
import os.path
import re
import shutil
import sys
import random
import time

url_regex = re.compile('http://\d+\.media\.tumblr\.com\/.+?\.(?:jpg|png|gif)')
size_regex = re.compile(r'_(\d+)\.')

if len(sys.argv) == 1:
	print('Usage: python tumblr_scrape.py <username> [max_pages]')
	exit(2)
elif len(sys.argv) > 1:
	username = sys.argv[1]
	if len(sys.argv) == 3:
		max_pages = int(sys.argv[2])
		no_limit = False
	else:
		max_pages = True
		no_limit = True # No set limit. Won't need to -= later on since it's a boolean.

	count = 1
	if not os.path.exists('images/' + username):
		    os.makedirs('images/' + username)

	previous = open('images/' + username + '/previous.txt', "a+")
	already_checked = previous.readlines()

	ctr = 0
	while ctr < len(already_checked):
		already_checked[ctr] = already_checked[ctr].strip()
		ctr += 1
	
	while max_pages:
		print '\n[+] Scraping page ' + str(count) + ' of ' + username
		req = requests.get('http://' + username + '.tumblr.com/page/' + str(count))
		
		page = req.text
		matches = re.findall(url_regex, page)
		
		only_avatars = True # pages past the end of the blog tend to only have avatars

		for match in matches:
			if 'avatar' not in match:
				only_avatars = False
				break
		
		if only_avatars:
			print matches
			print 'Complete'
			previous.close()
			exit(0)
		
		images_already_fetched = 0

		for match in matches:
			if match in already_checked or 'avatar' in match:
				images_already_fetched += 1
				if images_already_fetched == len(matches):
					print 'Images already exist. Complete.'
					previous.close()
					exit(0)
			elif 'avatar' not in match:
				final_url = match # the url actually downloaded
				img_name = match.rsplit('/', 1)[1]

				try:
					size = re.findall(size_regex, img_name)[0]
				except:
					size = 'fail'

				#print '[i i] Found ' + img_name

				if size == 'fail':
					continue
				img = requests.get(match, stream=True)

				if size != '1280':
					try_url = match.replace(size, '1280')
					#print '[i i]Size is ' + size + '. Trying ' + try_url
					try_get = requests.get(try_url, stream=True)

					if try_get.status_code == 200:
						#print '[! !] ' + str(try_get.status_code) + ' ' + try_url + ' exists'
						img_name = try_url.rsplit('/', 1)[1]
						img = try_get
						final_url = try_url

				print '[+ +] Downloading ' + img_name + '\n\t| ' + final_url
				out_file = open('images/' + username + '/' + img_name, 'wb')
				shutil.copyfileobj(img.raw, out_file)
				print >>previous, match
	
				#time.sleep(random.random())

		count += 1
		if not no_limit:
			max_pages -= 1

	previous.close()

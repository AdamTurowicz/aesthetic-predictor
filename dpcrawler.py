#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    A simple script to download the images specified in the AVA dataset from dpchallenge.
    This script is assumed to be placed in AVA_ROOT which contains a folder named 'images'.
'''


import os
from urllib import request
import numpy as np
from bs4 import BeautifulSoup
from clint.textui import progress, puts, colored

 
def savePhotoByUrl(url, imageID):
	fname = str(imageID) + '.jpg'
	print("Downloading " + url + '...')
	
	try:
		handle = request.urlopen(url, timeout=5)
		with open(fname, "wb") as f:
			while True:
				chunk = handle.read(1024)
				if not chunk: break
				f.write(chunk)
		# puts(colored.green("Finished downloading " + fname))
		return fname
	except Exception as e:
		print('ERROR: {}'.format(e))

def getPhotoURLByID(imageID):
	BASE_URL = 'http://www.dpchallenge.com/image.php?IMAGE_ID='

	data = None
	try:
		data = request.urlopen(BASE_URL + str(imageID), timeout=5).read()
	except Exception as e:
		print('ERROR: {}'.format(e))
	else:
		soup = BeautifulSoup(data, 'html.parser')
		title = soup.title.string.split('by')[0][:-1]
		
		results = soup.find(id='img_container').findAll('img')
		for result in results:
			#if (result.has_attr('alt') and result['alt'] == title):
			if (result.has_attr('alt')):
				# print result['src']
				return "http:"+result['src']

def getPhotoIDs():
	ava = np.loadtxt('AVA.txt', dtype=int)
	return ava[:,1]

def main():
	
	# load image IDs
	puts(colored.yellow("Loading image IDs..."))
	IDs = getPhotoIDs()
	puts("Done")
	
	for ID in IDs:
		if os.path.isfile('images/' + str(ID) + '.jpg'):
			puts(colored.red("Already downloaded " + str(ID) + '.jpg ... skip'))
			continue
		
		url = getPhotoURLByID(ID)
		if (url != None):
			savePhotoByUrl(url, ID)


if __name__ == "__main__":
	main()
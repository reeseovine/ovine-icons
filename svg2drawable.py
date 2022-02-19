#!/usr/bin/env python3

from bs4 import BeautifulSoup

###### INCOMPLETE!! ######

def svg2drawable(svg: str) -> str:
	soup = BeautifulSoup(svg, 'lxml')

	soup.svg.name = 'vector'
	soup.vector['xmlns:android'] = "http://schemas.android.com/apk/res/android"
	soup.vector['android:width'] = "108dp"
	soup.vector['android:height'] = "108dp"
	soup.vector['android:viewportWidth'] = "108"
	soup.vector['android:viewportHeight'] = "108"

	soup.vector.metadata.decompose()

	for tag in soup.vector.find_all('g'):
		tag.name = 'group'

	print(soup.prettify())





	return ''

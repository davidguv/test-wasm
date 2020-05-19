#!/usr/bin/python3

"""This script recursively scans all wasm in a directory and runs one 
chrome session per wasm to store the console.log in a ouput file 
"""

import os
import time
import argparse
import http.server
import socketserver
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Web Server
#############
def webServer():
	PORT = 8088
	print ("Starting Http server:" + str(PORT))
	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	httpd.serve_forever()
	
def testHtml(htmlFile):

	try:
		d = DesiredCapabilities.CHROME
		d['goog:loggingPrefs'] = { 'browser':'ALL' }

		chrome_options = Options()
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--no-gpu')
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-dev-shm-usage')

		driver = webdriver.Chrome(options=chrome_options,desired_capabilities=d)  

		driver.get('http://localhost:8088/'+ htmlFile);

		# TODO: Use waits https://www.selenium.dev/documentation/es/webdriver/waits/
		time.sleep(10)

		# Output console log messages
		outputFile = open(args.output, 'a')

		for entry in driver.get_log('browser'):
			mensaje = entry["message"]
			mensajeSimple = mensaje.split("\"")
			try:
				print (mensajeSimple[1])
				outputFile.write(mensajeSimple[1] + os.linesep)
			except Exception as e:
				print (e)
		outputFile.close()
		driver.quit()
		
	except Exception as e:
		print (e)
	
# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument( '-output', help='Output file', default="./test.log" )
parser.add_argument( '-dir', help='Directory to find the files', default="./" )
args=parser.parse_args()

print ("Output file: ", args.output)
print ("Directory to scan files: ", args.dir)

server = multiprocessing.Process(target=webServer)
server.start()

# Search the wasm files
########################
for path, directories, files in os.walk(args.dir):
	for file in files:
		nameWithoutExtension,Extension=os.path.splitext(file)
		if (Extension == ".wasm"):
			htmlFile = path + "/" + nameWithoutExtension + ".html"
			print ("Testing: " + htmlFile)
			testHtml(htmlFile)

server.terminate()

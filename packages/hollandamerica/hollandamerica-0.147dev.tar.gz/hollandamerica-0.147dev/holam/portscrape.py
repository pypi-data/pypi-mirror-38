from bs4 import BeautifulSoup, Tag
import csv
import urllib.request
from urllib.request import urlopen
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from langdetect import detect
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


##IN PROGRESS##
class portScrape(object):
	def __init__(self, lang, region, mailto):
		self.lang = lang
		self.region = region
		self.details = {}
		self.mailto = mailto
		self.mailfrom = "skateordie72@gmail.com"
		
	
	def visit(self):
		#capabilities = webdriver.DesiredCapabilities().FIREFOX
		#capabilities["marionette"] = True
		#capabilities["acceptInsecureCerts"] = True
		#binary = FirefoxBinary(r'C:\Users\lsc8524\AppData\Local\Mozilla Firefox\firefox.exe')
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--window-size=1920,1080")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable_dev_shm_usage")
		driver = webdriver.Chrome(chrome_options=chrome_options)
		details = {}

		driver.get("https://www.hollandamerica.com")
		dropdown = driver.find_element_by_class_name('dropdown-label')
		dropdown.click()
		items = driver.find_elements_by_class_name('dropdown-item')
		if "de" in self.lang:
			for item in items:
				if 'German' in item.text:
					item.click()
					break
		elif "es" in self.lang:
			for item in items:
				if 'Spanish' in item.text:
					item.click()
					break
		elif "nl" in self.lang:
			for item in items:
				if 'Dutch' in item.text:
					item.click()
					break
		
		url = "https://www.hollandamerica.com/"+self.lang+"/cruise-destinations/"+self.region+".ports.html#sort=name%20asc&start=0&rows=12?"
		driver.get(url)
		page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
		pages = int(driver.find_element_by_class_name("total-pages").get_attribute("innerText"))
		
		print(pages)
		next = driver.find_elements_by_class_name("next")
		driver.execute_script("window.scrollTo(0, 400);")
		x = True
		while x == True:
			time.sleep(2)
			page = int(driver.find_element_by_class_name("current-page").get_attribute("innerText"))
			pages = int(driver.find_element_by_class_name("total-pages").get_attribute("innerText"))
		
			links = driver.find_elements_by_class_name("card-container")
			for link in links:
				url = link.get_attribute("href")
				if url + "#" in list(details.keys()):
					url = url + "##"
				elif url in list(details.keys()):
					url = url + "#"
				details[url] = {}
				if "#" in url:
					if "de" in self.lang:
						print(link.get_attribute("aria-label"))
						bytes = link.get_attribute("aria-label").encode('ascii','replace')
						print(str(bytes) + "2")
						details[url]["title"] = str(bytes) + " (d)"
						print(details[url]["title"] + " !")
					else:
						details[url]["title"] = link.get_attribute("title") + " (d)"
				else:	
					if "de" in self.lang:
						print(link.get_attribute("aria-label"))
						bytes = link.get_attribute("aria-label").encode('ascii','replace')
						print(str(bytes) + "2")
						details[url]["title"] = str(bytes)
						print(details[url]["title"] + " !")
					else:
						details[url]["title"] = link.get_attribute("title")
					
			print(page)	
			if page < pages:
				next[0].click()
				
			else:
				x = False
				with open(self.region+"_en_ports.txt", "w") as f:
						f.write(str(details))
				break
					
		
		for url in details:
			print(url)
			driver.get(url + "?")
			places = list(details.keys())
			
			header = driver.find_elements_by_class_name("header")
			if len(header) != 0:
				title = header[0].find_elements_by_class_name("title")
				if str(title) in details[url]["title"]:
					pass
				else:
					if "de" not in self.lang:
						details[url]["title"] = title[0].text
			
			heroimg = driver.find_elements_by_class_name("image-lazy-loader")
			
			if len(heroimg) != 0:
				heroimg = driver.find_element_by_class_name("image-lazy-loader")
				src = str(heroimg.find_element_by_tag_name("img").get_attribute("src"))
				if src.startswith(".image"):
					details[url]["hero image"] = "n (broken)"
				else:
					details[url]["hero image"] = "y"
			else:
				details[url]["hero image"] = "n"
			
			cta = driver.find_elements_by_class_name("cta-noIcon")
			if len(cta) != 0:
				details[url]["cta"] = "y"
			else:
				details[url]["cta"] = "n"
			
			mapthing = driver.find_elements_by_class_name("port-map-image")
			if len(mapthing) != 0:
				details[url]["portmap"] = "y"
			else: 
				details[url]["portmap"] = "n"
				
			desc = driver.find_elements_by_class_name("desc")
			desc2 = driver.find_elements_by_class_name("desc  ")
			details[url]["translated"] = "n"
			if len(desc) != 0 or len(desc2) != 0:
				if len(desc[0].find_elements_by_tag_name("p")) != 0:
					details[url]["description"] = "y"
				else:
					details[url]["description"] = "n"
				details[url]["translated"] = "n"
				if len(desc) != 0 and details[url]["description"] == "y":
					if "en" not in self.lang and len(desc[0].find_elements_by_tag_name("p")) != 0:
						text = desc[0].find_element_by_tag_name("p").get_attribute("innerText")
						if len(text) > 10:
							tlang = detect(text)
							if tlang in self.lang:
								details[url]["translated"] = "y"
				elif len(desc2) != 0:
					if "en" not in self.lang and len(desc2[0].find_elements_by_tag_name("p")) != 0:
						text = desc2[0].find_element_by_tag_name("p").get_attribute("innerText")
						if len(text) > 10:
							tlang = detect(text)
							if tlang in self.lang:
								details[url]["translated"] = "y"
			else: 
				details[url]["description"] = "n"
				details[url]["translated"] = "n"
		
		if "en" in self.lang:
			if os.path.exists("en_US.txt"):
				os.remove("en_US.txt")
			with open("en_US.txt", "a") as enfile:
				enfile.write(str(details))
			with open(self.lang+"_"+self.region+"_ports.csv", "w", newline="") as csvfile:
				exwriter = csv.writer(csvfile)
				exwriter.writerow(["Hero Image present?", "Port map Present?", "Description present?", "Name", "Port Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["portmap"], details[key]["description"], details[key]["title"], str(key)])
		else:
			data = ""
			with open('en_US.txt', 'r') as newfile:
				data = newfile.read().replace('\n', '').replace("en_US", self.lang)
				print(data)
			for url in details:
				string = url
				print(string)
				if string in data:
					details[url]["inengsearch"] = "y"
				else:
					details[url]["inengsearch"] = "n"
				enstring = string.replace(self.lang, "en_US")
				details[url]["inen"] = "y"
				try:
					html = urlopen(enstring)
				except:
					details[url]["inen"] = "n"
				
				
		print(details)
		if os.path.exists(self.lang+"_"+self.region+"_ports.csv"):
			os.remove(self.lang+"_"+self.region+"_ports.csv")
		with open(self.lang+"_"+self.region+"_ports.csv", "w", newline = '') as csvfile:
			exwriter = csv.writer(csvfile)
			if self.lang == "en_US":
				exwriter.writerow(["Hero Image present?", "Port map present?", "Description present?", "CTA Present?", "Name", "Excursion Link"])
				for key in details:
					exwriter.writerow([details[key]["hero image"], details[key]["portmap"], details[key]["description"], details[key]["cta"], details[key]['title'], str(key)])
			else:
				exwriter.writerow(["Hero Image present?", "Port map present?", "Description present?", "CTA Present?", "in en search", "in en site", "translated", "name", "Excursion Link"])
				for key in details:
					if details[key]["title"]:
						exwriter.writerow([details[key]["hero image"], details[key]["portmap"], details[key]["description"], details[key]["cta"], details[key]["inengsearch"], details[key]["inen"], details[key]["translated"], details[key]["title"], str(key)])
					else:
						exwriter.writerow([details[key]["hero image"], details[key]["portmap"], details[key]["description"], details[key]["cta"], details[key]["inengsearch"], details[key]["inen"], details[key]["translated"], "????", str(key)])

		FILENAME = self.lang+"_"+self.region+"_ports.csv"
		SUBJECT = 'Finished copy of ' + FILENAME
		
		FILEPATH = './'+FILENAME
		MY_EMAIL = self.mailfrom
		MY_PASSWORD = "rodneymullen"
		TO_EMAIL = self.mailto
		SMTP_SERVER = 'smtp.gmail.com'
		SMTP_PORT = 587

		msg = MIMEMultipart()
		msg['From'] = MY_EMAIL
		msg['Subject'] = SUBJECT
		msg['To'] = COMMASPACE.join(TO_EMAIL)

		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(FILEPATH, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment', filename=FILENAME)
		msg.attach(part)

		smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login(MY_EMAIL, MY_PASSWORD)
		smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
		smtpObj.quit()

	
		
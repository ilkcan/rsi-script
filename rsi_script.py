from urllib import request
import smtplib
import sched, time
import argparse
import os
import smtplib
from bs4 import BeautifulSoup
gmailUser = ''
gmailPassword = ''
firstNFlag = False
currCount = 0
sumOfGains = 0
sumOfLosses = 0
avgGain = 0
avgLoss = 0
timePeriod = 1

def send_email(subject, body):
	global gmailPassword
	global gmailUser
	FROM = gmailUser
	TO = gmailUser
	SUBJECT = subject
	TEXT = body
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, TO, SUBJECT, TEXT)

	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmailUser, gmailPassword)
		server.sendmail(FROM, TO, message)
		server.quit()
	except:
		print("failed to send mail")

def checkValueOfCurrency(sc, currency, tick, prevVal): 
	global firstNFlag
	global currCount
	global sumOfLosses
	global sumOfGains
	global avgGain
	global avgLoss

	hdr = {	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'User-Agent' : "Magic Browser"}
	req = request.Request('https://tr.investing.com/currencies/' + currency, headers=hdr)
	resp = request.urlopen(req)
	html = resp.read()
	soup = BeautifulSoup(html, 'html.parser')
	currencySpan = soup.find(id="last_last")
	currencyVal = float(currencySpan.string.replace(",", "."))
	print(currencyVal)
	currGain = 0
	currLoss = 0
	if currCount != 0:
			change = currencyVal - prevVal
			if change <= 0:
				currLoss = abs(change)
				sumOfLosses += currLoss
			else:
				currGain = change
				sumOfGains += currGain

	if not firstNFlag:
		if currCount == timePeriod:
			firstNFlag = True 
			avgGain = sumOfGains / timePeriod
			avgLoss = sumOfLosses / timePeriod
			rs = avgGain / avgLoss
			rsi = 100 if rs == 0 else 100 - (100 / (1 + rs))
			print(rsi)
			send_email("RSI Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
			if rsi >= 80:
				send_email("Sell Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
			elif rsi <= 20:
				send_email("Buy Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
	else:
		avgGain = (avgGain * (timePeriod - 1) + currGain) / timePeriod
		avgLoss = (avgLoss * (timePeriod - 1) + currLoss) / timePeriod
		rs = avgGain / avgLoss
		rsi = 100 if rs == 0 else 100 - (100 / (1 + rs))
		print(rsi)
		send_email("RSI Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
		if rsi >= 80:
			send_email("Sell Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
		elif rsi <= 20:
			send_email("Buy Alert", currency + "/try has an rsi value of " + str(rsi) + " with the current value of " + str(currencyVal))
	currCount += 1
	sc.enter(tick, 1, checkValueOfCurrency, (sc, currency, tick, currencyVal))

def main(tp, currency, fetchFrequency, gUsername, gPassword):
	global timePeriod
	global gmailUser
	global gmailPassword
	s = sched.scheduler(time.time, time.sleep)
	timePeriod = tp
	gmailUser = gUsername
	gmailPassword = gPassword
	s.enter(0, 1, checkValueOfCurrency, (s, currency, fetchFrequency, 0))
	s.run()

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--tp", help="the time period for which rsi will be calculated (unit is --tick seconds)", required=True, type=float)
	parser.add_argument("--cur", help="the currency that you want to check the value of", required=True)
	parser.add_argument("--ff", help="the time period between each fetch (seconds)", required=True, type=int)
	parser.add_argument("--gu", help="gmail account for sending the mail", required=True)
	parser.add_argument("--gp", help="password for the gmail account", required=True)
	args = parser.parse_args()
	
	main(args.tp, args.cur, args.ff, args.gu, args.gp)
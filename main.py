from bs4 import BeautifulSoup
import os
import requests
import settings
import time

localPath = os.path.dirname( os.path.realpath( __file__ ) )
cmdLinePlaySoundCommand = "afplay -t " + settings.songTimeOutInSeconds
lastID = ""
#lastID = "38234" #Uncomment to play default song at startup

def playThemeSong(latestEntrant):
	songName = latestEntrant["id"] + "_" + str(latestEntrant["name"]).replace(" ", "_") + ".mp3"
	songPath = os.path.join(settings.soundEffectsDirectory, songName)
	time.sleep(settings.songDelayInSeconds)
	if (os.path.exists(songPath)):	#check for existence
		print "playing", songPath
		os.popen(cmdLinePlaySoundCommand + ' "' + songPath + '"')
	else: #play the backup sound
		defaultSongPath = os.path.join(settings.soundEffectsDirectory, settings.defaultSong)
		if (os.path.exists(defaultSongPath)):
			print "Playing default song: ", defaultSongPath
			os.popen(cmdLinePlaySoundCommand + ' "' + defaultSongPath + '"')

cookieTime = str(time.clock())

headers = {
    'cookie': "PHPSESSID=" + cookieTime,
    'origin': settings.url,
    'accept-encoding': "gzip, deflate",
    'accept-language': "en-US,en;q=0.8",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "*/*",
    'referer': settings.url,
    'x-requested-with': "XMLHttpRequest",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    }

while True:
	print "Loop Start", time.asctime()
	try:
		#Authorize/Login
		response = requests.request("POST", settings.url, data=settings.payload, headers=headers)

		#Get the most recent front door access list
		r = requests.request("GET", settings.url + '?c=access_report&m=select&action=search&page=1&eventcode=400', headers=headers)

		access_table = r.text
		soup = BeautifulSoup(access_table, 'html.parser')
		latest = soup.table.tbody.next_sibling.next_element.tr.find_all("td")
		latestEntrant = {"name":latest[3].string,"time":latest[1].string,"id":str(latest[4].string)}

		if len(lastID) < 1:
			lastID = latestEntrant['id']

		print "lastID ", lastID
		print "latestID", latestEntrant["id"]

		if (latestEntrant['id'] != lastID):
			lastID = latestEntrant['id']
			playThemeSong(latestEntrant)
		else:
			print "No new entrants"
	except Exception as e:
		print "Some kind of Error", e

	print 'Loop End', time.asctime()
	time.sleep(settings.sleepTimeInSeconds)
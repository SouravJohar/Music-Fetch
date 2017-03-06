from bs4 import BeautifulSoup
import dryscrape
import urllib
import os
from progressbar import ProgressBar, Percentage, Bar



def dlProgress(count, blockSize, totalSize):
    pbar.update( int(count * blockSize * 100 / totalSize) )


songInfo = {}
url = "http://mp3.direct/#!s="
url += raw_input(">")
connectionState = False
if "SongDownloads" not in os.listdir("."):
    os.system("mkdir SongDownloads")



try:
    session = dryscrape.Session()
    session.visit(url)
    connectionState = True
except:
    print "Connection error"
if connectionState:
    response = session.body()
    soup = BeautifulSoup(response, 'lxml')
    titles = soup.findAll("h3", {"class":"ui-li-heading"})
    songDetails = soup.findAll("p", {"class":"ui-li-desc"})
    index = 1
    url = soup.findAll("a", {"title" : "Listen & Download"})
    for i in range(min(len(titles), len(songDetails))):
        songInfo[index] = {"Name" : titles[i].text, "Details" : songDetails[i].text, "pageURL" : "mp3.direct" + url[i]["href"][1:]}
        index += 1
    track = 0
    for i in range(1,min(11, min(len(titles), len(songDetails)))):
        print "\n" + str(i) + ". " + songInfo[i]["Name"]
        print songInfo[i]["Details"]
        track += 1
    if track != 0:
        while True:
            choice = raw_input(">")
            if int(choice) in range(1,min(11, min(len(titles), len(songDetails)))):
                break
            else:
                print "song not found, enter another choice"

        downloadLink = songInfo[int(choice)]["pageURL"]
        fileSize = songInfo[i]["Details"].split(" MB")[0][::-1][:5][::-1]
        try:
            fileSize = float(str(fileSize))
        except:
            fileSize = float(str(songInfo[i]["Details"].split(" MB")[0][::-1][:4][::-1]))

        try:
            session = dryscrape.Session()
            session.visit("http://" + downloadLink)
            connectionState = True
        except:
            print "Connection error"
        if connectionState:
            response = session.body()
            soup = BeautifulSoup(response, "lxml")
            try:
                download = soup.findAll("a", {"id" : "download-btn"})[0]["href"]
                print "Downloading..."
                try:
                    pbar = ProgressBar(widgets=[Percentage(), Bar()])
                    urllib.urlretrieve(download, "./SongDownloads/{}.mp3".format(songInfo[int(choice)]["Name"]), reporthook=dlProgress)
                    if os.path.getsize("./SongDownloads/{}.mp3".format(songInfo[int(choice)]["Name"]))/(1024*1024.0) > fileSize - 2.5:
                        print 'Download Complete'
                    else:
                        print "The song wasnt downloaded correctly"
                except:
                    print "connection error"
            except:
                print "connection error1"

    else:
        print "Song not found"

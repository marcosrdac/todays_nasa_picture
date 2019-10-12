import urllib.request
import urllib.parse
import chardet


class Downloader():
    '''
    Basic Downloader class to download from a given URL.
    '''
    def __init__(self, url, textEncoding=None):
        self.url = url
        self.textEncoding = textEncoding
        self.contents = ''

    def requestData(self):
        req = urllib.request.Request(self.url)
        resp = urllib.request.urlopen(req)
        return(resp)

    def getAsBytes(self):
        resp = self.requestData()
        is_downloaded = (resp.getcode() == 200)
        if not is_downloaded:
            print('ERROR: Could not request the data!')
        else:
            respData = resp.read()
            self.contents = respData
            return(respData)

    def get(self):
        respData = self.getAsBytes()
        if self.textEncoding is None:
            self.textEncoding = chardet.detect(respData)['encoding']
        respData = respData.decode(self.textEncoding, 'ignore')
        self.contents = respData
        return(respData)


def download(url, textEncoding=None):
    downloader = Downloader(url, textEncoding)
    contents = downloader.get()
    return(contents)

url = 'https://apod.nasa.gov/apod/astropix.html'

page = download(url)
start = '<a href="image/'
startI = page.find(start)
link = page[startI+9:]
end = link.find('"')
link = link[:end]
link = 'https://apod.nasa.gov/apod/' + link
urllib.request.urlretrieve(link, 'todays_nasa_figure.png')

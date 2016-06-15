import os, requests
import threading
import urllib2
import time

URL = "http://www.nasa.gov/images/content/607800main_kepler1200_1600-1200.jpg"

#create a list of split ranges in bytes
def buildRange(value, numsplits):
    lst = []
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    print "Splitted list:",lst
    return lst


#main function
def main(url=None, splitBy=3):
    #log the time
    start_time = time.time()
    if not url:
        print "enter some url to begin download."
        return

    fileName = url.split('/')[-1]
    #need to get the length of the content if I don't get it will kill the process
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    print "%s bytes to download." % sizeInBytes
    if not sizeInBytes:
        print "Size cannot be determined."
        return

    #create a dictionary for the data
    dataDict = {}

    # split total num bytes into ranges
    ranges = buildRange(int(sizeInBytes), splitBy)

    # function to download the chunk and store it in dictionary
    def downloadChunk(idx, irange):
        req = urllib2.Request(url)
        req.headers['Range'] = 'bytes={}'.format(irange)
        dataDict[idx] = urllib2.urlopen(req).read()


    # obviously you could do it sequentially but have added a thread here just to demo the worst case with threads
    # create one downloading thread per chunk
    downloaders = [
        threading.Thread(
            target=downloadChunk, 
            args=(idx, irange),
        )
        for idx,irange in enumerate(ranges)
        ]

    # start threads, lets run in parallel, wait for all to finish
    for th in downloaders:
        th.start()
    for th in downloaders:
        th.join()

    print 'done: got {} chunks, total {} bytes'.format(
        len(dataDict), sum( (
            len(chunk) for chunk in dataDict.values()
        ) )
    )

    # just display the time stats
    print "--- %s seconds ---" % str(time.time() - start_time)

    #save the file
    if os.path.exists(fileName):
        os.remove(fileName)
    # reassemble file in correct order
    with open(fileName, 'w') as fh:
        for _idx,chunk in sorted(dataDict.iteritems()):
            fh.write(chunk)

    print "Finished Writing file %s" % fileName
    print 'file size {} bytes'.format(os.path.getsize(fileName))

if __name__ == '__main__':
    main(URL)

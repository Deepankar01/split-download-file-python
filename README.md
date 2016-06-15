# split-download-python
The code shows the way of how we can download a file by splitting the data into small chunks using python 

The basic trick or concept is that  we send a header request for the size of the file and then split the bits equally on
some criteria (i.e no of splits).

###How to get the length of the data that we are downloading###
so the header is `requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)`

so if will return the content length of the data in bytes now we can easily divide it into equal portions

###How to send how much we are going to download###
then we request the data using `req.headers['Range'] = 'bytes={}'.format(irange)` where `irange` is the split in the number of
the we would like to start from and end to 

###A word on optimization using threads###
once we start downloading the stuff we will get the data 
now to optimize this we could download the data using threads and put it in the dictionary and then can combine it to form the complete data
after all the data is just bits and bytes so we just need to join them together.


the sample data i have used for is an image from nasa here is it 
[logo]: http://www.nasa.gov/images/content/607800main_kepler1200_1600-1200.jpg "nasa image used as sample"
[logo]

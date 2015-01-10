sho.rt
======

A url-shortener backed by sqlite3 database.
This can serve as an API for any web-app providing url-shortening service.

For testing purpose, this software uses sqlite3 database. So, you can simply use this on your local machine to try out it's feautures.

##Get Started

```

from urlshortener import Url_Shortener

url_obj = Url_Shortener()

#encode the URL

encoded_url = url_obj.encode("docs.oracle.com/javase")   #say the short URL generated is "sho.rt/ab2"

#decode the URL

decoded_url = url_obj.decode("sho.rt/ab2")    #generates "docs.oracle.com/javase"


```




References:
[Stack Overflow](http://stackoverflow.com/questions/742013/how-to-code-a-url-shortener)

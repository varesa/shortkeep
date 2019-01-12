Shortkeep
=========

Shortkeep is a simple HTTP inteface to redis for publishing short-lived blobs of data.


Prerequisites
-------------
- Python3
- Working redis server


Usage
-----

```
# pip3 install -r requirements.txt
# python3 app.py
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
# curl -XPOST --data "Document content" http://localhost:5000/mykey/15m
OK
# curl -XGET http://localhost:5000/mykey
Document content
#
```

After 15 minutes:
```
# curl -XGET http://localhost:5000/mykey
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>

```

If you have redis running on some other address, you can use the `REDIS_HOST` environment variable.
The host defaults to `localhost`. 

Example use cases
-----------------

One application shortkeep can be used for is to utilize simple HTTP web monitoring tools
to make sure that a process has ran in some timeframe.

For example to monitor a CI/CD pipeline that should run hourly, one step could be to publish
an "OK" with an expiry of two hours. IF the pipeline is unable to execute the step for two hours,
the document will expire and monitoring tools can easily detect it.
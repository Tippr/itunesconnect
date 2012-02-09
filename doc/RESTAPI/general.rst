REST API Interface
==================


The iTunes REST API exposes the data pulled from iTunesConnect that contains the sales report of the applications published in the App Store. It allows to query the information for downloads and updates for a given publisher accepting several parameters such as app names or date ranges.

Base URL
========
All URLs referenced in the documentation has the following base::

http://96.126.123.172/stats/


Response Formats
================
iTunes API only supports returning resource representations as JSON. For example::

	GET /tippr/apps

response is::

	{
    	"appstats": [
        	{
            	"date": "20111122T00:00Z",
	            "developer": "PoweredByTippr",
    	        "downloads": 35,
        	    "publisher": "tippr",
            	"title": "Tippr",
	            "updates": 8,
    	        "version": "1.1.6"
        	},
	        {
    	        "date": "20111123T00:00Z",
        	    "developer": "PoweredByTippr",
            	"downloads": 435,
	            "publisher": "tippr",
    	        "title": "Tippr",
        	    "updates": 6,
            	"version": "1.1.6"
	        }
    	]
	}
	
Exceptions
==========
iTunes API returns exceptions in the HTTP header as HTTP Errors when something goes wrong.  

==================   =============================   ====================
URL Parameter        Reason                          HTTP Error
==================   =============================   ====================
publisher-name       Does not exists                 404 (Not Found)
app-id               Does not exists                 400 Bad Request
==================   =============================   ====================
	
Security
========
The iTunes API requires an API Key in order to work. The API Key should be sent as part of the HTTP header as a parameter named X-API-KEY. Exception might be raised according the following table:

=============================================  ==================
Scenario	                                   Response
=============================================  ==================
X-API-KEY not sent as HTTP header parameter	   400 Bad Request 
X-API-KEY is invalid/improper format           400 Bad Request 
X-API-KEY is unknown                           403 Forbidden
=============================================  ==================



Example of request with API-KEY
===============================
An example of request::

	curl -H "Accept:application/json" -H "X-API-KEY:hpG9DPvhCEpzkZqftqsgo3sS5gAyd1wu633h5PhELBo" "http://96.126.123.172:8080/stats/tippr/apps/Tippr"


Paging Control Headers
=======================
The client can specify HTTP parameters to control the paging of the result set returned by the API. The parameters, described in the table below, are optional.

============  ==============
Parameter	  Default Value
============  ==============
X-PAGE-SIZE   20
X-PAGE-NUMBER 1
============  ==============


When the data is received, the API informs of the paging using RESPONSE headers, according the following table:

==============  ===============================================================
Parameter	    Value
==============  ===============================================================
X-PAGE-SIZE     The number of results per page requested in the HTTP request 
X-PAGE-NUMBER   The page number returned 
X-PAGE-COUNT    The number of pages in the result set 
==============  ===============================================================


REST Resources for Apps
============================

URI::

	GET /[publisher-name]/apps
	
	
**App properties**

An iTunes app is represented by the following properties::

	{	
    	"date": "20111122T00:00Z",
    	"developer": "PoweredByTippr",
    	"downloads": 35,
    	"publisher": "tippr",
    	"title": "Tippr",
    	"updates": 8,
    	"version": "1.1.6"
	}
	
	
	
	
Apps Method 
================
**Pull the information for a single app**

*Format*::

	GET /[publisher-name]/apps/[app-id]
	
	
*Example*::

	GET /tippr/apps/Tippr
	
	
*Response*::

	{
    "date": "20111122T00:00Z",
    "developer": "PoweredByTippr",
    "downloads": 35,
    "publisher": "tippr",
    "title": "Tippr",
    "updates": 8,
    "version": "1.1.6"
}
	
**Pull the information for all the apps for a given publisher between dates**

*Format*::

	GET /[publisher-name]/apps?start-date=<start-date>&end-date=<end-date>
	
	
*Example*::

	GET /tippr/apps?start-date=20111122&end-date=20111123
	
	
*Response*::

	{
    	"appstats": [
        	{
            	"date": "20111122T00:00Z",
	            "developer": "PoweredByTippr",
    	        "downloads": 35,
        	    "publisher": "tippr",
            	"title": "Tippr",
	            "updates": 8,
    	        "version": "1.1.6"
        	},
	        {
    	        "date": "20111123T00:00Z",
        	    "developer": "PoweredByTippr",
            	"downloads": 435,
	            "publisher": "tippr",
    	        "title": "Tippr",
        	    "updates": 6,
            	"version": "1.1.6"
	        }
    	]
	}
	

	
	
	
	
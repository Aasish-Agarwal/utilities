# Living Documentation Generator

## Configure
Set the variable SERVERROOTDIR in server.py to the directory to the roor of your HTML files
SERVERROOTDIR = '../src/test/robotframework/acceptance'

## Creating new html files
Copy the template.html
Change the attribure "val" of div having id "docid" to map the file name along with path relative to root. for example if the html is created in "feature1/item2/keycases.html" w.r.t. root, the div should look like this


<div id=docid val="feature1/item2/keycases.html"></div>


## Execute
Open a command prompt
Move to folder where the server.py exists
Execute command python server.py

## Access your web pages
http://localhost:8000




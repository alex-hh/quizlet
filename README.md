To authorize the application and obtain an access token: follow the flow outline [here](https://yizhangid.blogspot.co.uk/2012/09/quizlet-api-how-to-get-oauth-access.html)

 1. register for an api account https://quizlet.com/api-dashboard, and find the client_id. set redirect url to some site which will allow you to retrieve an unmodified query string (try http://bbc.co.uk)
 2. in browser, go to https://quizlet.com/authorize/?response_type=code&client_id=$clientID&scope=write_set%20read&state=state
 3. set $BASIC_AUTH env var to "Basic <AUTH KEY>" (found at https://quizlet.com/api/2.0/docs/authorization_code_flow/), and $CODE env var to the code query string at the redirect url

TO install dictionaries:

One easy source of dictionaries is the OpenOffice.org project, which uses the same spelling engine. There is a list of available dictionaries at http://extensions.services.openoffice.org/. Note that TeXworks can only use the spelling dictionaries (*.dic and *.aff) for each language; to get them, rename the downloaded .oxt file to .zip and extract the spelling dictionary files (they may be contained in a subdirectory). (this is what I need to do: download the dictionary into the /Users/alexhooker/projects/informatics/py3env/lib/python3.4/site-packages/enchant/share/enchant/myspell directory.
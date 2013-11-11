import gflags
import httplib2
import os

from apiclient.discovery import build
from apiclient import errors
from oauth2client.client import flow_from_clientsecrets

from oauth2client.file import Storage
from oauth2client.tools import run


CLIENTSECRETS_LOCATION = 'client_secret.json'
SCOPE = 'https://www.googleapis.com/auth/drive'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENTSECRETS_LOCATION)


# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENTSECRETS_LOCATION,
                               scope=SCOPE,
                               message=MISSING_CLIENT_SECRETS_MESSAGE)

def retrieve_qs_files(service):
 """Retrieve a list of File resources.

 Args:
   service: Drive API service instance.
 Returns:
   List of File resources.
 """

 print "start retrieve_qs_files"

 result = []
 try:
   parent = '0B6wohqbOBqyKaktKY0c4YTFQdG8' # qs folder
   files = service.files().list(q="'%s' in parents and trashed = false" % parent).execute()
   result.extend(files['items'])
 except errors.HttpError, error:
   if error.resp.status == 401:
     # Credentials have been revoked.
     # TODO: Redirect the user to the authorization URL.

     raise NotImplementedError()
 print "end of retrieve_qs_files(service)"
 return result


def download_files(service, files):
  for item in files:
    # Check that the file is a csv file.
    if item['title'].find('.csv') > 0:
      print "Try to download %s" %(item['title'])
      content = download_file(service, item)
    
    if content is not None:
      print "Print content: "
      print content

  print "Done downloading files"


def download_file(service, drive_file):
 """Download a file's content.

 Args:
   service: Drive API service instance.
   drive_file: Drive File instance.

 Returns:
   File's content if successful, None otherwise.
 """
 download_url = drive_file.get('downloadUrl')
 
 if download_url:
   print "Attempting to download %s" %(drive_file['title'])
   resp, content = service._http.request(download_url)
   if resp.status == 200:
     print 'Status: %s' % resp
     return content
   else:
     print 'An error occurred: %s' % resp
     return None
 else:
   # The file doesn't have any content stored on Drive.
   return None


def main():
  # If the Credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('drive.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
      credentials = run(FLOW, storage)
      print "credentials have been set"

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)
  print "http object: "
  print http

  service = build("drive", "v2", http=http)
  print "service: "
  print service
  
  # Get list of data files.
  files = retrieve_qs_files(service)
  #print "\nfiles: "
  #print files

  # Open each data file.
  download_files(service, files)
  
  # Save data.
  f = open('file_list_from_Drive.txt', 'w') # Old version will be erased!
  f.write(str(files))
  f.close()


if __name__ == '__main__':
    main()
# MOST IMPORTANT NOTE: BEFORE WRITING A CHANNEL, THERE MUST ALREADY BE A URL SERVICE FOR THE VIDEOS ON THE WEBSITE
# YOU WANT TO CREATE A CHANNEL FOR OR YOU WILL HAVE TO WRITE A URL SERVICE BEFORE YOU CAN WRITE THE CHANNEL. TO
# SEE IF A URL SERVICE ALREADY EXISTS, CHECK THE SERVICES BUNDLE IN THE PLEX PLUGIN FOLDER
# <a href="http://www.freepik.com/free-photos-vectors/icon">Icon vector designed by Freepik</a>
# IMPORTANT NOTE: PYTHON IS VERY SENSITIVE TO PROPER INDENTIONS.  IF YOUR CHANNEL HAS IMPROPER INDENTIONS IT WILL
# NOT BE RECOGNIZED BY PLEX. I RUN THE PROGRAM THROUGH A CHECK MODULE ON A LOCAL VERSION OF PYTHON I HAVE LOADED
# PRIOR TO ACCESSING IT THROUGH PLEX TO MAKE SURE THERE ARE NO INDENTION ERRORS.

# You will need to decide how you want to set up your channel. If you want to have just one page that list all 
# the videos or if you want to break these videos down into subsections for different types of videos, individual shows, season, etc
# It is easiest to determine this system based on the structure of the website you are accessing. 

# You can hard code these choice in or pull the data from a web page or JSON data file and put it in a for loop to 
# automate the process. I created a basic example in the form of functions below to show the most common methods of 
# parsing data from different types of websites. When you want to produce results to the screen and have subpage come up # when they click on those results, you usually will use a
# DirectoryObject and include the name of the next function that will create that subpage called in the key.
# The key callback section sends your data to the next function that you will use to produce your next subpage.  Usually
# you will pass the value of the url onto your next function, but there are many attributes that can be sent.  It is good 
# to pass the title as well so it shows up at the top of the screen. Refer to the Framework Documentation to see the full
# list

# You will need a good working knowledge of xpath the parse the data properly.  Good sources for information related to 
# xpath are:fdf
# 'http://devblog.plexapp.com/2012/11/14/xpath-for-channels-the-good-the-bad-and-the-fugly/'
# 'http://forums.plexapp.com/index.php/toppic/49086-xpath-coding/'

# Here is a good article about working with Chrome Development Tools: 
# 'http://devblog.plexapp.com/2012/09/27/using-chromes-built-in-debugger-for-channel-development/'

# And here are a few pages that give you some pointers ON figuring out the basics of creating a channel
# 'http://devblog.plexapp.com/2011/11/16/a-beginners-guide-to-v2-1/'
# 'http://forums.plexapp.com/index.php/topic/28084-plex-plugin-development-walkthrough/'

# The title of your channel should be unique and as explanatory as possible.  The preifx is used for the channel
# store and shows you where the channel is executed in the log files
import xml.etree.ElementTree as ET
import datetime
import urllib2
import ast
import json

TITLE    = 'NextPVR Live TV'
NAME     = 'NextPVR'
PREFIX   = '/video/npvr'

# The images below are the default graphic for your channel and should be saved or located in you Resources folder
# The art and icon should be a certain size for channel submission. The graphics should be good quality and not be blurry
# or pixelated. Icons must be 512x512 PNG files and be named, icon-default.png. The art must be 1280x720 JPG files and be
# named, art-default.jpg. The art shows up in the background of the PMC Client, so you want to make sure image you choose 
# is not too busy or distracting.  I tested out a few in PMC to figure out which one looked best.

ART      = 'art-default.jpg'
ICON     = 'icon-default.png'

PVR_URL = 'http://%s:%s/' % (Prefs['server'],Prefs['port'])
PMS_URL = 'http://localhost:32400%s'
  
####################################################################################################

def Start():
    
    ObjectContainer.title1 = NAME
    Log('%s Started' % NAME)
    Log('URL set to %s' % PVR_URL)
    
    try:
        # Get curret server version and save it to dict.
        server_version = XML.ElementFromURL(PMS_URL % '', errors='ignore').attrib['version']
        Log('Server Version is %s' % server_version)
        Dict['server_version'] = server_version

    except: pass

    ValidatePrefs()


####################################################################################################
# This main function will setup the displayed items.
@handler('/video/npvr',NAME)
def MainMenu():
  
    Log('Client %s' % Request.Headers)
    clientident = ''
    try:
        clientident = Request.Headers['X-Plex-Client-Identifier']
    except:
        Log('Could not get client details')
 
    Log('Client Details: ident:%s' %  clientident)
    dir=ObjectContainer()
   
    Log('MainMenu: Adding Live Menu')
    dir.add(DirectoryObject(key=Callback(LiveMenu), title='Live',thumb=R('live.png')))
    
    dir.add(PrefsObject(title="Preferences", summary="Configure how to connect to NextPVR", thumb=R("icon-prefs.png")))
    Log('MainMenu: URL set to %s' % PVR_URL)
    return dir




####################################################################################################  
@route('/video/npvr/live')
def LiveMenu():
    oc = ObjectContainer(title2='Live')

    clientident = ''
    try:
      clientident = Request.Headers['X-Plex-Client-Identifier']
    except:
      Log('Could not get client details')

    url = PVR_URL + 'public/GuideService/Listing'
    Log('LiveMenu: Loading URL %s' % url)
    parsed_json = json.load(urllib2.urlopen(url))

    # Nodes with start_time > stime which is x number of days ago
    listings = parsed_json['Guide']['Listings']
    shows = []
    for listing in listings:
      Log('LiveMenu: **********************************************************************************************************')
      channelname = listing['Channel']['channelName']
      channelnumbermajor = listing['Channel']['channelNumber']
      channelnumberminor = listing['Channel']['channelMinor']
      channelid = listing['Channel']['channelOID']
      
      Log('LiveMenu: Channel number \'%s\'.\'%s\' name is \'%s\'' % (channelnumbermajor, channelnumberminor, channelname))
      
      Log('LiveMenu: Getting first programme for %s' % channelname)
   
      summary = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['Desc']
      programmname = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['Title']
      formattedChannel = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['FormattedChannelNumber']

      Log('LiveMenu: Channel name %s, Summary %s' % (programmname,summary))
      
      testURL = PVR_URL + 'live?channel=%s.%s&sid=plex&client=%s' % (channelnumbermajor,channelnumberminor,clientident) 
      Log('LiveMenu: URL set to %s' % testURL)
      oc.add(
      CreateVideoClipObject(
        url = testURL,
        title = formattedChannel + ' ' + programmname,
        summary=summary,
        rating_key=int(channelid),
        channel=channelid
        )
      )
    return oc




@route('/video/npvr/videoclipobject')
def CreateVideoClipObject(url, title, summary, rating_key, channel=None, container='mp2ts', include_container=False, includeRelated=False,includeRelatedCount=False):
  
    #later add channel call signs
    if not channel is None:
      thumb = R(ART)
    else:
      thumb = R(ART)

    Log('CreateVideoClipObject: Playvideo: ' + url)
    track_object = EpisodeObject(
      key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, rating_key=rating_key,channel=channel,container=container,include_container=True, includeRelated=False,includeRelatedCount=False),
      title = title ,
      summary = summary,
      originally_available_at = datetime.datetime.now(),
      duration = int(3600000),
      rating_key=int(rating_key),
      thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback='icon-default.png'),
      items = [
        MediaObject(
          parts = [
            PartObject(key=url)
          ],
          container = container,
          #video_resolution = 128,
          #video_codec = VideoCodec.H264,
          #audio_channels = 2,
          optimized_for_streaming = True
        )
      ]
    )
    

    if include_container:
      return ObjectContainer(objects=[track_object])
    else:
      return track_object


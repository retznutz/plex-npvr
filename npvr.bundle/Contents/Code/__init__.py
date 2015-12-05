# Made by retznutz
# Install at your own risk
# Copy freely

import xml.etree.ElementTree as ET
import datetime
import urllib2
import ast
import json

TITLE    = 'NextPVR Live TV'
NAME     = 'NextPVR'
PREFIX   = '/video/npvr'
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
      
      summary = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['Desc']
      programmname = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['Title']
      formattedChannel = listing['EPGEvents'][0]['epgEventJSONObject']['epgEvent']['FormattedChannelNumber']

      Log('LiveMenu: Channel name %s, Summary %s' % (programmname,summary))
      
      playbackUrl = PVR_URL + 'live?channel=%s.%s&sid=plex&client=%s' % (channelnumbermajor,channelnumberminor,clientident) 

      oc.add(
      CreateVideoClipObject(
        url = playbackUrl,
        title = channelname + ' (' + formattedChannel + ')  ' + programmname,
        summary=summary,
        rating_key=int(channelid),
        call_sign = channelname,
        channel=channelid,
        
        )
      )
    return oc




@route('/video/npvr/videoclipobject')
def CreateVideoClipObject(url, title, summary, rating_key, call_sign='', channel=None, container='mp2ts', include_container=False, includeRelated=False,includeRelatedCount=False):
  
    #later add channel call signs
    if not channel is None:
      thumb = R(call_sign + '.png')
      Log('Logo: ' + call_sign + '.png')
      if thumb is None:
        thumb = R(ICON)
        
    Log('CreateVideoClipObject: Playvideo: ' + url)
    track_object = EpisodeObject(
      key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, rating_key=rating_key,channel=channel,container=container,include_container=True, includeRelated=False,includeRelatedCount=False),
      title = title ,
      summary = summary,
      originally_available_at = datetime.datetime.now(),
      #duration = int(0),
      rating_key=int(rating_key),
      thumb = thumb,
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


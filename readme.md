Plex plugin for use with NextPVR - http://www.nextpvr.com/

This is a super-early release of a NextPVR plugin for Plex for watching live TV. Please have the latest versions of both. Thanks to psyciknz (https://github.com/psyciknz/NextPVR-Plex) for his code which I used for an example. I've updated / changed the code base enough I didn't think it prudent to fork.

This plugin uses the new NextPVR webservice and handles channels with sub-channels (example: channel 4 is actually 4.1, 4.2, 4.3).

This is super early code, and while it works for me, you may need ot tweak it. As always, copy the npvr.bundle to your Plex Media Server plug-ins folder to use. Make sure you configure this plugin (with the settings gear icon in Plex).

To add icons to your channels, just name the image file (PNG's only) the name of the channel name and drop them in the Resources folder of this plugin.  The channel name is the first word or words you see before the channel number in the channels listing.  For example: WISN-TV (12.1) Entertainers: With Some Guy.  WISN-TV is the channel name, so make an icon called wisn-tv.png  or CW 18 (18.1) Noel - CW 18 is the name, so make the icon called cw 18.png (watch out of capitalization in linux).


Some References:
<a href="http://www.freepik.com/free-photos-vectors/icon">Icon vector designed by Freepik</a>
<a href="http://www.1001freefonts.com/designer-nicks-fonts-fontlisting.php">Aerovias Brasil by Nick</a>
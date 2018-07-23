#!/usr/bin/env python

import os, sys, subprocess, json
from pprint import pprint
from termcolor import colored
# https://github.com/inAudible-NG/tables
ffprobe = '/usr/bin/ffprobe'
ffmpeg = '/usr/bin/ffmpeg'
rainbowtables_location='/home/james/bin/tables'

def rip(this_file):
    this_dir = os.path.dirname(this_file)
    #pprint(this_dir)
    if this_dir:
        activation_file = this_dir + '/activation.txt'
    else :
        activation_file = 'activation.txt'
    #pprint(activation_file)
    if (os.path.isfile(activation_file)):
        f = open(activation_file, 'r')
        activation_bytes = f.readline().strip()
        #pprint(activation_bytes)
        pass

    if activation_bytes:
        ffprobe_command = '%s -show_data -show_format -show_streams -print_format json %s' % (ffprobe, this_file)
        process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (out, err) = process.communicate()
        #print err
        props = json.loads(out)
        #print 'props: '
        #pprint(props)
        try:
            title = props['format']['tags']['title'].encode('utf-8').replace('(Unabridged)', '').replace('Free Version', '').strip().replace(' ', '_').replace(':', '').replace(',', '').replace("'", '').replace('!', '')
            #print 'title: %s' % title
        except:
            print colored('---- cannot generate title from title in metatags of %s' % this_file, 'red')
            pprint(props['format']['tags'])

        if this_dir:
            new_file = '%s/%s.m4a' % (this_dir, title)
        else:
            new_file = '%s.m4a' % (title)
        if (os.path.isfile(new_file)):
            print colored(new_file, 'green') + colored(' already exists' , 'yellow')
        else:
            print 'ripping %s' % (colored(title, 'green'))
            ffmpeg_command = '%s -activation_bytes %s -i "%s"  -map_metadata 0 -y -vn -c:a copy "%s"' % (ffmpeg, activation_bytes, this_file, new_file)
            pprint(ffmpeg_command)
            # copy the streams and metadata including the album art
            ffmpeg_command = '%s -activation_bytes %s -i "%s"  -map_metadata 0 -map 0:0 -map 0:2 -y  -c:a copy "%s"' % (ffmpeg, activation_bytes, this_file, new_file)
            pprint(ffmpeg_command)
            os.system(ffmpeg_command)
    # ffmpeg -activation_bytes 62037501 -i B002UZJF4U_ep5.aax -map_metadata 0 -y -vn -c:a copy "The Three Musketeers (Unabridged).m4a"
    pass

if __name__=='__main__':
    files = sys.argv[1:]
    for this_file in files:
        rip(this_file)
    pass
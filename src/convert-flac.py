"""
usage:
    convert-flac.py [-i indir] [-o outdir] [-b bitrate] [--ffmpeg=FFMPEG]

options: 
    -i indir            input directory
    -o outdir           output directory
    -b bitrate          output bitrate (in kbits/s)
    --ffmpeg=FFMPEG     which ffmpeg to use
"""

import os
import sys
import re
from docopt import docopt

FFMPEG = "/usr/local/bin/ffmpeg"
CMD = ["%(ffmpeg)s",
       "-i \"%(infile)s\"",
       "-b:a %(bitrate)sk",
       "-metadata title=\"%(title)s\"",
       "-metadata album=\"%(album)s\"",
       "-metadata artist=\"%(artist)s\"",
       "-metadata year=\"%(year)s\"",
       "-metadata track=\"%(track)s\"",
       "\"%(outfile)s\""]
DEFAULT_BITRATE = "256"

def convert_song(fname, infolder, outfolder, stats):
    """
    Main per-song entry point

    Task:
        fname       filename w/o dir
        infolder    source dir
        outfolder   dest dir
        stats       {'artist', 'album', 'year', 'bitrate'}
    """
    song_specs = analyze_filename(fname)
    if song_specs == None:
        print "Couldn't extract data from filename %s, skipping" % fname
        return
    stats.update(song_specs)
    outfile = "%s.mp3" % re.match("^(.*)\.flac$", fname).groups()[0]
    stats.update({'infile':os.path.join(infolder, fname),
                  'outfile':os.path.join(outfolder, outfile)})
    clean_common_title_goofs(stats)
    ## convert the song
    cmd = " ".join(CMD) % stats
    ## print cmd   ## for debugging
    os.system(cmd)

def clean_common_title_goofs(stats):
    """
    A bit more cleanup. This function mutates its input!
    """
    m = re.match("(?P<artist>%s)[\s-]+(?P<title>.*)$" % stats['artist'], stats['title'])
    if m != None:
        ## title is of form <artist> - <title>, remove artist
        stats['title'] = m.groupdict()['title']

def analyze_filename(fname):
    """
    Extract title/track number from filename
    returns {'title', 'track'}
    """
    m = re.match("^(?P<track>[0-9]+)[\s-]+(?P<title>.+)\.flac$", fname)
    if m != None:
        return m.groupdict()   ## return {'title', 'track'}
    m = re.match("^(?P<title>.*)\.flac$", fname)
    if m != None:
        d = m.groupdict()
        d.update({'track':''})
        return d
    return None

def prep_outfolder(outf):
    """
    make sure the outfolder exists and is readable
    """
    if not os.path.exists(outf):
        if not os.access(os.path.dirname(outf), os.W_OK):
            error("Can't write to directory %s" % os.path.dirname(outf))
        os.mkdir(outf)
    if not os.access(outf, os.W_OK):
        error("Can't write to directory %s" % outf)

def main(infolder, outfolder, bitrate, ffmpeg):
    if not os.access(infolder, os.R_OK):
        error("Can't read from directory %s" % infolder)
    prep_outfolder(outfolder)
    stats = {'bitrate':bitrate,
             'ffmpeg':ffmpeg}
    stats['artist'] = raw_input("artist name: ")
    stats['album'] = raw_input("album: ")
    stats['year'] = raw_input("year: ")
    print "operating with stats:\n%s" % stats
    print "infolder: %s" % infolder
    print "outfolder %s" % outfolder
    return len([convert_song(f, infolder, outfolder, stats) for f in filter(lambda x: re.match("^.*\.flac$", x) != None, os.listdir(infolder))])

def error(msg):
    print "ERROR: %s" % msg
    sys.exit(-1)

if __name__ == "__main__":
    opts = docopt(__doc__)
    indir = opts['-i'] if opts['-i'] else os.getcwd()
    outdir = opts['-o'] if opts['-o'] else os.path.join(indir, "mp3")
    bitrate = opts['-b'] if opts['-b'] else DEFAULT_BITRATE
    ffmpeg = opts['--ffmpeg'] if opts['--ffmpeg'] in opts else FFMPEG
    print "%d songs processed" % main(indir, outdir, bitrate, ffmpeg)

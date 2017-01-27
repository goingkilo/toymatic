
import os, sys
from PIL import Image

#size1 = 128,128
size2 = 320,150
size3 = 800,300

folders = {}

def thumbnail( infile, size, outfunction):
    im = Image.open( infile)
    im.thumbnail( size)
    outfile = outfunction(infile,size)
    im.save(outfile)

def get_jpegs(folder):
    files = [x for x in os.listdir(folder) if x]
    jpegs = [x for x in files if x.endswith('jpg') or x.endswith('JPG') or x.endswith('jpeg') or x.endswith('JPEG')]
    return jpegs


def get_output_file( filename, size):
    #a =   os.path.splitext(filename)[0] + '_' + '_'.join([str(x) for x in list(size)]) +'.jpg'
    if size == size2:
        return '../small/' + filename
    return '../medium/' + filename

for jpg in get_jpegs( sys.argv[1]):
    try:

        thumbnail( jpg, size2, get_output_file)
        thumbnail( jpg, size3, get_output_file)
    except IOError,e:
        print "cannot create thumbnail for", jpg,e

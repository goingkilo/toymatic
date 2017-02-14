import csv, os, json
from PIL import Image


small_size = 320,150
main_size = 800,300

def thumbnail( infile, size, outfile):
    im = Image.open( infile)
    im.thumbnail( size)
    im.save(outfile)

def readcsv( a, b):
    with open( a, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            yield b(row)


def get_row( row):
    return row

def process_row(col):
    ret = {}
    ret['id']  = col[0]
    ret['title']   = col[1]
    ret['ages']     = col[5]
    ret['image'] = col[9]
    ret['desc']    = col[12]

    folder = col[0]
    outfolder = 'i'+col[0]

    if not os.path.exists(folder):
        return None

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)
    jpgs = [x for x in os.listdir( './' + folder) if x]
    counter = 1
    small_images = []
    for i in jpgs:
        infile = './'+ folder+'/'+i
        outfile = './' + outfolder+'/'+folder+'_'+str(counter)+'.jpg'
        thumbnail( infile, small_size, outfile)
        counter += 1
        small_images.append( '/static/images/inventory/' + outfile[1:])

    ret["secondary_images"] = ','.join(small_images)

    thumbnail( './'+ folder+'/'+ ret["image"], main_size, './' + outfolder+'/'+folder+'_main.jpg')

    ret["image"] = small_images[0]
    ret["image_large"] = '/static/images/inventory/' + outfolder+'/'+folder+'_main.jpg'

    #print json.dumps( ret, indent=4)
    return ret


rows = [x for x in readcsv( 'inventory.csv', get_row)]
a  = []
for i in rows:
    b = process_row(i)
    if b:
        a.append(b)
print json.dumps( a, indent=4)



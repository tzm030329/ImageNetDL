# coding: utf-8

import sys
import os
from urllib import request
from PIL import Image
import json


def download(url, decode=False, timeout=60):
    response = request.urlopen(url, timeout=timeout)
    if response.geturl() == "https://s.yimg.com/pw/images/en-us/photo_unavailable.png":
        # Flickr :This photo is no longer available iamge.
        raise Exception("This photo is no longer available iamge.")

    body = response.read()
    if decode == True:
        body = body.decode()
    return body


def write(path, img):
    file = open(path, 'wb')
    file.write(img)
    file.close()


if __name__ == '__main__':
    args = sys.argv
    ii = int(args[1])
    istr = '%d' % ii

    f = open('imagenet_class_index.json', 'r')
    dic = json.load(f)
    f.close()

    tdir, tid = dic[istr]
    print(tdir, tid)

    offset = 0
    nmax = 50

    urldir = './urls'
    urlfile = '%s/%04d_%s_%s.txt' % (urldir, ii, tid, tdir)
    if not os.path.exists(urlfile):
        print('%s is not exist' % urlfile)
        print('Use \'sh dl_urllist.sh\' for making URL list for image download.')
        sys.exit()

    else:
        print('read URL list for %s (%s) from files' % (tdir, tid))
        inf = open(urlfile, 'r')
        urls = inf.readlines()
        inf.close()

    print('Number of URLs: %d' % len(urls))

    itry, iget = 0, 0
    for url in urls:
        if itry < offset:
            itry = itry+1
            continue
        if iget > nmax:
            break

        try:
            tfile = os.path.split(url)[1]
            name, ext = os.path.splitext(tfile)
            ext = ext.lower()
            outdir = 'data/%04d_%s' % (ii, tdir)
            if not os.path.exists(outdir):
                os.makedirs(outdir, exist_ok=True)
            path = '%s/%04d_%04d_%s_%s%s' % (outdir, ii, iget, tid, tdir, ext)
            path = path.strip() # remove \n, \r, \r\n
            if not os.path.exists(path):
                print(path)
                write(path, download(url, timeout=15))
            print('done: %d: %s' % (itry, tfile))
            iget = iget+1

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print('done: %d: %s' % (itry, tfile))

        itry = itry+1

    print("end")

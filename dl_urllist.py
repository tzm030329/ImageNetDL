# coding: utf-8

import sys
import os
import json
from urllib import request


def download(url, decode=False, timeout=60):
    response = request.urlopen(url, timeout=timeout)
    body = response.read()
    if decode == True:
        body = body.decode()
    return body


if __name__ == '__main__':
    args = sys.argv
    istr = args[1]
    i = int(istr)

    f = open('imagenet_class_index.json', 'r')
    dic = json.load(f)
    f.close()

    tid, tdir = dic[istr]
    print(i, tdir, tid)

    outdir = 'urls'
    if not os.path.exists(outdir):
        os.makedirs('%s' % outdir)

    urlfile = '%s/%04d_%s_%s.txt' % (outdir, i, tdir, tid)
    if not os.path.exists(urlfile):
        print('try to get URL list for class \'%s (%s)\' from Imagenet website' % (tdir, tid))
        url = "http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s" % tid
        urls = download(url, decode=True, timeout=60).split()
        of = open(urlfile, 'w')
        for line in urls:
            of.write('%s\n' % line)
        of.close()

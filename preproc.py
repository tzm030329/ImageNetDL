# coding: utf-8

import os
import numpy as np
import cv2
from glob import glob
from skimage import io as skio


def preproc(target):
    tid = target.split('_')[0]

    tdir = 'data/%s' % target
    files = sorted(glob('%s/%s_*' % (tdir, tid)))

    outdir = 'imgs/%s' % target
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    thumout = 'thum'
    if not os.path.exists(thumout):
        os.makedirs(thumout)

    i = 0
    imgs = []
    for ifile in files:
        name, ext = os.path.splitext(os.path.basename(ifile))
        try:
            img = skio.imread(ifile)
        except:
            print('%s is not an image file !' % ifile)
            continue

        # white image
        if img.std() < 5.0:
            continue

        # color channel > 3
        if img.shape[2] > 3:
            continue

        # gray image
        if len(img.shape) == 2:
            print('gray')
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        # gif anime
        if len(img.shape) == 4:
            img = img[0]

        # resize
        h, w, c = img.shape
        if h>w:
            hst, hed = h//2-w//2, h//2+w//2
            img = img[hst:hed]
        else:
            wst, wed = w//2-h//2, w//2+h//2
            img = img[:,wst:wed]

        if min(img.shape[:2]) < 224:
            interp = cv2.INTER_CUBIC
        else:
            interp = cv2.INTER_LINEAR

        img = cv2.resize(img, (224,224), interpolation = interp)

        # to uint8
        img = img.astype(np.uint8)
        thum = cv2.resize(img, (64,64), interpolation=cv2.INTER_LINEAR)
        imgs.append(thum)
        print('%s mean=%.3f std=%.3f'%
              (name, img.mean(), img.std()), img.shape, len(img.shape))
        skio.imsave('%s/%s.png' % (outdir, name), img)
        i = i+1

    print('number of images = %d' %i)
    nthum = min(i, 49)
    imgs = np.array(imgs)[:nthum]
    n,h,w,c = imgs.shape
    m = np.int(np.ceil(np.sqrt(n)))
    add = np.zeros((m**2-n,h,w,c), dtype=np.uint8)
    dst = np.append(imgs, add, axis=0)
    dst = dst.reshape(m,m,h,w,c).transpose(0,2,1,3,4).reshape(m*h,m*w,c)
    skio.imsave('%s/%s.png' % (thumout, target), dst)


if __name__ == '__main__':

    dirs = sorted(glob('data/0*'))
    for idir in dirs:
        target = os.path.basename(idir)
        preproc(target)

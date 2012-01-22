#!/bin/bash

cd /usr/share/magicrescue/recipes

magicrescue /dev/md1p1 -d /media/magicrescue -r avi -r flac -r gzip -r jpeg-exif -r jpeg-jfif -r mp3-id3v1 -r mp3-id3v2 -r msoffice -r png -r zip &> /media/magicrescue.log

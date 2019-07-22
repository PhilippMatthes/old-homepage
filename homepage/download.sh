#!/bin/bash
fileid="1iXjsizwiCRTtbfOG8Y_L955P0Ju808bl"
filename="siri/logdir.zip"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

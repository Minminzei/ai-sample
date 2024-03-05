#!/bin/sh

echo "create video to images"
python files.py video_to_images -n input_a -f 5
python files.py video_to_images -n input_b -f 5
python files.py video_to_images -n convert -f 10

echo "extract images"
python extract.py extract -n input_a
python extract.py extract -n input_b
python extract.py extract -n convert

echo "clustering images"
python extract.py sort_by_face -n input_a
python extract.py sort_by_face -n input_b
python extract.py sort_by_face -n convert
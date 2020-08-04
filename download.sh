#!/bin/bash

if [ ! -d html ]; then
	mkdir html
fi
cd html

for name in $(cat ../list)
do
	wget https://dnd-5e.herokuapp.com/monsters/$name
	../fix_head.py $name
	mv $name $name.html
done

#!/bin/bash
git pull
current_date=$(date)
echo $current_date >> input.txt
git add input.txt
git commit -m "$current_date"
git push

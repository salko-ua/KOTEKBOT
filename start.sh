#!/bin/bash
current_date=$(date)
echo $current_date >> input.txt
git add .
git commit -m "$current_date"
git push

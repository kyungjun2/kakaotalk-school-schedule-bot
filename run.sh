#!/bin/bash
cd "$(dirname "$0")"

git pull https://github.com/kyungjun2/kakaotalk-school-schedule-bot.git
git update-index --chmod=+x run.sh

nohup python3 app.py >> log.log &

logresult=$(tail -n 6 log.log)
echo "$logresult"

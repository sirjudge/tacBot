#!/bin/sh
for ((i=1;i<10;i++));
do
  java -jar match-wrapper-1.3.2.jar "$(cat wrapper-commands.json)" &
  BACK_PID=$!
  while kill -0 $BACK_PID ; do
    echo "Process is still active..."
    sleep 10
  #start cleanup stuff
  python cleanUp.py
done
done

echo all done!

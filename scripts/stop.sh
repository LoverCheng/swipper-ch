#!/bin/bash

BASE_DIR="/opt/swiper"
PID_FILE="$BASE_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    GUNICORN_PID=`cat $PID_FILE`
    kill $GUNICORN_PID
    echo 'Gunicorn 程序已关闭'
else
    echo 'Gunicorn 的 pid 文件未找到'
fi

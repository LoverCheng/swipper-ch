#!/bin/bash
# 平滑重启
# 11295 master

# # 旧的进程
# 15259 worker <- 2736
# 15260 worker <- 3725
# 15261 worker <- 7362
# 15262 worker <- 7251

# # 当 master 收到 kill -HUP 的信号后，先产生新的子进程，然后等旧的子进程处理完毕后，再将其关闭
# 18412 new worker <- 12
# 18413 new worker <- 21
# 18414 new worker <- 42
# 18415 new worker <- 12


BASE_DIR="/opt/swiper"
PID_FILE="$BASE_DIR/logs/gunicorn.pid"

if [ -f $PID_FILE ]; then
    echo '正在重启服务器'
    GUNICORN_PID=`cat $PID_FILE`
    kill -HUP $GUNICORN_PID
    echo 'Gunicorn 程序已重启完毕'
else
    echo 'Gunicorn 的 pid 文件未找到'
fi

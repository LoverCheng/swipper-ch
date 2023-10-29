#!/bin/bash

LOCAL_DIR="./"
REMOTE_DIR="/opt/swiper/"
USER="ubuntu"
HOST="121.36.230.33"

# 获取指定代码版本
if [ -z "$1" ]; then
    echo '请输入正确的参数'
    exit 1
fi

# 检查版本切换是否成功
if git checkout $1; then
    rsync -crvP --exclude={.git,.venv,.vscode,logs,__pycache__} $LOCAL_DIR $USER@$HOST:$REMOTE_DIR

    # 重启远程服务器
    read -p '您是否要重启服务器? (y/n) ' user_input
    if [[ "$user_input" == "y" ]]; then
        ssh $USER@$HOST 'bash /opt/swiper/scripts/restart.sh'
    fi

    # 切回之前操作的分支
    git checkout -
else
    echo "您输入的版本不存在"
    echo 1
fi

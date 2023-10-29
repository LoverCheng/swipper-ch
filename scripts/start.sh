#!/bin/bash

BASE_DIR="/opt/swiper"

# 加载虚拟环境
cd $BASE_DIR
source .venv/bin/activate
gunicorn -c swiper/gconfig.py swiper.wsgi
deactivate
cd -

#!/bin/bash
# 一键部署脚本

# 系统更新
system_update() {
    echo '正在更新系统...'
    apt update -y
    apt upgrade -y
    echo -e '系统更新完毕.\n'
}


# 安装系统软件
install_software() {
    echo '正在安装系统组件...'
    BASIC='man sudo lsof ssh openssl tree vim language-pack-zh-hans'
    EXT='dnsutils iputils-ping net-tools psmisc sysstat'
    NETWORK='curl telnet traceroute wget'
    LIBS='libbz2-dev libpcre3 libpcre3-dev libreadline-dev libsqlite3-dev libssl-dev zlib1g-dev'
    SOFTWARE='mysql-server zip p7zip apache2-utils sendmail'
    apt install -y $BASIC $EXT $NETWORK $LIBS $SOFTWARE

    echo '正在清理临时文件'
    apt autoremove
    apt autoclean

    echo '正在设置中文环境'
    locale-gen zh_CN.UTF-8
    export LC_ALL='zh_CN.utf8'
    echo "export LC_ALL='zh_CN.utf8'" >> /etc/bash.bashrc

    echo '正在启动邮件服务'
    systemctl start sendmail

    echo -e '系统组件安装完毕.\n'
}


# 安装 Nginx
install_nginx() {
    echo '正在安装 Nginx...'
    if ! which nginx > /dev/null
    then
        apt install -y curl gnupg2 ca-certificates lsb-release
        echo "deb http://nginx.org/packages/ubuntu `lsb_release -cs` nginx" \
            | tee /etc/apt/sources.list.d/nginx.list
        curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -
        apt update
        apt install -y nginx
        echo -e 'Nginx 安装完毕.\n'
    else
        echo -e 'Nginx 已存在.\n'
    fi
}


# 安装 Redis
install_redis() {
    echo '正在安装 Redis'
    if ! which redis-server > /dev/null
    then
        wget -P /tmp/ 'http://download.redis.io/releases/redis-5.0.0.tar.gz'
        tar -xzf /tmp/redis-5.0.0.tar.gz -C /tmp
        cd /tmp/redis-5.0.0
        make && make install
        cd -
        rm -rf /tmp/redis*
        echo -e 'Redis 安装完毕.\n'
    else
        echo -e 'Redis 已存在\n'
    fi
}


# 编译安装 Python 3
install_python() {
    echo '正在安装 Python 3'
    if ! which python3 > /dev/null;
    then
        apt install -y python3
        apt install -y python3-pip
        echo -e 'Python3 安装完毕.\n'
    else
        echo 'Python3 已存在'
    fi

    if ! python --version|grep 'Python 3' > /dev/null
    then
        mkdir -p ~/.local/bin
        ln -sfv `which python3` ~/.local/bin/python
        ln -sfv `which pip3` ~/.local/bin/pip
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc
        source $HOME/.bashrc
        echo -e "Python 环境设置完毕.\n"
    fi
}


# 项目环境初始化
project_init() {
    echo '正在设置项目环境...'
    proj='/opt/swiper/'
    mkdir -p $proj/logs

    echo '正在创建 python 运行环境...'
    if [ ! -d $proj/.venv ]; then
        python -m venv $proj/.venv
    fi
    source $proj/.venv/bin/activate
    pip install -U pip
    if [ -f $proj/requirements.txt ]; then
        pip install -r $proj/requirements.txt
    fi
    deactivate

    echo -e '项目环境设置完毕.\n'
}

install_all() {
    system_update
    install_software
    install_nginx
    install_redis
    install_pyenv
    set_pyenv_conf
    install_python
    project_init
}


cat << EOF
请输入要执行的操作的编号: [1-9]
===============================
【 1 】 系统更新
【 2 】 安装系统组件
【 3 】 安装 Nginx
【 4 】 安装 Redis
【 5 】 安装 Python
【 6 】 项目运行环境初始化
【 7 】 全部执行
【 * 】 退出
===============================
EOF

# 获取要执行的操作编号
if [[ -n $1 ]]; then
    OPT_NUM=$1
    echo "执行操作: $1"
else
    read -p "请选择: " OPT_NUM
fi

case $OPT_NUM in
    1) system_update;;
    2) install_software;;
    3) install_nginx;;
    4) install_redis;;
    5) install_python;;
    6) project_init;;
    7) install_all;;
    *) exit;;
esac

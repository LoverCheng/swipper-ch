'''程序配置，及第三方平台配置'''

# Redis 配置
REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
}


# 滑动积分配置
SWIPE_SCORE = {
    'like': 5,
    'superlike': 7,
    'dislike': -5,
}


# 赛迪云通信配置
SD_API = 'https://api.mysubmail.com/message/xsend'
SD_APPID = '48182'
SD_APPKEY = '499871e968f40f1a50517b5ecd6bb74b'
SD_PROJECT = '2OuxR3'
SD_SIGN_TYPE = 'md5'


# 七牛云配置
QN_HOST = 'http://qdwxojq56.bkt.clouddn.com'
QN_ACCESS_KEY = 'kEM0sRR-meB92XU43_a6xZqhiyyTuu5yreGCbFtw'
QN_SECRET_KEY = 'QxTKqgnOb_UVldphU261qu9IdzmjkgGHh6GQVPPy'
QN_BUCKET = 'sh2001'
QN_TIMEOUT = 600

import pymysql

from libs.orm import patch_model

pymysql.install_as_MySQLdb()  # 使用 pymysql 伪装成 MySQLdb
patch_model()  # 为 model 打补丁，添加缓存处理

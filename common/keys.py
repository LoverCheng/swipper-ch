'''所有缓存的 Key'''

VCODE_K = 'Vcode-%s'  # 验证码的 Key, 拼接用户的手机号
FIRST_RCMD_Q = 'FirstRcmdQ-%s'  # 优先推荐队列，拼接用户的 uid
PROFILE_K = 'Profile-%s'  # 用户资料的 Key，拼接 uid
MODEL_K = 'Model-%s-%s'  # Model 的缓存 Key，拼接 Model 的名称，和对象的主键
HOTRANK_K = 'HotRank'

"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home import views
from user import apis as user_api
from social import apis as social_api


urlpatterns = [
    url(r'^$', views.home),

    url(r'api/user/vcode/fetch', user_api.fetch_vcode),
    url(r'api/user/vcode/submit', user_api.submit_vcode),
    url(r'api/user/profile/show', user_api.show_profile),
    url(r'api/user/profile/update', user_api.update_profile),

    url(r'qiniu/token', user_api.qn_token),
    url(r'qiniu/callback', user_api.qn_callback),

    url(r'api/social/rcmd', social_api.rcmd_users),
    url(r'api/social/like', social_api.like),
    url(r'api/social/superlike', social_api.superlike),
    url(r'api/social/dislike', social_api.dislike),
    url(r'api/social/rewind', social_api.rewind),
    url(r'api/social/fans', social_api.show_fans),
    url(r'api/social/friends', social_api.show_friends),
    url(r'api/social/rank', social_api.hot_rank)
]

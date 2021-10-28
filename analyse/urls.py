from django.contrib import admin
from django.urls import include, path
from . import views


# 这是analyse分析路由分发
urlpatterns = [

    path(r'hello/', views.hello),
    path(r'world/', views.world),
    path(r'worldCloud/', views.worldCloud),

    #**********V2.0************
    #=========总体分析==========
    path(r'job_city_num/',views.job_city_num),  # 表1 城市职位需求
    path(r'job_keyword/',views.job_keyword),  # 表2 编程语言
    path(r'job_exp/',views.job_exp),  # 表3 工作经验
    path(r'job_edu/',views.job_edu),  # 表4 学历水平
    path(r'job_city_money/',views.job_city_money),  # 表5 城市薪资水平
    path(r'job_edu_money/',views.job_edu_money),  # 表6 学历薪资水平
    path(r'job_exp_money/',views.job_exp_money),  # 表7 经验薪资水平
    path(r'job_wordcloud/',views.job_wordcloud),  # 表7 经验薪资水平

    #========行业分析============
    path(r'pandect/', views.pandect),
    path(r'Java/', views.Java),
    path(r'Python/', views.Python),
    path(r'PHP/', views.PHP),
    path(r'C++/', views.C_add_add),
    path(r'NET/', views.NET),
    path(r'Android/', views.Android),
    path(r'AI/', views.AI),
    path(r'Algorithm/', views.Algorithm),

    #=========查询=============
    path(r'seachs/',views.seachs),  # 测试
    path(r'posts/',views.posts),  # 测试
    # path(r'search1/',views.search1),
    path(r'search2/',views.search2),

    # =====反馈=======
    path(r'feedback/',views.feedback),

    # ======index========
    path(r'index/',views.index),

]
from django.shortcuts import render,redirect

import jieba
import jieba.analyse

# Create your views here.
import pymysql

class MysqlConnet(object):
    def __init__(self,sql):
        self.sql = sql

    def select(self):
        mysql = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='jobinfo',
                                charset='utf8')  # 链接数据库
        # 2.新建个查询页面
        cursor = mysql.cursor()
        # 3编写sql
        sql = self.sql
        # 4.执行sql
        cursor.execute(sql)
        results = cursor.fetchall()  # 用于返回多条数据
        # 6.关闭查询
        cursor.close()

        # 关闭数据库
        mysql.close()
        return results

# --------------测试-------------------
def hello(request):
    context = {}
    context['data1'] = 'analyse'
    return render(request,'index.html',context=context)

def world(request):
    context = {}
    context['data'] = 'analyse'
    return render(request,'world.html',context=context)

def worldCloud(request):
    context = {}
    keyword = '"PHP"'
    sql = "select job_weal from jobdata where keywords = " + keyword
    p1 = MysqlConnet(sql)
    result = p1.select()

    string = ''
    for i in result:
        string = string + i[0].replace(',', '')
        string = string + ' '

    jieba.load_userdict(r'E:\Python\02-爬虫\MyProject\analyse\weal_dic.txt')  # 自定义词组
    word_weights = jieba.analyse.extract_tags(string, topK=30, withWeight=True)  # topK 前50个  withWeight返回权重
    # print(word_weights)
    word_list = []
    for i in word_weights:
        word = {}
        word['name']=i[0]
        word['value']=i[1]
        word['emphasis'] = {'textStyle': {'color': 'red'}}

        word_list.append(word)

    context['data4'] = word_list

    return render(request,'worldCloud.html',context=context)

# ----------------------------------------------------

# 总览
def pandect(request):  # -------这是总览总体分析-------
    context = {}
    # 表1 main1 各城市职位数
    sql = 'select job_city ,count(*) from jobdata group by job_city'
    p1 = MysqlConnet(sql)
    results = p1.select()
    city1 = []
    data1 = []
    for i in results:
        city1.append(i[0])
        data1.append(i[1])
    # context['city'] = ["北京", "上海", "广州", "深圳", "成都", "杭州", "重庆", "武汉", "东莞", "佛山", "合肥", "大连", "福州", "厦门"]
    # context['data'] = [6380, 4060, 2153, 5108, 2866, 2336, 1202, 1817, 556, 610, 1424, 1298, 1244, 930]
    context['city1'] = city1
    context['data1'] = data1

    # 表2 编程语言职位数
    sql = 'select keywords as "职位" ,count(*) as "职位数" from jobdata group by keywords'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li1 = []
    li2 = []
    for i in range(len(results)):
        li1.append(results[i][0])
        li2.append(results[i][1])
    context['name2'] = li1
    context['data2'] = li2

    # 表3 工作经验
    ''' 饼图应该输入
        [
        {name:'',value:}
        ]
        '''
    sql = 'select job_exp ,count(*) from jobdata group by job_exp order by count(*) DESC'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li = []
    dontShow = ['提篮桥', '', '西北旺']  # 数据清洗
    for i in results:
        if i[0] in dontShow:
            continue
        dic = {}
        dic['value'] = i[1]
        dic['name'] = i[0]
        li.append(dic)
    context['data3'] = li

    # 表4  学历水平
    ''' 饼图应该输入
            [
            {name:'',value:}
            ]
            '''
    # 这是工作学历统计的sql 饼图
    sql = 'select job_edu ,count(*) from jobdata group by job_edu order by count(*) DESC'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li = []
    for i in results:
        dic = {}
        dic['value'] = i[1]
        dic['name'] = i[0]
        li.append(dic)
    context['data4'] = li

    # 表5 各城市薪资水平
    # 这是各城市薪资sql   floor 和 upper
    sql = 'SELECT job_city,round(sum(job_money_floor)/count(*)*job_money_month/12,2),round(sum(job_money_upper)/count(*)*job_money_month/12,2) FROM jobinfo.jobdata where job_money_floor != 0 group by job_city'
    p1 = MysqlConnet(sql)
    results = p1.select()
    city5 = []
    floor5 = []
    upper5 = []
    for i in results:
        city5.append(i[0])
        floor5.append(i[1])
        upper5.append(i[2])
    context['city5'] = city5
    context['floor5'] = floor5
    context['upper5'] = upper5

    # 表6 main6 学历-薪资水平对比
    # z这是对比学历和工资的关系  条形统计图
    sql = 'SELECT job_edu ,round(sum(job_money_avg)/count(*),2) from jobdata group by job_edu order by round(sum(job_money_avg)/count(*),2) '
    p1 = MysqlConnet(sql)
    results = p1.select()
    edu6 = []
    moneyAvg6 = []

    for i in results:
        edu6.append(i[0])
        moneyAvg6.append(i[1])
    context['edu6'] = edu6
    context['moneyAvg6'] = moneyAvg6

    # 表7 工作经验-薪资水平对比
    sql = 'SELECT job_exp ,round(sum(job_money_avg)/count(*),2) from jobdata group by job_exp order by round(sum(job_money_avg)/count(*),2) '
    p1 = MysqlConnet(sql)
    results = p1.select()
    exp7 = []
    moneyAvg7 = []

    for i in results:
        exp7.append(i[0])
        moneyAvg7.append(i[1])
    context['exp7'] = exp7
    context['moneyAvg7'] = moneyAvg7

    # 表8 关键词词云图
    sql8 = "select job_name from jobdata "
    p1 = MysqlConnet(sql8)
    result = p1.select()

    string = ''
    for i in result:
        string = string + i[0].replace(',', '')
        string = string + ' '

    # jieba.load_userdict('./weal_dic.txt')  # 自定义词组
    string = string.title()  # 首字母大写
    word_weights = jieba.analyse.extract_tags(string, topK=50, withWeight=True)  # topK 前50个  withWeight返回权重

    word_list = []
    for i in word_weights:
        word = {}
        word['name'] = i[0]
        word['value'] = i[1]
        word['emphasis'] = {'textStyle': {'color': 'red'}}
        word_list.append(word)

    context['data8'] = word_list

    return render(request,"pandect.html",context=context)

# ******************************


# ***************V2.0修改版***************

# =============index =============
def index(request):
    return render(request,'index.html')

#================ 总体分析 ================
# 图1 城市职位需求 条形图
def job_city_num(request):
    # 表1 main1 各城市职位数
    context={}
    sql = 'select job_city ,count(*) from jobdata group by job_city'
    p1 = MysqlConnet(sql)
    results = p1.select()
    city1 = []
    data1 = []
    for i in results:
        city1.append(i[0])
        data1.append(i[1])
    context['city1'] = city1
    context['data1'] = data1
    return render(request,'pandect/pandect_job_city_num.html',context=context)

def job_keyword(request):
    context = {}
    # 表2 编程语言职位数
    sql = 'select keywords as "职位" ,count(*) as "职位数" from jobdata group by keywords'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li1 = []
    li2 = []
    for i in range(len(results)):
        li1.append(results[i][0])
        li2.append(results[i][1])
    context['name2'] = li1
    context['data2'] = li2
    return render(request,'pandect/pandect_job_keyword.html',context=context)

def job_exp(request):  # 工作经验分布
    context = {}
    # 表3 工作经验
    """ 饼图应该输入
        [
        {name:'',value:}
        ]
    """
    sql = 'select job_exp ,count(*) from jobdata group by job_exp order by count(*) DESC'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li = []
    for i in results:
        dic = {}
        dic['value'] = i[1]
        dic['name'] = i[0]
        li.append(dic)
    context['data3'] = li
    return render(request, 'pandect/pandect_job_exp.html', context=context)

def job_edu(request):  # 学历水平分布
    context = {}
    # 表4  学历水平
    # 这是工作学历统计的sql 饼图
    sql = 'select job_edu ,count(*) from jobdata group by job_edu order by count(*) DESC'
    p1 = MysqlConnet(sql)
    results = p1.select()
    li = []
    for i in results:
        dic = {}
        dic['value'] = i[1]
        dic['name'] = i[0]
        li.append(dic)
    context['data4'] = li
    return render(request, 'pandect/pandect_job_edu.html', context=context)

def job_city_money(request):  # 城市薪资水平
    context = {}
    # 表5 各城市薪资水平
    # 这是各城市薪资sql   floor 和 upper
    sql = 'SELECT job_city,round(sum(job_money_floor)/count(*)*job_money_month/12,2),round(sum(job_money_upper)/count(*)*job_money_month/12,2) FROM jobinfo.jobdata where job_money_floor != 0 group by job_city'
    p1 = MysqlConnet(sql)
    results = p1.select()
    city5 = []
    floor5 = []
    upper5 = []
    for i in results:
        city5.append(i[0])
        floor5.append(i[1])
        upper5.append(i[2])
    context['city5'] = city5
    context['floor5'] = floor5
    context['upper5'] = upper5
    return render(request,'pandect/pandect_job_city_money.html', context=context)

def job_edu_money(request):  # 学历-薪资关系
    context = {}
    # 表6 main6 学历-薪资水平对比
    # z这是对比学历和工资的关系  条形统计图
    sql = 'SELECT job_edu ,round(sum(job_money_avg)/count(*),2) from jobdata group by job_edu order by round(sum(job_money_avg)/count(*),2) '
    p1 = MysqlConnet(sql)
    results = p1.select()
    edu6 = []
    moneyAvg6 = []
    for i in results:
        edu6.append(i[0])
        moneyAvg6.append(i[1])
    context['edu6'] = edu6
    context['moneyAvg6'] = moneyAvg6
    return render(request, 'pandect/pandect_job_edu_money.html', context=context)

def job_exp_money(request):  # 7工作经验-薪资关系
    context = {}
    # 表7 工作经验-薪资水平对比
    sql = 'SELECT job_exp ,round(sum(job_money_avg)/count(*),2) from jobdata group by job_exp order by round(sum(job_money_avg)/count(*),2) '
    p1 = MysqlConnet(sql)
    results = p1.select()
    exp7 = []
    moneyAvg7 = []
    for i in results:
        exp7.append(i[0])
        moneyAvg7.append(i[1])
    context['exp7'] = exp7
    context['moneyAvg7'] = moneyAvg7
    return render(request, 'pandect/pandect_job_exp_money.html', context=context)

def job_wordcloud(request):  # 关键词词云图
    context = {}
    # 表8 关键词词云图
    sql8 = "select job_name from jobdata "
    p1 = MysqlConnet(sql8)
    result = p1.select()
    string = ''
    for i in result:
        string = string + i[0].replace(',', '')
        string = string + ' '
    # jieba.load_userdict('./weal_dic.txt')  # 自定义词组
    string = string.title()  # 首字母大写
    word_weights = jieba.analyse.extract_tags(string, topK=50, withWeight=True)  # topK 前50个  withWeight返回权重

    word_list = []
    for i in word_weights:
        word = {}
        word['name'] = i[0]
        word['value'] = i[1]
        word['emphasis'] = {'textStyle': {'color': 'red'}}
        word_list.append(word)

    context['data8'] = word_list
    return render(request, 'pandect/pandect_job_wordcloud.html', context=context)


#=========== 互联网行业分析=============
# 下面是编程语言及特定工作分类
class seed(object):
    def __init__(self,keyword):
        self.keyword=keyword
    def dataAnalyse(self):
        keyword = self.keyword  # 关键词  两种引号  实际上keyword =》 "C++"
        context = {}  # 数据传递

        # 1.各城市职位数  此为图一 数据后缀 1  柱形图
        sql1 = "select job_city ,count(*) from jobdata  where keywords = " + keyword + " group by job_city"
        p1 = MysqlConnet(sql1)
        results = p1.select()
        city1 = []  # 城市
        num1 = []  # 职位数
        for i in results:
            city1.append(i[0])
            num1.append(i[1])
        context['city1'] = city1
        context['num1'] = num1

        # 2.经验分布 饼图
        sql2 = 'select job_exp ,count(*) from jobdata  where keywords = ' + keyword + ' group by job_exp order by count(*) desc'
        p1 = MysqlConnet(sql2)
        results = p1.select()

        li = []
        for i in results:  # 饼图
            dic = {}
            dic['value'] = i[1]
            dic['name'] = i[0]
            li.append(dic)
        context['exp2'] = li

        # 3.学历分布
        sql3 = 'select job_edu ,count(*) from jobdata  where keywords = ' + keyword + ' group by job_edu'
        p1 = MysqlConnet(sql3)
        results = p1.select()

        li = []
        for i in results:  # 饼图
            dic = {}
            dic['value'] = i[1]
            dic['name'] = i[0]
            li.append(dic)
        context['edu3'] = li

        # 4.词云图
        sql4 = "select job_weal from jobdata where keywords = " + keyword
        p1 = MysqlConnet(sql4)
        result = p1.select()

        string = ''
        for i in result:
            string = string + i[0].replace(',', '')
            string = string + ' '

        jieba.load_userdict(r'E:\Python\02-爬虫\MyProject\analyse\weal_dic.txt')  # 自定义词组
        word_weights = jieba.analyse.extract_tags(string, topK=40, withWeight=True)  # topK 前50个  withWeight返回权重
        word_list = []
        for i in word_weights:
            word = {}
            word['name'] = i[0]
            word['value'] = i[1]
            word['emphasis'] = {'textStyle': {'color': 'red'}}

            word_list.append(word)

        context['data4'] = word_list
        # 5.经验/薪资

        sql = 'select data from edu_exp_money where keyword =' + keyword
        p1 = MysqlConnet(sql)
        results = p1.select()
        context['data5'] = results[0][0]
        # job_exps = ['"无经验"', '"经验不限"', '"1年以下"', '"1-3年"', '"3-5年"', '"5-10年"', '"10年以上"']
        # job_edus = ['"中专/中技"', '"学历不限"', '"大专"', '"本科"', '"硕士"', '"博士"']
        # data5 = []
        # # resu = [] # 存每种工作经验下数据
        # data5.append(['学历/薪资', '"中专/中技"', '"学历不限"', '"大专"', '"本科"', '"硕士"', '"博士"'])
        # for i in job_exps:
        #     li = [i]
        #
        #     for j in job_edus:
        #         sql = 'select job_edu,round(sum(job_money_avg)/count(*)*job_money_month/12,2) from jobdata  where keywords = ' + keyword + 'and job_exp = ' + i + 'and job_edu=' + j + ' group by job_edu'
        #         p1 = MysqlConnet(sql)
        #         results = p1.select()
        #
        #         try:
        #             li.append(results[0][1])
        #         except:
        #             li.append(0)
        #
        #     data5.append(li)
        # # data5.append(resu)
        # context['data5'] = data5

        context['keyword'] = keyword
        context['img_path'] = keyword.replace('"', '') + '.jpg'
        return context

def Java(request):
    keyword = '"Java"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request,'internet/internet.html',context = context)

def Python(request):
    keyword = '"Python"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def C_add_add(request):
    keyword = '"C++"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def PHP(request):
    keyword = '"PHP"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def NET(request):
    keyword = '".NET"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def Android(request):
    keyword = '"Android"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def AI(request):
    keyword = '"人工智能"'
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

def Algorithm(request):  # 这是算法工程师的
    keyword = '"算法工程师"'  # 关键词
    result = seed(keyword)
    context = result.dataAnalyse()
    return render(request, 'internet/internet.html', context=context)

# ========查询========

def seachs(request):
    if request.method == "POST":
        print("the POST method")
        concat = request.POST
        postBody = request.body
        print(concat)
        print(type(postBody))
        print(postBody)
    return render(request, '下拉列表2.html', locals())

def posts(request):
    if request.method == "POST":
        print("the POST method")
        concat = request.POST
        postBody = request.body
        print(concat)
        print(type(postBody))
        print(postBody)
        print('==============')
        print(concat['name'],concat['age'],concat['salary'],concat['city'])
    return render(request,'post传输数据.html')


def search2(request):
    if request.method == "POST":
        concat = request.POST

        job_business = "'" + concat['job_business'] + "'"  # 行业
        job_keyword = "'" + concat['job_keyword'] + "'" # 方向关键词
        job_city = "'" + concat['job_city'] + "'"   # 城市
        job_type = "'" + concat['job_type'] + "'"  # 类型
        job_edu = "'" + concat['job_edu'] + "'"  # 学历
        job_exp = "'" + concat['job_exp'] + "'"  # 经验
        if concat['job_business']=='' and concat['job_keyword'] == '' and concat['job_city'] == ''and concat['job_type']=='' and concat['job_edu']==''and concat['job_exp']:
            return render(request, 'search/search1.html')
        # print('===============')
        # print(concat['job_business'],concat['job_keyword'],concat['job_city'],concat['job_type'],concat['job_edu'],concat['job_exp'])

        #  ************************************
        # 表一 职业在不同城市薪资对比
        context = {}
        sql = 'SELECT job_city ,round(avg(job_money_floor),2) FROM jobinfo.jobdata '
        sign1 = False
        fil1 = ''
        if concat['job_keyword'] != '':
            if sign1:
                fil1 = fil1 + ' and '
            else:
                fil1 = 'where'
            fil1 = fil1 + ' keywords =' + job_keyword
            sign1 = True
        if concat['job_type'] != '':
            if sign1:
                fil1 = fil1 + ' and '
            else:
                fil1 = 'where'
            fil1 = fil1 + ' job_type =' + job_type
            sign1 = True
        if concat['job_edu'] != '':
            if sign1:
                fil1 = fil1 + ' and '
            else:
                fil1 = 'where'
            fil1 = fil1 + ' job_edu =' + job_edu
            sign1 = True
        if concat['job_exp'] != '':
            if sign1:
                fil1 = fil1 + ' and '
            else:
                fil1 = 'where'
            fil1 = fil1 + ' job_exp =' + job_exp
            sign1 = True
        sql = sql + fil1 +' group by job_city '
        print(sql)
        p1 = MysqlConnet(sql)
        results = p1.select()
        city1 = []
        data1 = []
        for i in results:
            city1.append(i[0])
            data1.append(i[1])
        context['city1'] = city1
        context['data1'] = data1

        # 表2 月份职位
        sql = 'SELECT month,count(*) FROM jobinfo.jobdata '
        sign2 = False
        fil2 = ''
        if concat['job_keyword'] != '':
            if sign2:
                fil2 = fil2 + ' and '
            else:
                fil2 = 'where'
            fil2 = fil2 + ' keywords =' + job_keyword
            sign2 = True
        if concat['job_type'] != '':
            if sign2:
                fil2 = fil2 + ' and '
            else:
                fil2 = 'where'
            fil2 = fil2 + ' job_type =' + job_type
            sign1 = True
        if concat['job_edu'] != '':
            if sign2:
                fil2 = fil2 + ' and '
            else:
                fil2= 'where'
            fil2 = fil2 + ' job_edu =' + job_edu
            sign2 = True
        if concat['job_exp'] != '':
            if sign2:
                fil2 = fil2 + ' and '
            else:
                fil2 = 'where'
            fil2 = fil2 + ' job_exp =' + job_exp
            sign2 = True
        sql = sql + fil2 + ' group by month '
        print(sql)
        p1 = MysqlConnet(sql)
        results = p1.select()
        month2 = []
        data2 = []
        for i in results:
            month2.append(i[0])
            data2.append(i[1])
        context['month2'] = month2
        context['data2'] = data2

        # 3.词云图
        sql3 = "select job_weal from jobdata where keywords = " + job_keyword
        p1 = MysqlConnet(sql3)
        result = p1.select()

        string = ''
        for i in result:
            string = string + i[0].replace(',', '')
            string = string + ' '

        jieba.load_userdict(r'E:\Python\02-爬虫\MyProject\analyse\weal_dic.txt')  # 自定义词组
        word_weights = jieba.analyse.extract_tags(string, topK=40, withWeight=True)  # topK 前50个  withWeight返回权重
        word_list = []
        for i in word_weights:
            word = {}
            word['name'] = i[0]
            word['value'] = i[1]
            word['emphasis'] = {'textStyle': {'color': 'red'}}

            word_list.append(word)

        context['data3'] = word_list
        # 4.经验/薪资

        sql = 'select data from edu_exp_money where keyword =' + job_keyword
        p1 = MysqlConnet(sql)
        results = p1.select()
        context['data4'] = results[0][0]

        return render(request, 'search/search2.html',context=context)  # 跳转

    return render(request, 'search/search2.html', locals())  # 返回搜索页2


# ==============反馈=============
def feedback(request):
    if request.method == "POST":
        concat = request.POST
        title = concat['title']
        cont = concat['cont']
        from django.core.mail import EmailMultiAlternatives

        subject, from_email, to = '反馈邮件', '3590746101@qq.com', '3590746101@qq.com'
        text_content = title
        html_content = cont
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return render(request,'feedback/feedback.html')
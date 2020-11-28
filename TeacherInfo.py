#教师信息管理
import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session,Blueprint
from sql.sqlite3 import *
import json
import time

#模块
teacher_api = Blueprint("teacher_api",__name__)

#查询教师授课表
@teacher_api.route('/teacherlist', methods=['POST', 'GET'])
def teacherlist():
    r = request.args.get('result', '')
    result,_ = GetSql2("select * from t_teacher_info")
    return render_template("man_teacher_cap.html", results=result, result=r)

#新增教师页面
@teacher_api.route('/add_teacher', methods=['POST', 'GET'])
def add_teacher():
    sql ="select * from t_department";
    r = request.args.get('result', '')
    result,_ = GetSql2(sql)
    print(result)
    return render_template("add_teacher_cap.html",result = result)

@teacher_api.route("/cha2",methods=['POST'])
def cha2():
    data = request.get_data().decode('utf-8')
    data = request.form.to_dict()
    strsql ="select * from t_teacher_info where teacher_name = '"+str(data["teacher_name"])+"'" 
    if data["teacher_name"]=="":
        strsql ="select * from t_teacher_info"
    print(data)
    result,_ = GetSql2(strsql)

    return render_template("man_teacher_cap.html", results=result)

@teacher_api.route("/deldata2",methods=['GET','POST'])
def deldata2():
    r = ''
    if request.method == 'POST':
        #是批量删除
        couids = request.form.getlist('couid')
        # couid是列表的形式，['12301+1+45601', '12302+1+45602']，用字典的方式获取数据
        ke = []
        flag = 0
        for couid in couids:
            #将数据库中的信息删除
            result1 = DelDataByIdOne("delete from t_teacher_info where teacher_num = '"+couid+"'")
            print(result1)
        result,_ = GetSql2("select * from t_teacher_info")
        return render_template("man_teacher_cap.html", results=result, result=r)
    # 根据id删除数据
    table = request.args.get('table','erro')
    database = request.args.get('database','erro')
    apath = table
    useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro'),'teacher_num':request.args.get('teacher_num','erro')},'teacher_num')
    result,_ = GetSql2("select * from t_teacher_info")
    print(result)
    return render_template("man_teacher_cap.html", results=result, result=r)

#添加教师信息
@teacher_api.route('/addteacher', methods=['POST', 'GET'])
def addteacher():
    if request.method == 'POST':
        #获取信息
        teacher_num = request.form.get('teacher_num')
        teacher_name = request.form.get('teacher_name')
        sex = request.form.get('sex')
        dep_num = request.form.get('dep_num')
        title = request.form.get('title')
        pwd = request.form.get('pwd')
        #将教师信息存储到数据库
        sql = "insert into t_teacher_info (teacher_num,teacher_name,sex,dep_num,title,pwd) values ('"+str(teacher_num)+"','"+str(teacher_name)+"','"+str(sex)+"','"+str(dep_num)+"','"+str(title)+"','"+str(pwd)+"') "
        resultadd = InsertDataV(sql) 
        print(resultadd)
        r = request.args.get('result', '')
        results,_ = GetSql2("select * from t_teacher_info")
        return render_template("man_teacher_cap.html", result=resultadd,results=results)
    else:
       return render_template("man_teacher_cap.html", result="添加失败")
#教师信息跳转修改页
@teacher_api.route("/up_teacher_cap2")
def up_teacher_cap2():
    x = request.args.get('teacher_num')
    result,_ = GetSql2("select * from t_teacher_info where teacher_num = "+str(x))

    sql ="select * from t_department";
    r = request.args.get('result', '')
    result1,_ = GetSql2(sql)
    print(result)
    return render_template("up_teacher_cap2.html",result=result,xisuo=result1)

#教师信息修改
@teacher_api.route("/updatatecher",methods=['POST'])
def updatatecher():
    if request.method == 'POST':
        #获取信息
        teacher_num = request.form.get('teacher_num')
        teacher_name = request.form.get('teacher_name')
        sex = request.form.get('sex')
        dep_num = request.form.get('dep_num')
        title = request.form.get('title')
        pwd = request.form.get('pwd')
        #将教师信息存储到数据库
        sql = "update t_teacher_info set teacher_name ='"+str(teacher_name)+"',sex ='"+str(sex)+"',dep_num ='"+str(dep_num)+"',title ='"+str(title)+"' ,pwd ='"+str(pwd)+"'  where teacher_num ='"+str(teacher_num)+"' "
        resultup = UpdatedataTwo(sql) 
        print(resultup)
        r = request.args.get('result', '')
        results,_ = GetSql2("select * from t_teacher_info")
        return render_template("man_teacher_cap.html", result=resultup,results=results)
    else:
       return render_template("man_teacher_cap.html", result="删除失败")


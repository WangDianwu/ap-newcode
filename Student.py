#学生信息管理
import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session,Blueprint
from sql.sqlite3 import *
import json
import time

#模块
student_api = Blueprint("student_api",__name__)

#查询学生信息表
@student_api.route('/studentlist', methods=['POST', 'GET'])
def studentlist():
    r = request.args.get('result', '')
    result,_ = GetSql2("select * from t_student_info")
    return render_template("man_student_cap.html", results=result, result=r)

#查询按钮
@student_api.route("/qstudent",methods=['POST'])
def qstudent():
    data = request.get_data().decode('utf-8')
    data = request.form.to_dict()
    strsql ="select * from t_student_info where student_name = '"+str(data["student_name"])+"'"
    if data["student_name"] =="":
        strsql="select * from t_student_info"
    print(data)
    result,_ = GetSql2( strsql)
    return render_template("man_student_cap.html", results=result)

@student_api.route('/add_student', methods=['POST', 'GET'])
def add_student():
    result1,_ = GetSql2("select * from t_specialty_info")
    result2,_ = GetSql2("select * from t_class_info")
    return render_template("add_student_cap.html", sp=result1, cl=result2)

@student_api.route("/add_studentdata",methods=['POST'])
def add_studentdata():
    #获取信息
    student_num = request.form.get('student_num')
    student_name = request.form.get('student_name')
    sex = request.form.get('sex')
    birth_date = request.form.get('birth_date')
    sp_num = request.form.get('sp_num')
    class_num = request.form.get('class_num')
    pwd = request.form.get('pwd')
    sql = "insert into t_student_info (student_num,student_name,sex,birth_date,sp_num,class_num,pwd) values ('"+str(student_num)+"','"+str(student_name)+"','"+str(sex)+"','"+str(birth_date)+"','"+str(sp_num)+"','"+str(class_num)+"','"+str(pwd)+"') "
    resultadd = InsertDataV(sql) 
    print(resultadd)

    #查询学生信息表
    result,_ = GetSql2("select * from t_student_info")
    print(result)

    return render_template("man_student_cap.html", results=result, result=resultadd)

#删除
@student_api.route("/deldata1",methods=['GET','POST'])
def deldata1():
    if request.method == 'POST':
        couids = request.form.getlist('couid')
        ke = []
        flag = 0
        for couid in couids:
            #将数据库中的信息删除
            result1 = DelDataByIdOne("delete from t_student_info where student_num = '"+couid+"'")
            print(result1)
        result,_ = GetSql2("select * from t_student_info")
        return render_template("man_student_cap.html", results=result)
    # 根据id删除数据
    table = request.args.get('table','erro')
    database = request.args.get('database','erro')
    apath = table
    result1= useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro'),'student_num':request.args.get('student_num','erro')},'student_num')
    result,_ = GetSql2("select * from t_student_info")
    print(result)
    return render_template("man_student_cap.html", results=result,result=result1)


@student_api.route("/add_student_cap2")
def add_student_cap2():
    x = request.args.get('student_num')
    result,_ = GetSql2("select * from t_student_info where student_num = "+str(x))
    result1,_ = GetSql2("select * from t_specialty_info")
    result2,_ = GetSql2("select * from t_class_info")
    return render_template("up_student_cap2.html",result=result, sp=result1, cl=result2)

# 根据id修改数据
@student_api.route("/updatedatastd",methods=['POST'])
def updatedatastd():
    student_num = request.form.get('student_num')
    student_name = request.form.get('student_name')
    sex = request.form.get('sex')
    birth_date = request.form.get('birth_date')
    sp_num = request.form.get('sp_num')
    class_num = request.form.get('class_num')
    pwd = request.form.get('pwd')

    sql = "update t_student_info set student_name ='"+str(student_name)+"',sex ='"+str(sex)+"',birth_date ='"+str(birth_date)+"',sp_num ='"+str(sp_num)+"' ,class_num ='"+str(class_num)+"' ,pwd ='"+str(pwd)+"'  where student_num ='"+str(student_num)+"' "
    resultup = UpdatedataTwo(sql) 
    print(resultup)

    #查询学生信息表
    result,_ = GetSql2("select * from t_student_info")
    print(result)

    return render_template("man_student_cap.html", results=result, result=resultup)



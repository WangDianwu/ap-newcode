import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session,Blueprint
from sql.sqlite3 import *
import json
import time

#模块
login_api = Blueprint("login_api",__name__)

@login_api.route('/')
def index():
    session.clear()
    return render_template('login_cap.html')

#登录信息处理界面，处理由'/'传送过来的表单信息
@login_api.route('/result', methods=['POST', 'GET'])   
def result():
    if request.method == 'POST':
        #用户名
        username = request.form.get('username') 
        #密码
        password = request.form.get('password')
        #登陆类型
        usertype = request.form.get('usertype')
        name = ''
        #学生
        if usertype == 'student':
            result, _ = GetSql2("select student_name from t_student_info where student_num = '"+username+"' and pwd = '"+password+"'")
        #教师
        if usertype == 'teacher':
            result, _ = GetSql2("select teacher_name from t_teacher_info where teacher_num = '"+username+"' and pwd = '"+password+"'")
        #管理员
        if usertype == 'admin':
            result, _ = GetSql2("select * from t_sys_info where sys_num = '"+username+"' and pwd = '"+password+"'")
        #登录成功，页面跳转到相应的功能页面
        if result: 
            name = result[0][0]
            if usertype == 'admin':
                return render_template("manager_cap.html", name=username)
            if usertype == 'teacher':
                return render_template("teacher_cap.html", name=name, bianhao=username)
            if usertype == 'student':
                return render_template("student_cap.html", name=name, xuehao=username)
        else:
            # 没整明白
            flash("用户名密码错误，请重新输入！")
            # 密码错误重定向到登录页面
            return redirect(url_for('index'))  

    else:
        # 重定向到登录页面
        return redirect(url_for('index'))


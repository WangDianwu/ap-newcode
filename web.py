import string

import xlrd as xlrd
from flask import Flask, redirect, url_for, request, Response, render_template, flash, session
from sql.sqlite3 import *
import json
import time
app = Flask(__name__)
app.secret_key = "jJInfdd4444dewp(f8e5ffkd*9&jfkl"      # flash的消息都存储在session，需要一个会话密匙，密匙随便输入就行，如果对保密性要求高的话，可以使用相关的密匙生成函数，不在细讲
@app.route('/updateCource', methods=['POST'])
def updateCource():
    #修改开设课程
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    tea = request.form.get('tea')
    num = request.form.get('num')
    kaike = request.form.get('kaike')
    didian = request.form.get('didian')
    zhou = request.form.get('zhou')
    xing = request.form.get('xing')
    jie = request.form.get('jie')
    opens = request.form.getlist('open')
    #将数据存储到数据库中
    data = dict(
        course_num=kehao,
        course_id=kexuhao,
        teacher_num=tea,
        teaching_max=num,
        open_date=kaike,
        class_addr=didian,
        weeks_count=zhou,
        week_num=xing,
        sections_num=jie
    )
    result1 = UpdatedataTwo("update t_teaching set teacher_num = '"+str(tea)+"', teaching_max = "+str(num)+", open_date = '"+str(kaike)+"', class_addr = '"+str(didian)+"', weeks_count='"+str(zhou)+"', week_num="+str(xing)+", sections_num="+str(jie)+" where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'")
    for o in opens:
        data1 = dict(course_num=kehao, course_id=kexuhao, class_num=o)
        UpdatedataTwo("update t_open_class set class_num = '"+str(o)+"' where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'")

    return redirect(url_for('course', result=result1))

@app.route('/luru', methods=['GET'])
def luru():
    #单个录入学生成绩界面
    #获取学生的学号,课程的课程编号和课序号
    xuehao = request.args.get('xuehao')
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    bianhao = request.args.get('bianhao')
    page = request.args.get('page')

    return render_template("luru_cap.html", xuehao=xuehao, kehao=kehao, kexuhao=kexuhao, bianhao=bianhao, page=page)

@app.route('/studentlist', methods=['POST', 'GET'])
def studentlist():
    r = request.args.get('result', '')
    #查询学生信息表
    result,_ = GetSql2("select * from student")
    print(result)

    return render_template("man_student_cap.html", results=result, result=r)
@app.route('/result', methods=['POST', 'GET'])   #登录信息处理界面，处理由'/'传送过来的表单信息
def result():
    #如果使用post方法传送过来的数据才验证
    if request.method == 'POST':
        #获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        shenfen = request.form.get('shenfen')
        #从数据库中验证信息是否正确
        name = ''
        if shenfen == '学生':
            result, _ = GetSql2("select student_name from t_student_info where student_num = '"+username+"' and pwd = '"+password+"'")
            name = result[0][0]
        if shenfen == '教师':
            result, _ = GetSql2("select teacher_name from t_teacher_info where teacher_num = '"+username+"' and pwd = '"+password+"'")
            name = result[0][0]
        if shenfen == '管理员':
            result, _ = GetSql2("select * from t_sys_info where sys_num = '"+username+"' and pwd = '"+password+"'")
        if result: #登录成功，页面跳转到相应的功能页面
            # return '登录成功'
            if shenfen == '管理员':
                return render_template("manager_cap.html", name=username)
            if shenfen == '教师':
                return render_template("teacher_cap.html", name=name, bianhao=username)
            if shenfen == '学生':
                return render_template("student_cap.html", name=name, xuehao=username)
        else:
            flash("您输入的用户名和密码有误，请重新输入！")
            return redirect(url_for('index'))  # 密码错误重定向到登录页面

    else:
        return redirect(url_for('index'))

@app.route('/add_teacher', methods=['POST', 'GET'])
def add_teacher():
    return render_template("add_teacher_cap.html")
@app.route('/tongxuan', methods=["GET"])
def into_tongxuan():
    #通选限选
    xuehao = request.args.get('xuehao')
    page = int(request.args.get('page', 1))  # 默认值为1
    alert = request.args.get('result', '')  # 默认值为空
    if page <= 0:
        page = 1
    # 设置每一页展示5行
    hang = 5
    # 查询未选的必修课，获取页数
    result, _ = GetSql2("select count(*) from t_course_info,t_teaching where t_course_info.course_num = t_teaching.course_num and course_type = '通选限选' and t_teaching.course_num not in (select course_num from t_student_Course where student_num = '" + xuehao + "')")
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    # 计算当前页数，查询该范围内的必修课
    current_page = page
    start_hang = (page - 1) * hang
    result, _ = GetSql2("select * from tongxuan where course_num not in (select course_num from t_student_Course where student_num = '" + xuehao + "') limit " + str(hang) + " offset " + str(start_hang) + "")
    # 根据result中的课程编号，获取开课班级
    for i in range(len(result)):
        sql = "select calss_name from t_open_class, t_class_info where t_class_info.class_num = t_open_class.class_num and course_num = '" + result[i][0] + "'"
        r1, _ = GetSql2(sql)
        result[i] = (result[i], r1)
    # 获取剩余人数
    return render_template("tongxuan_cap.html", xuehao=xuehao, results=result, page_num=page_num, current_page=current_page,
                           result_num=result_num, result=alert)


@app.route('/excel', methods=['GET'])
def excel():
    #进入Excel文件成绩批量录入界面
    #获取编号
    bianhao = request.args.get('bianhao')
    r = request.args.get('result', '')
    #查询教师所教授的课程
    result, _ = GetSql2("select t_teaching.course_num, course_id, course_name, credit, course_type from t_teaching, t_course_info where t_teaching.course_num = t_course_info.course_num and teacher_num = '"+str(bianhao)+"'")
    return render_template("excel_cap.html", bianhao=bianhao, results=result, result=r)

@app.route('/selectCourse', methods=['POST'])
def selectCourse():
    #查询开设课程
    r = request.args.get('result', '')
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    #查询该课程的开课信息
    # 查询教师授课表
    result, _ = GetSql2("select * from t_teaching where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'")
    # 查询开课班级表
    for i in range(len(result)):
        result1, _ = GetSql2("select calss_name from t_open_class, t_class_info where t_open_class.class_num = t_class_info.class_num and course_num = '" + str(
            result[i][0]) + "' and course_id = '" + str(result[i][1]) + "'")
        result[i] = (result[i], result1)
    return render_template("man_cou_cap.html", results=result, result=r)

@app.route('/self_info', methods=["GET"])
def self_info():
    #个人中心

    shenfen = request.args.get('shenfen')
    if shenfen == '学生':
        xuehao = request.args.get('xuehao')
        result, _ = GetSql2("select student_num,student_name,sex,birth_date,t_specialty_info.sp_name,t_class_info.calss_name from t_student_info,t_specialty_info,t_class_info where t_student_info.class_num = t_class_info.class_num and t_student_info.sp_num = t_specialty_info.sp_num and student_num = '" + xuehao + "'")
        return render_template("student_self_cap.html", student = result[0])
    if shenfen == '教师':
        bianhao = request.args.get('bianhao')
        result, _ = GetSql2("select t_teacher_info.teacher_num, teacher_name, sex, dep_name, title from t_teacher_info, t_department where t_teacher_info.dep_num = t_department.dep_num and t_teacher_info.teacher_num = '" + bianhao + "'")
        return render_template("teacher_self_cap.html", teacher=result[0])
    print(shenfen)
    if shenfen == None:
        bianhao = request.args.get('bianhao')
        result, _ = GetSql2("select sys_num, pwd  from t_sys_info where t_sys_info.sys_num = '" + bianhao + "'")
        return render_template("manager_self_cap.html", student=result[0])

@app.route('/teacherlist', methods=['POST', 'GET'])
def teacherlist():
    r = request.args.get('result', '')
    #查询教师授课表
    result,_ = GetSql2("select * from t_teacher_info")
    print(result)

    return render_template("man_teacher_cap.html", results=result, result=r)
@app.route('/stu_mark', methods=['POST', 'GET'])
def into_stu_mark():
    #学生查询成绩页面
    #根据学号查询出成绩单
    xuehao = request.args.get('xuehao')
    result = request.args.get('result', '')
    pingshi = int(request.args.get('pingshi', 0))
    kaoshi = int(request.args.get('kaoshi', 0))
    sql = "select t_student_Course.course_num, course_id, course_name, credit, course_type, achievement, achievement_exam from t_student_Course, t_course_info where t_student_Course.course_num = t_course_info.course_num and student_num = '"+xuehao+"' and achievement != 0 and achievement_exam!=0"
    r, _ = GetSql2(sql)

    return render_template("stu_cha_mark_cap.html", xuehao=xuehao, results=r, result=result, pingshi=pingshi, kaoshi=kaoshi)

@app.route('/piliang', methods=['GET'])
def piliang():
    #批量输入成绩
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    bianhao = request.args.get('bianhao')
    r = request.args.get('result', '')  # 默认值设为空
    #查询这门课的所有学生
    result, _ = GetSql2("select student_num, achievement, achievement_exam from t_student_Course where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'")

    return render_template("piliang_cap.html", results=result, result=r, kehao=kehao, kexuhao=kexuhao, bianhao=bianhao)

@app.route('/deleteCource', methods=['GET', 'POST'])
def deleteCource():
    #删除开设课程
    if request.method == 'GET':
        #是单独删除
        kehao = request.args.get('kehao')
        kexuhao = request.args.get('kexuhao')
        tea = request.args.get('tea')
        sql1 = "delete from t_teaching where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"' and teacher_num = '"+str(tea)+"'"
        result1 = DelDataByIdOne(sql1)
        sql2 = "delete from t_open_class where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"'"
        result2 = DelDataByIdOne(sql2)
        if result1 == '删除成功' and result2 == '删除成功':
            result = '删除成功'
        else:
            result = '删除失败'
        return redirect(url_for('course', result=result))
    else:
        #是批量删除
        couids = request.form.getlist('couid')
        # couid是列表的形式，['12301+1+45601', '12302+1+45602']，用字典的方式获取数据
        ke = []
        flag = 0
        for couid in couids:
            #第一个加号的位置
            index = couid.find('+')
            #第二个加号的位置
            index2 = couid.find('+', index+1)
            dic = {}
            dic['kehao'] = couid[:index]
            dic['kexuhao'] = couid[index + 1:index2]
            dic['tea'] = couid[index2+1:]
            #将数据库中的信息删除
            result1 = DelDataByIdOne("delete from t_teaching where course_num = '"+str(dic['kehao'])+"' and course_id = '"+str(dic['kexuhao'])+"' and teacher_num = '"+str(dic['tea'])+"'")
            result2 = DelDataByIdOne("delete from t_open_class where course_num = '"+str(dic['kehao'])+"' and course_id = '"+str(dic['kexuhao'])+"'")
            if result1 == '删除成功' and result2 == '删除成功':
                continue
            else:
                flag = 1
        if flag == 1:
            result = '删除失败'
        else:
            result = '删除成功'
        return redirect(url_for('course', result=result))

@app.route('/tea_stu', methods=['GET'])
def tea_stu():
    #查询选修该课程的学生名单
    bianhao = request.args.get('bianhao')
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    page = int(request.args.get('page', 1))  # 默认值为1
    if page <= 0:
        page = 1
    # 设置每一页展示5行
    hang = 5
    # 查询选修这门课程的所有学生
    sql1 = "select count(*) from t_student_Course where course_num = '" + kehao + "' and course_id = '" + kexuhao + "'"
    result, _ = GetSql2(sql1)
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    # 计算当前页数，查询该范围内的学生
    current_page = page
    start_hang = (page - 1) * hang
    sql = "select t_student_Course.student_num, student_name, sex, t_specialty_info.sp_name, t_class_info.calss_name from t_student_Course, t_student_info, t_specialty_info, t_class_info where t_student_Course.student_num = t_student_info.student_num and t_specialty_info.sp_num = t_student_info.sp_num and t_class_info.class_num = t_student_info.class_num and course_num = '" + kehao + "' and course_id = '" + kexuhao + "' limit " + str(
        hang) + " offset " + str(start_hang) + ""
    result, _ = GetSql2(sql)
    return render_template("tea_stu_cap.html", bianhao=bianhao, results=result, page_num=page_num,
                           current_page=current_page,
                           result_num=result_num, kehao=kehao, kexuhao=kexuhao)


@app.route('/stu_cha_mark', methods=['POST'])
def stu_cha_mark():
    #学生输入课程编号和课序号查询成绩
    #接受学号，课程编号，课序号
    xuehao = request.form.get('xuehao')
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    #检验是否是该学生所选课程，以及该课程是否已经发布成绩
    result = ""
    r, _ = GetSql2("select * from t_student_Course where student_num = '"+xuehao+"' and course_num = '"+kehao+"' and course_id = '"+kexuhao+"' and achievement != 0 and achievement_exam != 0")
    if len(r) == 0:
        result = "您未选修该课程或者该课程并未公布成绩！"
        return redirect(url_for('into_stu_mark', xuehao=xuehao, result=result))
    else:
        #获取平时成绩和考试成绩
        pingshi = r[0][3]
        kaoshi = r[0][4]
        return redirect(url_for('into_stu_mark', xuehao=xuehao, pingshi=pingshi, kaoshi=kaoshi))

@app.route('/home')
def home():
   return render_template('home_cap.html')

@app.route('/xuanke', methods=['POST', 'GET'])
def sel_cou():
    #选课
    if request.method == 'POST':
        #证明是form的整体提交，是批量选课
        #获取学号和批量课号和课序号
        xuehao = request.form.get('xuehao')
        couids = request.form.getlist('couid')
        #couid是列表的形式，['12301+1', '12302+1']，用字典的方式获取数据
        ke = []
        for couid in couids:
            index = couid.find('+')
            dic = {}
            dic['kehao'] = couid[:index]
            dic['kexuhao'] = couid[index+1:]
            ke.append(dic)
        #调用插入函数
        flag = 0
        error = []
        for k in ke:
            data = dict(student_num = xuehao, course_num = k['kehao'], course_id = k['kexuhao'])
            result = InsertData(data, "t_student_Course")
            if result == '选课成功':
                continue
            else:
                flag = 1
                error.append(k)
        if flag == 1:
            result = "您选择的"
            for e in error:
                result = result+"课程编号为{}、课序号为{}的课,".format(e['kehao'], e['kexuhao'])
            result = result + "选课失败！！"

        return redirect(url_for('into_bixiu', xuehao=xuehao, result=result))
    else:
        #证明是单独的选课
        xuehao = request.args.get('xuehao')
        kehao = request.args.get('kehao')
        kexuhao = request.args.get('kexuhao')
        data = dict(student_num = xuehao, course_num = kehao, course_id = kexuhao)
        result = InsertData(data, "t_student_Course")
        return redirect(url_for('into_bixiu', xuehao=xuehao, result=result))

@app.route('/')
def index():
    session.clear()
    return render_template('login_cap.html')

@app.route('/add_open', methods=['POST', 'GET'])
def add_open():
    #添加开设课程页面
    #把没有开课的课程编号传过去
    kehao, _ = GetSql2("select course_num from t_course_info where course_num not in (select course_num from t_teaching)")
    #查询所有的教师编号传过去
    tea, _ = GetSql2("select teacher_num from t_teacher_info")

    #查询所有的班级
    ban, _ = GetSql2("select class_num from class")

    return render_template("add_open_cap.html", kehao=kehao, tea=tea, ban=ban)

@app.route('/update_mima', methods=['POST'])
def update_password():
    #点击修改按钮，修改表中信息
    result = ""
    shenfen = request.form.get('shenfen')
    hao = request.form.get('hao')
    mima = request.form.get('mima')
    if shenfen == '学生':
        data = dict(student_num = hao, pwd = mima)
        result = UpdateData(data, "t_student_info")
        return render_template("mima_cap.html", shenfen=shenfen, hao=hao, result=result)
    if shenfen == '教师':
        data = dict(teacher_num = hao, pwd = mima)
        result = UpdateData(data, "t_teacher_info")
        return render_template("mima_cap.html", shenfen=shenfen, hao=hao, result=result)

    data = dict(sys_num = hao, pwd = mima)
    result = UpdateData(data, "t_sys_info")
    return render_template("manager_self_cap.html",  student=[hao,mima])

@app.route('/xiugai', methods=['GET'])
def xiugai():
    #单个修改学生成绩界面
    #获取学生的学号,课程的课程编号和课序号
    xuehao = request.args.get('xuehao')
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    bianhao = request.args.get('bianhao')
    page = request.args.get('page')
    #查询平时成绩和考试成绩
    result, _ = GetSql2("select achievement, achievement_exam from t_student_Course where student_num = '"+xuehao+"' and course_num = '"+kehao+"' and course_id = '"+kexuhao+"'")

    return render_template("xiugai_cap.html", xuehao=xuehao, kehao=kehao, kexuhao=kexuhao, bianhao=bianhao, page=page, result=result)


@app.route('/kechenglist', methods=['POST', 'GET'])
def kechenglist():
    r = request.args.get('result', '')
    #查询教师授课表
    result,_ = GetSql2("select * from t_course_info")
    print(result)

    return render_template("man_kecheng_cap.html", results=result, result=r)

@app.route('/luru_mark', methods=['POST'])
def luru_mark():
    #单个录入学生成绩
    xuehao = request.form.get('xuehao')
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    pingshi = request.form.get('pingshi')
    kaoshi = request.form.get('kaoshi')
    bianhao = request.form.get('bianhao')
    page = request.form.get('page')
    sql = "update t_student_Course set achievement = "+pingshi+", achievement_exam = "+kaoshi+" where student_num = '"+xuehao+"' and course_num = '"+kehao+"' and course_id = '"+kexuhao+"'"
    result = UpdateDataOne(sql)

    return redirect(url_for('tea_cha', bianhao=bianhao, result=result, page=page, kehao=kehao, kexuhao=kexuhao))

@app.route('/mima', methods=["GET"])
def password():
    #点击修改密码，将信息传递到修改密码界面
    shenfen = request.args.get('shenfen')
    if shenfen == '学生':
        xuehao = request.args.get('xuehao')
        return render_template("mima_cap.html", shenfen=shenfen, hao=xuehao)
    if shenfen == '教师':
        bianhao = request.args.get('bianhao')
        return render_template("mima_cap.html", shenfen=shenfen, hao=bianhao)

@app.route('/excel_mark', methods=['POST', 'GET'])
def excel_mark():
    #进入Excel文件成绩批量录入
    if request.method == 'POST':
        kehao = request.form.get('kehao')
        kexuhao = request.form.get('kexuhao')
        bianhao = request.form.get('bianhao')
        #获取文件
        file = request.files.get('file')
        f = file.read()  #文件内容
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        nrows = table.nrows  # 获取该sheet中的有效行数
        ncols = table.ncols  # 获取该sheet中的有效列数
        #excel文件的内容格式必须是学号，平时成绩，考试成绩
        list = []
        for i in range(nrows):
            rowlist = []
            for j in range(ncols):
                rowlist.append(table.cell_value(i, j))
            list.append(rowlist)
        del list[0]  # 删掉第一行，第一行获取的是文件的头
        #将数据存储到数据库中
        result = ''
        flag = 0
        for a in list:
            sql = "update t_student_Course set achievement = " + str(a[1]) + ", achievement_exam = " + str(a[2]) + " where student_num = '" + str(a[0]) + "' and course_num = '" + str(kehao) + "' and course_id = '" + str(kexuhao) + "'"
            r = UpdateDataOne(sql)
            if r == '成绩录入成功':
                continue
            else:
                flag = 1
                result = ' ' + result + '学号' + a[0]

        result = result + '的同学成绩录入失败，请检查！！'
        if flag == 0:
            return redirect(url_for('excel', bianhao=bianhao, result='成绩单导入成功，请点击成绩中心进行查看！'))
        else:
            return redirect(url_for('excel', bianhao=bianhao, result=result))
    else:
        bianhao = request.args.get('bianhao')
        return redirect(url_for('excel', bianhao=bianhao))

@app.route('/zhuanye', methods=["GET"])
def into_zhuanye():
    #专业限选
    xuehao = request.args.get('xuehao')
    page = int(request.args.get('page', 1))  # 默认值为1
    alert = request.args.get('result', '')  # 默认值为空
    if page <= 0:
        page = 1
    # 设置每一页展示5行
    hang = 5
    # 查询未选的必修课，获取页数
    result, _ = GetSql2("select count(*) from t_course_info,t_teaching where t_course_info.course_num = t_teaching.course_num and course_type = '专业限选' and t_teaching.course_num not in (select course_num from t_student_Course where student_num = '" + xuehao + "')")
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    # 计算当前页数，查询该范围内的必修课
    current_page = page
    start_hang = (page - 1) * hang
    result, _ = GetSql2("select * from zhuanye where course_num not in (select course_num from t_student_Course where student_num = '" + xuehao + "') limit " + str(hang) + " offset " + str(start_hang) + "")
    # 根据result中的课程编号，获取开课班级
    for i in range(len(result)):
        sql = "select calss_name from t_open_class, t_class_info where t_class_info.class_num = t_open_class.class_num and course_num = '" + result[i][0] + "'"
        r1, _ = GetSql2(sql)
        result[i] = (result[i], r1)
    # 获取剩余人数
    return render_template("zhuanye_cap.html", xuehao=xuehao, results=result, page_num=page_num, current_page=current_page,
                           result_num=result_num, result=alert)

@app.route('/bixiu', methods=["GET"])
def into_bixiu():
    #必修
    xuehao = request.args.get('xuehao')
    page = int(request.args.get('page', 1)) #默认值为1
    alert = request.args.get('result', '') #默认值为空
    if page <= 0:
        page = 1
    #设置每一页展示5行
    hang = 5
    #查询未选的必修课，获取页数
    result, _ = GetSql2("select count(*) from t_course_info,t_teaching where t_course_info.course_num = t_teaching.course_num and course_type = '必修' and t_teaching.course_num not in (select course_num from t_student_Course where student_num = '"+xuehao+"')")
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    #计算当前页数，查询该范围内的必修课
    current_page = page
    start_hang = (page - 1) * hang
    result, _ = GetSql2("select * from bixiu where course_num not in (select course_num from t_student_Course where student_num = '"+xuehao+"') limit "+str(hang)+" offset "+str(start_hang)+"")
    #根据result中的课程编号，获取开课班级
    for i in range(len(result)):
        sql = "select calss_name from t_open_class, t_class_info where t_class_info.class_num = t_open_class.class_num and course_num = '"+result[i][0]+"'"
        r1, _ = GetSql2(sql)
        result[i] = (result[i], r1)
    #获取剩余人数
    return render_template("bixiu_cap.html", xuehao=xuehao, results=result, page_num=page_num, current_page=current_page, result_num = result_num, result = alert)

@app.route('/course', methods=['POST', 'GET'])
def course():
    #将所有的教师授课信息显示出来
    r = request.args.get('result', '')
    #查询教师授课表
    result,_ = GetSql2("select * from t_teaching")
    #查询开课班级表
    for i in range(len(result)):
        result1, _ = GetSql2("select calss_name from t_open_class, t_class_info where t_open_class.class_num = t_class_info.class_num and course_num = '"+str(result[i][0])+"' and course_id = '"+str(result[i][1])+"'")
        result[i] = (result[i], result1)

    return render_template("man_cou_cap.html", results=result, result=r)
@app.route('/addCourse', methods=['POST', 'GET'])
def addCourse():
    #添加开设课程
    if request.method == 'POST':
        #获取信息
        kehao = request.form.get('kehao')
        kexuhao = request.form.get('kexuhao')
        tea = request.form.get('tea')
        num = request.form.get('num')
        kaike = request.form.get('kaike')
        didian = request.form.get('didian')
        zhou = request.form.get('zhou')
        xing = request.form.get('xing')
        jie = request.form.get('jie')
        opens = request.form.getlist('open')
        #将开课信息存储到数据库
        data = dict(
            course_num = kehao,
            course_id = kexuhao,
            teacher_num = tea,
            teaching_max = num,
            open_date = kaike,
            class_addr = didian,
            weeks_count =zhou,
            week_num = xing,
            sections_num = jie
        )
        result = InsertDataOne(data, "t_teaching")
        for o in opens:
            data1 = dict(course_num=kehao, course_id=kexuhao, class_num=o)
            InsertDataOne(data1, "t_open_class")

        return redirect(url_for('course', result=result))
    else:
        return redirect(url_for('add_open'))

@app.route('/xiugai_mark', methods=['POST'])
def xiugai_mark():
    # 单个修改学生成绩
    xuehao = request.form.get('xuehao')
    kehao = request.form.get('kehao')
    kexuhao = request.form.get('kexuhao')
    pingshi = request.form.get('pingshi')
    kaoshi = request.form.get('kaoshi')
    bianhao = request.form.get('bianhao')
    page = request.form.get('page')
    sql = "update t_student_Course set achievement = " + pingshi + ", achievement_exam = " + kaoshi + " where student_num = '" + xuehao + "' and course_num = '" + kehao + "' and course_id = '" + kexuhao + "'"
    result = UpdateDataOne(sql)

    return redirect(url_for('tea_cha', bianhao=bianhao, result=result, page=page, kehao=kehao, kexuhao=kexuhao))

@app.route('/tea_cha', methods=['GET'])
def tea_cha():
    #教师点击查询
    bianhao = request.args.get('bianhao')
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    page = int(request.args.get('page', 1))  # 默认值为1
    r = request.args.get('result', '') #默认值设为空
    if page <= 0:
        page = 1
    # 设置每一页展示5行
    hang = 5
    #查询选修这门课程的所有学生
    sql1 = "select count(*) from t_student_Course where course_num = '"+kehao+"' and course_id = '"+kexuhao+"'"
    result, _ = GetSql2(sql1)
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    # 计算当前页数，查询该范围内的学生
    current_page = page
    start_hang = (page - 1) * hang
    sql = "select t_student_Course.student_num, student_name, sex, t_specialty_info.sp_name, t_class_info.calss_name, achievement, achievement_exam from t_student_Course, t_student_info, t_specialty_info, t_class_info where t_student_Course.student_num = t_student_info.student_num and t_specialty_info.sp_num = t_student_info.sp_num and t_class_info.class_num = t_student_info.class_num and course_num = '"+kehao+"' and course_id = '"+kexuhao+"' limit " + str(hang) + " offset " + str(start_hang) + ""
    result, _ = GetSql2(sql)
    #计算出总成绩
    #判断平时成绩和考试成绩是否已经公布
    pingshi = ''
    kaoshi = ''
    zong = 0
    for i in range(len(result)):
        if result[i][5] is None:
            pingshi = '未公布'
        if result[i][6] is None:
            kaoshi = '未公布'
        if result[i][5] is not None and result[i][6] is not None:
            zong = int(int(result[i][5]) * 0.3 + int(result[i][6]) * 0.7)
        result[i] = (result[i], zong)

    return render_template("stu_mark_cap.html", bianhao=bianhao, results=result, page_num=page_num, current_page=current_page,
                           result_num=result_num, kehao=kehao, kexuhao=kexuhao, pingshi=pingshi, kaoshi=kaoshi, result=r, zong=zong)

@app.route('/tuike', methods=["GET"])
def into_tuike():
    #进入退课页面
    xuehao = request.args.get('xuehao')
    page = int(request.args.get('page', 1))  # 默认值为1
    alert = request.args.get('result', '')  # 默认值为空
    if page <= 0:
        page = 1
    # 设置每一页展示5行
    hang = 5
    #查询该学生已选的课程
    result, _ = GetSql2("select count(*) from t_student_Course where student_num = '"+xuehao+"'")
    result_num = result[0][0]
    page_num = int(int(result_num) / hang)
    if result_num % hang != 0:
        page_num = page_num + 1
    # 计算当前页数，查询该范围内的必修课
    current_page = page
    start_hang = (page - 1) * hang
    result, _ = GetSql2("select * from yixuan,t_student_Course where yixuan.course_num = t_student_Course.course_num and yixuan.course_id = t_student_Course.course_id and student_num = '"+xuehao+"' limit " + str(hang) + " offset " + str(start_hang) + "")
    # 根据result中的课程编号，获取开课班级
    for i in range(len(result)):
        sql = "select calss_name from t_open_class, t_class_info where t_class_info.class_num = t_open_class.class_num and course_num = '" + result[i][0] + "'"
        r1, _ = GetSql2(sql)
        result[i] = (result[i], r1)
    return render_template("tuike_cap.html", xuehao=xuehao, results=result, page_num=page_num, current_page=current_page,
                           result_num=result_num, result=alert)

@app.route('/updateCourcePage', methods=['GET'])
def updateCourcePage():
    #修改开设课程页面
    #将数据查询出来，传递给修改界面
    kehao = request.args.get('kehao')
    kexuhao = request.args.get('kexuhao')
    tea = request.args.get('tea')
    # 查询教师授课表
    result, _ = GetSql2("select * from t_teaching where course_num = '"+str(kehao)+"' and course_id = '"+str(kexuhao)+"' and teacher_num = '"+str(tea)+"'")
    # 查询开课班级表
    for i in range(len(result)):
        op = []
        result1, _ = GetSql2("select t_class_info.class_num from t_open_class, t_class_info where t_open_class.class_num = t_class_info.class_num and course_num = '" + str(
            result[i][0]) + "' and course_id = '" + str(result[i][1]) + "'")
        for r in result1:
            op.append(r[0])
        result[i] = (result[i], op)
    #将所有任课教师查询出来
    teachers, _ = GetSql2("select teacher_num from t_teacher_info")
    #将所有的班级查询出来
    bans,_ = GetSql2("select class_num from class")
    return render_template("updateCourcePage_cap.html", results=result[0], teachers=teachers, ban=bans)

@app.route('/tea_mark', methods=['GET'])
def tea_mark():
    #教师成绩查询页面
    #获取编号
    bianhao = request.args.get('bianhao')
    #查询教师所教授的课程
    result, _ = GetSql2("select t_teaching.course_num, course_id, course_name, credit, course_type from t_teaching, t_course_info where t_teaching.course_num = t_course_info.course_num and teacher_num = '"+bianhao+"'")

    return render_template("tea_cha_mark_cap.html", bianhao=bianhao, results=result)

@app.route('/t_teaching', methods=['GET'])
def t_teaching():
    #教师开课信息界面
    #获取编号
    bianhao = request.args.get('bianhao')
    #查询教师所教授的课程
    result, _ = GetSql2("select t_teaching.course_num, course_id, course_name, credit, course_type, open_date, class_addr, weeks_count, week_num, sections_num from t_teaching, t_course_info where t_teaching.course_num = t_course_info.course_num and teacher_num = '"+bianhao+"'")
    #查询选择该课程的学生人数
    for i in range(len(result)):
        num, _ = GetSql2("select count(*) from t_student_Course where course_num = '"+str(result[i][0])+"' and course_id = '"+str(result[i][1])+"'")
        result[i] = (result[i], num[0])

    return render_template("tea_cou_cap.html", bianhao=bianhao, results=result)

@app.route('/add_kecheng', methods=['POST', 'GET'])
def add_kecheng():
    return render_template("add_kecheng_cap.html")

@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    return render_template("add_student_cap.html")

@app.route('/tui_cou', methods=['POST', 'GET'])
def tui_cou():
    #退课
    if request.method == 'POST':
        #证明是form的整体提交，是批量退课
        #获取学号和批量课号和课序号
        xuehao = request.form.get('xuehao')
        couids = request.form.getlist('couid')
        #couid是列表的形式，['12301+1', '12302+1']，用字典的方式获取数据
        ke = []
        for couid in couids:
            index = couid.find('+')
            dic = {}
            dic['kehao'] = couid[:index]
            dic['kexuhao'] = couid[index+1:]
            ke.append(dic)
        #调用删除函数
        flag = 0
        error = []
        for k in ke:
            result = DelDataById("delete from t_student_Course where student_num = '"+xuehao+"' and course_num = '"+k['kehao']+"' and course_id = '"+k['kexuhao']+"'")
            if result == '退课成功':
                continue
            else:
                flag = 1
                error.append(k)
        if flag == 1:
            result = "您选择的"
            for e in error:
                result = result+"课程编号为{}、课序号为{}的课,".format(e['kehao'], e['kexuhao'])
            result = result + "退课失败！！"

        return redirect(url_for('into_tuike', xuehao=xuehao, result=result))
    else:
        #证明是单独的退课
        xuehao = request.args.get('xuehao')
        kehao = request.args.get('kehao')
        kexuhao = request.args.get('kexuhao')
        result = DelDataById("delete from t_student_Course where student_num = '"+xuehao+"' and course_num = '"+kehao+"' and course_id = '"+kexuhao+"'")
        return redirect(url_for('into_tuike', xuehao=xuehao, result=result))

@app.route("/add_student_cap2")
def add_student_cap2():
    x = request.args.get('学号')
    result,_ = GetSql2("select * from student where 学号 = "+str(x))
    return render_template("add_student_cap2.html",result=result)

@app.route("/updatedata",methods=['POST'])
def updatedata():
    # 根据id修改数据
    data = request.get_data().decode('utf-8')
    data = json.loads(data)
    useSqliteUpdate(data)
    return json.dumps({"msg":"保存成功"})


@app.route("/updatedata1",methods=['POST'])
def updatedata1():
    # 根据id修改数据
    data = request.get_data().decode('utf-8')
    print(data)
    data = request.form.to_dict()
    # data = json.loads(data)
    useSqliteUpdate(data,"学号")
    r = request.args.get('result', '')
    #查询学生信息表
    result,_ = GetSql2("select * from student")
    print(result)

    return render_template("man_student_cap.html", results=result, result=r)


@app.route("/deldata",methods=['GET'])
def deldata():
    # 根据id删除数据
    table = request.args.get('table','erro')
    database = request.args.get('database','erro')
    apath = table
    useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro')},'zi')
    return json.dumps({"msg":"删除成功"})

@app.route("/deldata1",methods=['GET','POST'])
def deldata1():
    if request.method == 'POST':
        #是批量删除
        couids = request.form.getlist('couid')
        # couid是列表的形式，['12301+1+45601', '12302+1+45602']，用字典的方式获取数据
        ke = []
        flag = 0
        for couid in couids:
            #将数据库中的信息删除
            result1 = DelDataByIdOne("delete from student where 学号 = '"+couid+"'")
            print(result1)
        result,_ = GetSql2("select * from student")
        return render_template("man_student_cap.html", results=result)
    # 根据id删除数据
    table = request.args.get('table','erro')
    database = request.args.get('database','erro')
    apath = table
    useSqliteDelete({"database":database,'table':table,"id":request.args.get('id','erro'),'学号':request.args.get('学号','erro')},'学号')
    result,_ = GetSql2("select * from student")
    print(result)
    return render_template("man_student_cap.html", results=result)


@app.route("/cha1",methods=['POST'])
def cha1():
    # 根据id删除数据
    data = request.get_data().decode('utf-8')
    data = request.form.to_dict()
    print(data)
    result,_ = GetSql2("select * from student where 姓名 = '"+str(data["姓名"])+"'"  )
    # print(result)
    # print(result)

    return render_template("man_student_cap.html", results=result)

@app.route("/savedata",methods=['POST'])
def savedata():
    # 上传数据
    data = request.get_data().decode('utf-8')
    data = request.form.to_dict()
    # data = json.loads(data)
    print(data)
    useSqliteInsert(data)
    # InsertDataOne(data, data["table"])

    return json.dumps({"msg":"保存成功"})
@app.route("/savedata1",methods=['POST'])
def savedata1():
    # 上传数据
    data = request.get_data().decode('utf-8')
    data = request.form.to_dict()
    # data = json.loads(data)
    print(data)
    useSqliteInsert(data)
    r = request.args.get('result', '')
    #查询学生信息表
    result,_ = GetSql2("select * from student")
    print(result)

    return render_template("man_student_cap.html", results=result, result=r)

@app.route("/getdata",methods=['GET'])
def getdata():
    # 获取每一行数据
    table = request.args.get('table','erro')
    database = request.args.get('database','erro')
    return json.dumps({"msg":"获取成功","data":useSqliteSelect(database,table)})


if __name__ == '__main__':
   app.run(debug = True,port=8081)
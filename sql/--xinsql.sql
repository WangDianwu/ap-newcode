--建表
--1.教师授课表
create table tea_cou(
课程编号 char(5),
课序号 int,
任课教师 char(5),
选课人数上限 int,
开课学期 char(9),
上课地点 nvarchar(20),
周数 varchar(5),
星期 int check(星期 > 0 and 星期 < 8),
节数 int check(节数 > 0 and 节数 < 7),
primary key(课程编号, 课序号)
);
create table t_teaching
(
course_num char(5),
course_id int,
teacher_num char(5),
teaching_max int,
open_date char(9),
class_addr nvarchar(20),
weeks_count varchar(5),
week_num int check(week_num > 0 and week_num < 8),
sections_num int check(sections_num > 0 and sections_num < 7),
primary key(course_num, course_id)
);
--2.开课班级表
create table open_cou(
课程编号 char(5),
课序号 int,
班级号 char(5),
primary key(课程编号, 课序号, 班级号)
);

create table  t_open_class(
course_num char(5),
course_id int,
class_num char(5),
primary key(course_num, course_id, class_num)  
)
--3.系所信息表
create table xisuo(
编号 char(5) primary key,
名称 nvarchar(20)
);

create table t_department(
dep_num char(5) primary key,
dep_name nvarchar(20)
);
--4.专业信息表
create table sdept(
编号 char(5) primary key,
名称 nvarchar(20),
所属系所 char(5)
);

create table t_specialty_info(
sp_num char(5) primary key,
sp_name nvarchar(20),
dep_num char(5)
);
--5.班级信息表
create table class(
班级号 char(5) primary key,
名称 nvarchar(20),
所属专业 char(5),
入学年份 int,
人数 int,
导员 char(5),
班长 char(12)
);

create table t_class_info(
class_num char(5) primary key,
calss_name nvarchar(20),
sp_num char(5),
entrance_date int,
person_num int,
counsellor_num char(5),
monitor_num char(12)
);
--6.教师信息表
create table teacher(
编号 char(5) primary key,
姓名 nvarchar(10),
性别 nchar(1) check(性别 in ('男', '女')),
所属系所 char(5),
职称 nvarchar(3) check(职称 in ('助教','讲师','副教授','教授')),
密码 char(16) check(length(密码) > 5 and length(密码) < 17)
);

create table t_teacher_info(
teacher_num char(5) primary key,
teacher_name nvarchar(10),
sex nchar(1) check(sex in ('男', '女')),
dep_num char(5),
title nvarchar(3) check(title in ('助教','讲师','副教授','教授')),
pwd char(16) check(length(pwd) > 5 and length(pwd) < 17)
);
--7.课程信息表
create table course(
课程编号 char(5) primary key,
名称 nvarchar(20),
总学时 int,
学分 int,
课程类别 nvarchar(4) check(课程类别 in ('必修','专业限选','通选限选'))
);

create table t_course_info(
course_num char(5) primary key,
course_name nvarchar(20),
total_hours int,
credit int,
course_type nvarchar(4) check(course_type in ('必修','专业限选','通选限选'))
);
--8.学生信息表
create table student(
学号 char(12) primary key,
姓名 nvarchar(10),
性别 nchar(1) check(性别 in ('男','女')),
出生日期 char(10),
专业 char(5),
班级号 char(5),
密码 char(16) check(length(密码) > 5 and length(密码) < 17)
);

create table t_student_info(
student_num char(12) primary key,
student_name nvarchar(10),
sex nchar(1) check(sex in ('男','女')),
birth_date char(10),
sp_num char(5),
class_num char(5),
pwd char(16) check(length(pwd) > 5 and length(pwd) < 17)
);
--9.管理员信息表
create table manager(
账号 char(5) primary key,
密码 char(16) check(length(密码) > 5 and length(密码) < 17),
类型 int check(类型 > -1 and 类型 < 2)
);

create table t_sys_info(
sys_num char(5) primary key,
pwd char(16) check(length(pwd) > 5 and length(pwd) < 17),
sys_type int check(sys_type > -1 and sys_type < 2)
);
--10.选课表
create table stu_cou(
学号 char(12),
课程编号 char(5),
课序号 int,
平时成绩 int,
考试成绩 int,
primary key(学号, 课程编号, 课序号)
);

create table t_student_Course(
student_num char(12),
course_num char(5),
course_id int,
achievement int,
achievement_exam int,
primary key(student_num, course_num, course_id)
);
--录入数据
--1.系所信息表
insert into t_department values('32101','计算机系');
insert into t_department values('32102','电子系');
insert into t_department values('32103','控制系');
insert into t_department values('32104','机械系');
--2.专业信息表
insert into t_specialty_info values('65401','计算机科学与技术','32101');
insert into t_specialty_info values('65402','软件工程','32101');
insert into t_specialty_info values('65403','数字媒体技术','32101');
insert into t_specialty_info values('65404','电子信息科学与技术','32102');
insert into t_specialty_info values('65405','通信工程','32102');
insert into t_specialty_info values('65406','测控技术与仪器','32102');
insert into t_specialty_info values('65407','自动化','32102');
insert into t_specialty_info values('65408','机械设计制造及其自动化','32103');
insert into t_specialty_info values('65409','材料成型与控制工程','32103');
--3.教师信息表
insert into t_teacher_info values('45601','张杰','男','32101','讲师','zhangjie');
insert into t_teacher_info values('45602','张三','男','32101','教授','zhangsan');
insert into t_teacher_info values('45603','赵一聪','女','32101','教授','zhaoyicong');
insert into t_teacher_info values('45604','何照','男','32101','副教授','hezhao');
insert into t_teacher_info values('45605','杨过','男','32101','讲师','yangguo');
insert into t_teacher_info values('45606','杨芙蓉','女','32101','副教授','yangfurong');
insert into t_teacher_info values('45607','薛洁','女','32101','讲师','xuejie');
insert into t_teacher_info values('45608','邹文琴','女','32101','教授','zouwenqin');
--4.学生信息表
insert into t_student_info values('201800800001','张明一','男','2000/1/2','65401','78901','zhangmingyi');
insert into t_student_info values('201800800002','张新安','男','2000/1/3','65401','78901','zhangxinan');
insert into t_student_info values('201800800003','王嘉尔','男','2000/2/25','65401','78901','wangjiaer');
insert into t_student_info values('201800800004','李静','女','2000/3/15','65401','78901','lijing');
insert into t_student_info values('201800800005','刘默','女','1999/12/19','65401','78901','liumo1');
insert into t_student_info values('201800800006','尚晨','男','1999/10/18','65401','78901','shangchen');
insert into t_student_info values('201800800007','秦玉玲','女','2000/5/5','65401','78901','qinyuling');
insert into t_student_info values('201800800008','邹文轩','S男','2000/6/6','65401','78901','zouwenxuan');
insert into t_student_info values('201800800009','肖潇','男','1999/8/8','65401','78901','xiaoxiao');
insert into t_student_info values('201800800010','李飞','男','1999/9/16','65402','78902','lifei1');
insert into t_student_info values('201800800011','王杰','男','2000/4/15','65402','78903','wangjie');
insert into t_student_info values('201800800012','薛子轩','男','1999/11/12','65403','78904','xuezixuan');
--5.班级信息表
insert into t_class_info values('78901','计算机科学与技术','65401','2018','50','45601','201800800001');
insert into t_class_info values('78902','软件工程一班','65402','2018','50','45602','201800800010');
insert into t_class_info values('78903','软件工程二班','65402','2018','50','45603','201800800011');
insert into t_class_info values('78904','数字媒体技术','65403','2018','50','45604','201800800012');
--6.课程信息表
insert into t_course_info values('12301','大学综合英语','120','4','必修');
insert into t_course_info values('12302','计算机引论','32','3','必修');
insert into t_course_info values('12303','web技术','16','3','专业限选');
insert into t_course_info values('12304','高等数学','80','4','必修');
insert into t_course_info values('12305','线性代数','32','4','必修');
insert into t_course_info values('12306','中西文化比较','32','2','通选限选');
insert into t_course_info values('12307','古代名句鉴赏','32','2','通选限选');
insert into t_course_info values('12308','思辨与创新','32','2','通选限选');
insert into t_course_info values('12309','清史','32','2','通选限选');
insert into t_course_info values('12310','java程序设计','80','3','专业限选');
insert into t_course_info values('12311','Linux应用','32','2','专业限选');
insert into t_course_info values('12312','面向对象技术','32','3','专业限选');
insert into t_course_info values('12313','高级程序设计语言','80','4','必修');
insert into t_course_info values('12314','离散数学','32','5','必修');
insert into t_course_info values('12315','马克思主义基本原理','60','5','必修');
insert into t_course_info values('12316','形势与政策','16','1','必修');
insert into t_course_info values('12317','电影鉴赏','32','2','通选限选');
insert into t_course_info values('12318','音乐鉴赏','32','2','通选限选');
insert into t_course_info values('12319','艺术鉴赏','32','2','通选限选');
insert into t_course_info values('12320','明史','32','2','通选限选');
insert into t_course_info values('12321','模式识别技术','48','3','专业限选');
insert into t_course_info values('12322','人工智能','48','3','专业限选');
insert into t_course_info values('12323','人机交互技术','48','3','专业限选');
--添加几个没有开课的课程
insert into t_course_info values('12324', '计算机网络', '120', '3', '必修');
insert into t_course_info values('12325', '数据结构', '120', '3', '必修');
--7.管理员信息表
insert into t_sys_info values('98701','123456','1');
insert into t_sys_info values('98702','123456','0');
--8.教师授课表
insert into t_teaching values('12301','1','45601','50','2019-2020','商学院101','1-18','1','2');
insert into t_teaching values('12301','2','45602','50','2019-2020','商学院102','1-18','1','2');
insert into t_teaching values('12302','1','45603','60','2019-2020','海洋学院502','1-18','2','1');
insert into t_teaching values('12303','1','45604','60','2019-2020','商学院201','1-18','2','3');
insert into t_teaching values('12304','1','45605','60','2019-2020','商学院202','1-18','3','1');
insert into t_teaching values('12305','1','45606','70','2019-2020','海洋学院503','1-18','3','2');
insert into t_teaching values('12306','1','45607','100','2019-2020','商学院101','5-12','4','5');
insert into t_teaching values('12307','1','45601','150','2019-2020','图西101','5-12','1','6');
insert into t_teaching values('12308','1','45602','120','2019-2020','图西102','5-12','2','5');
insert into t_teaching values('12309','1','45603','90','2019-2020','图西103','5-12','3','5');
insert into t_teaching values('12310','1','45604','60','2019-2020','商学院101','1-18','1','4');
insert into t_teaching values('12311','1','45605','60','2019-2020','海洋学院504','1-18','4','1');
insert into t_teaching values('12312','1','45606','60','2019-2020','图西201','1-18','2','3');
insert into t_teaching values('12313','1','45607','60','2019-2020','图西205','1-18','5','4');
insert into t_teaching values('12314','1','45601','60','2019-2020','图西205','1-18','2','2');
insert into t_teaching values('12315','1','45602','60','2019-2020','图西201','1-18','3','3');
insert into t_teaching values('12316','1','45603','60','2019-2020','商学院301','1-18','4','4');
insert into t_teaching values('12317','1','45604','100','2019-2020','商学院302','5-12','1','1');
insert into t_teaching values('12318','1','45605','100','2019-2020','商学院303','5-12','5','2');
insert into t_teaching values('12319','1','45606','100','2019-2020','商学院304','5-12','5','2');
insert into t_teaching values('12320','1','45607','70','2019-2020','商学院401','5-12','5','6');
insert into t_teaching values('12321','1','45608','70','2019-2020','商学院402','1-18','3','2');
insert into t_teaching values('12322','1','45607','60','2019-2020','商学院403','1-18','2','4');
insert into t_teaching values('12323','1','45608','70','2019-2020','商学院404','1-18','5','2');
--9.选课表
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
insert into stu_cou values('','','','','')
--10.开课班级
insert into t_open_class values('12301','1','78901');
insert into t_open_class values('12301','1','78904');
insert into t_open_class values('12301','2','78902');
insert into t_open_class values('12301','2','78903');
--获取未选修的必修课数目
select count(*) from course,t_teaching where t_course_info.course_num = t_teaching.course_num and
课程类别 = '必修' and t_teaching.course_num not in (select 课程编号 from stu_cou where 学号 = '')

--获取未选修的必修课
create view bixiu
as
    select t_teaching.course_num, 课序号, 名称, 课程类别, 姓名, 学分, 上课地点, 周数, 星期, 节数 from
    tea_cou, course, teacher where t_teaching.course_num = t_course_info.course_num and t_teacher_info.teacher_num = t_teaching.teacher_num
    and 课程类别 = '必修'
create view tongxuan
as
    select t_teaching.course_num, 课序号, 名称, 课程类别, 姓名, 学分, 上课地点, 周数, 星期, 节数 from
    tea_cou, course, teacher where t_teaching.course_num = t_course_info.course_num and t_teacher_info.teacher_num = t_teaching.teacher_num
    and 课程类别 = '通选限选'
create view zhuanye
as
    select t_teaching.course_num, 课序号, 名称, 课程类别, 姓名, 学分, 上课地点, 周数, 星期, 节数 from
    tea_cou, course, teacher where t_teaching.course_num = t_course_info.course_num and t_teacher_info.teacher_num = t_teaching.teacher_num
    and 课程类别 = '专业限选'

--查询已选的课程
select count(*) from stu_cou where 学号 = ''
create view yixuan
as
    select t_teaching.course_num, t_teaching.course_id, 名称, 课程类别, 姓名, 学分, 上课地点, 周数, 星期, 节数 from stu_cou, tea_cou, course, teacher
    where t_student_Course.course_num = t_teaching.course_num and t_student_Course.course_id = t_teaching.course_id and t_teaching.teacher_num = t_teacher_info.teacher_num and t_course_info.course_num
    = t_student_Course.course_num

--查询成绩单
select t_student_Course.course_num, 课序号, 名称, 学分, 课程类别, 平时成绩, 考试成绩 from stu_cou, course where t_student_Course.course_num = t_course_info.course_num where
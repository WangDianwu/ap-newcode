import sqlite3

# 增
def useSqliteInsert(dic):
    # print("进入插入")
    conn = sqlite3.connect(r'sql/'+dic["database"]+'.db')
    cursor = conn.cursor()
    string = ''
    string2 = ''
    string3 = ''
    arr3 = []
    string33 = ''
    for x in dic:
        if x=='database':
            continue
            pass
        if x=='table':
            continue
            pass
        if string == '':
            string = x + ' ' +'text'
            string2=x
            string3= '\''+str( dic[x])+'\''
            string33 = '?'
            pass
        else:
            string = string+', ' + x + ' ' +'text'
            string2 = string2+','+x
            string3 = string3+','+'\''+ str(dic[x])+'\''
            string33 = string33 + ',' + '?'
        arr3.append(dic[x])
        pass
    try:
        cursor.execute('create table if not exists '+dic["table"]+' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT , '+ string +')')
        # print('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
        string3 = string3.replace("'",'"')
        cursor.execute('insert into '+dic["table"]+' ('+string2+') values ('+string33+')',arr3)
    except:
        print("---------------error---------------")
        print('insert into '+dic["table"]+' ('+string2+') values ('+string3+')')
    cursor.close()
    conn.commit()
    conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
# 删
def useSqliteDelete(data,zi):
    conn = sqlite3.connect(r'sql/'+data['database']+'.db')
    conn.row_factory = dict_factory 
    cursor = conn.cursor()
    print('===========================')
    # print('DELETE  from ' + data["table"] + ' WHERE id=\'' + data["id"]+'\'')
    print('DELETE  from ' + data["table"] + ' WHERE '+zi+'= ?',[data[zi]])
    cursor.execute('DELETE  from ' + data["table"] + ' WHERE '+zi+'= ?',[data[zi]])

    cursor.close()
    conn.commit()
    conn.close()

# 查
def useSqliteSelect(database,table):
    conn = sqlite3.connect(r'sql/'+database+'.db')
    conn.row_factory = dict_factory 
    cursor = conn.cursor()
    cursor.execute('SELECT * from '+table)
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values

# 查
def useSqliteSelectByKey(dic):
    conn = sqlite3.connect(r'sql/'+dic['database']+'.db')
    conn.row_factory = dict_factory 
    cursor = conn.cursor()
    # print('SELECT * from '+table+' WHERE nickname = '+key)
    # print('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = '+str(dic["value"] )+'  limit '+str(dic["limit"])+' offset '+str(int(dic["offset"])*int(dic["limit"])))
    cursor.execute('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = \''+str(dic["value"] + '\''))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values

def useSqliteSelectByPage(dic):
    conn = sqlite3.connect(r'sql/'+dic['database']+'.db')
    conn.row_factory = dict_factory 
    cursor = conn.cursor()
    # print('SELECT * from '+table+' WHERE nickname = '+key)
    # print('SELECT * from '+dic["table"]+' WHERE '+ dic['key'] +' = '+str(dic["value"] )+'  limit '+str(dic["limit"])+' offset '+str(int(dic["offset"])*int(dic["limit"])))
    print('SELECT * from '+dic["table"] +' limit '+dic["pageSize"]+' offset '+str((int(dic["page"])-1)*int(dic["pageSize"])))
    cursor.execute('SELECT * from '+dic["table"] +' limit '+dic["pageSize"]+' offset '+str((int(dic["page"])-1)*int(dic["pageSize"])))
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return values

# 改
def useSqliteUpdate(dic,zi):
    conn = sqlite3.connect(r'sql/'+dic["database"]+'.db')
    cursor = conn.cursor()
    string3 = ''
    
    for x in dic:
        if x=='database':
            continue
            pass
        if x=='table':
            continue
            pass
        if x=='id':
            continue
            pass
        if string3 == '':
    
            string3= x +' = ' '\''+ str(dic[x])+'\''
            pass
        else:
        
            string3 = string3+' , '+  x +' = ' '\''+ str(dic[x])+'\''
        pass
    # cursor.execute('create table if not exists '+dic["key"]+' (id integer NOT NULL PRIMARY KEY AUTOINCREMENT , '+ string +')')
    astr = 'UPDATE '+dic["table"]+' SET '+string3+' WHERE '+zi+' = \''+str(dic[zi])+'\''
    print(astr)
    cursor.execute(astr)
    cursor.close()
    conn.commit()
    conn.close()

def OpenDatabase():
    database = "./sql/database.db"
    conn = sqlite3.connect(database)
    return conn

def GetSql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    fields = []
    for field in cur.description:
        fields.append(field[0])
    result = cur.fetchall()
    # for item in result:
    #     print(item)
    cur.close()
    return result, fields

def CloseDb(conn):
    conn.close()

def GetSql2(sql):
    conn = OpenDatabase()
    result, fields = GetSql(conn, sql)
    CloseDb(conn)
    return result, fields

def UpdateData(data, tablename):
    result = ""
    conn = OpenDatabase()
    values = []
    cusor = conn.cursor()
    idName = list(data)[0]
    for v in list(data)[1:]:
        values.append("%s='%s'" % (v, data[v]))
    sql = "update %s set %s where %s='%s'" % (tablename, ",".join(values), idName, data[idName])
    # print(sql)
    try:
        cusor.execute(sql)
        conn.commit()
        result = "修改成功"
    except Exception as e:
        conn.rollback()
        result = "修改失败"
    cusor.close()
    CloseDb(conn)
    return result

def InsertData(data, tablename):
    conn = OpenDatabase()
    values = []
    cusor = conn.cursor()
    fieldNames = list(data)
    for v in fieldNames:
        values.append(data[v])
    sql = "insert into  %s (%s) values( %s) " % (tablename, ",".join(fieldNames), ",".join(["?"] * len(fieldNames)))
    # print(sql)
    try:
        cusor.execute(sql, values)
        conn.commit()
        result = "选课成功"
    except Exception as e:
        conn.rollback()
        result = "选课失败"
    cusor.close()
    CloseDb(conn)
    return result

def DelDataById(sql):
    conn = OpenDatabase()
    cusor = conn.cursor()
    # print (sql)
    try:
        cusor.execute(sql)
        conn.commit()
        result = "退课成功"
    except Exception as e:
        conn.rollback()
        result = "退课失败"
    cusor.close()
    CloseDb(conn)
    return result

def UpdateDataOne(sql):
    result = ""
    conn = OpenDatabase()
    values = []
    cusor = conn.cursor()
    try:
        cusor.execute(sql)
        conn.commit()
        result = "成绩录入成功"
    except Exception as e:
        conn.rollback()
        result = "成绩录入失败"
    cusor.close()
    CloseDb(conn)
    return result

def InsertDataV(sql):
    conn = OpenDatabase()
    cusor = conn.cursor()
    print(sql)
    try:
        cusor.execute(sql)
        conn.commit()
        result = "添加成功"
    except Exception as e:
        conn.rollback()
        result = "添加失败"
    cusor.close()
    CloseDb(conn)
    return result

def InsertDataOne(data, tablename):
    conn = OpenDatabase()
    values = []
    cusor = conn.cursor()
    fieldNames = list(data)
    for v in fieldNames:
        values.append(data[v])
    sql = "insert into  %s (%s) values( %s) " % (tablename, ",".join(fieldNames), ",".join(["?"] * len(fieldNames)))
    # print(sql)
    try:
        cusor.execute(sql, values)
        conn.commit()
        result = "添加成功"
    except Exception as e:
        conn.rollback()
        result = "添加失败"
    cusor.close()
    CloseDb(conn)
    return result

def DelDataByIdOne(sql):
    conn = OpenDatabase()
    cusor = conn.cursor()
    try:
        cusor.execute(sql)
        conn.commit()
        result = "删除成功"
    except Exception as e:
        conn.rollback()
        result = "删除失败"
    cusor.close()
    CloseDb(conn)
    return result

def UpdatedataTwo(sql):
    result = ""
    conn = OpenDatabase()
    values = []
    cusor = conn.cursor()
    try:
        cusor.execute(sql)
        conn.commit()
        result = "修改成功"
    except Exception as e:
        conn.rollback()
        result = "修改失败"
    cusor.close()
    CloseDb(conn)
    return result
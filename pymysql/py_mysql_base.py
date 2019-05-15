#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
'''
mysql  pymysql  class
func 基于 pymysql 的数据可以交互类，支持事务提交和回滚，返回结果记录行数，和insert 的最新id
'''
import pymysql
CONNECT_TIMEOUT=100
conf = {'host':'localhost','port':3306,'user':'root','password':'root','timeout':CONNECT_TIMEOUT,'dbname':'guazi'}
class mysql_py():
    ## 定义构造方法，初始化参数
    def __init__(self):
        self.__conn = None
        self.__cursor = None
        self.lastrowid = None
        self.connect_timeout = conf['timeout']
        self.host = conf['host']
        self.port = conf['port']
        self.user = conf['user']
        self.password = conf['password']
        self.dbname = conf['dbname']
        self.rows_affected = 0


    ## 定义链接数据库
    def __init_conn(self):
        try:
            conn = pymysql.connect(host=self.host,port=int(self.port),user=self.user,passwd=self.password,db=self.dbname,charset="utf8")
        except pymysql.Warning as e:
            raise pymysql.Warning(e)
        self.__conn = conn

    # 定义 句柄
    def __init_cursor(self):
        if self.__conn:
            self.__cursor = self.__conn.cursor()

    def close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None

    ## 处理select 语句
    def exec_selectsql(self,sql,args=None,fecth=0):
        try:
            if self.__conn is None:
                self.__init_conn()
                self.__init_cursor()
            if self.__cursor is None:
                self.__init_cursor()
            self.__conn.autocommit = True
            self.__cursor.execute(sql,args)
            self.rows_affected=self.__cursor.rowcount
            if fecth == 1:
                results = self.__cursor.fetchone()
            else:
                results = self.__cursor.fetchall()
            return results
        except pymysql.Error as e:
            raise pymysql.Error(e)
        finally:
            if self.__conn:
                self.close()
    # 处理 dml 语句 delete update insert
    def exec_txsql(self,sql,args=None):
        try:
            if self.__conn is None:
                self.__init_conn()
                self.__init_cursor()
            if self.__cursor is None:
                self.__init_cursor()
            if isinstance(args,list): ## isinstance 用于判断变量类型
                self.rows_affected = self.__cursor.executemany(sql,args)
            else:
                self.rows_affected = self.__cursor.execute(sql,args)
            self.lastrowid = self.__cursor.lastrowid
            return self.rows_affected
        except pymysql.Error as e:
            raise pymysql.Error(e)
        finally:
            if self.__conn:
                self.close()


    # 动态拼接sql 调用 exec_txslq()方法执行操作
    def auto_joint_sql(self,table,data={},act="insert",where=None):
        if isinstance(data,dict):
            if act == "update":
                ## 更新操作
                # sql update table set a=%s,b=%s,c=%s where id=1
                field = ','.join('`' + k + '`=%s' for k in data.keys())
                argd = tuple(data.values())
                sql = "UPDATE "+table+ " SET "+field
                if where is not None:
                    argsw = tuple(where.values())
                    where = ' AND '.join('`' + k + '`=%s' for k in where.keys())
                    sql += " WHERE "+ where
                    args = argd + argsw
            else:
                ## 插入操作
                ## sql = insert into table value(%s,%s,%s)
                ## args = ('fdf',323,3434)
                ## exceture(sql,args)
                val = ('%s',)*len(data)
                val = ','.join(val)
                keys = list(data.keys())
                keys = ','.join(keys)

                sql = "INSERT INTO "+table+'('+keys +') VALUES('+val+')'

                args = tuple(data.values())

            return self.exec_txsql(sql,args)
        else:
            return "请输入字典数据"


    ## 提交事务
    def exex_commit(self):
        try:
            if self.__conn:
                self.__conn.commit()
        except pymysql.Error as e:
            raise pymysql.Error(e)
        finally:
            if self.__conn:
                self.close()

    ## 回滚操作
    def exec_rollback(self):
        try:
            if self.__conn:
                self.__conn.rollback()
        except pymysql.Error as e:
            raise pymysql.Error(e)
        finally:
            if self.__conn:
                self.close()


    # 获取插入记录最后的主键id
    def get_lastrowid(self):
        return self.lastrowid

    # 获取影响的行数
    def get_affectrows(self):
        return self.rows_affected
    # 实例销毁之后，自动提交
    def __del__(self):
        self.exex_commit()


# # 实例化类
#conn = mysql_py()
# # 查询sql
#sql = "select * from py_car_module order by id desc"
#args = None
#res = conn.exec_selectsql(sql,args)
#print(res)

# # 插入sql
# sql = "insert into emoloyee(first_name,last_name,age,sex,income) values(%s,%s,%s,%s,%s)"
# # 参数 插入1条用元组  插入多条用 列表
# args = [('efdf','efdef',65,'M',7676),('efdf','efdef',65,'M',7676)]

# res = conn.exec_txsql(sql,args)
# print(res)

# # 调用自动拼接sql
# #
#table="py_car_module"
# # 数据要用 字典
#data = {'parent_id': 0, 'module_name': '奥迪', 'url': 'https://www.guazi.com/sz/audi/#bread', 'level': 1, 'addtime': '2019-04-08 15:10:19'}
# # 数据要用 字典
# where = {'age':25,'sex':"L"}

#res = conn.auto_joint_sql(table,data)
#print(res)


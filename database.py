#!/usr/bin/env python
# coding: utf-8

# In[1]:


#本次实验环境为python 3.7,使用pymysql包
import pymysql as mdb
import re
import datetime


# In[2]:


#基本配置
config={
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'20000822lty666',
    'db':'supermarket',
    'charset':'utf8'
}

conn=mdb.connect(**config) #建立连接
cursor=conn.cursor()       #获取游标



class query:
    def __init__(self):
        #基本配置
        config={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'passwd':'20000822lty666',
            'db':'supermarket',
            'charset':'utf8'
            }

        conn=mdb.connect(**config) #建立连接
        #conn.autocommit(True)
        cursor=conn.cursor()       #获取游标
        sql='select * from salesperson'
        cursor.execute(sql)
        l=cursor.fetchall()
        self.low_sal=max(l,key=lambda x:x[2])[2]-2000 #售货员底薪
    
    
    def register(self):
        '''实现会员顾客或售货员的注册功能'''
        while True:
            reg=input("请输入想注册的角色：1（顾客会员） 2（售货员） q(退出)")
            if reg=='1':
                #输入信息
                customer_id=cursor.execute("select * from customer")+20183001 #自动生成会员卡号
                name=input("请输入您的姓名")
                year,month,day=tuple(map(int,input("请输入您生日的年月日").split()))
                birthdate=datetime.date(year,month,day)
             
                sql='INSERT INTO `supermarket`.`customer`(`customer_id`, `birthdate`, `name`) values(%d,\'%s\',\'%s\')'%(customer_id,birthdate,name)
                
                try:
                    cursor.execute(sql)
                    print("注册成功！")
                except:
                    print("未知错误！")
            elif reg=='2':
                work_id=cursor.execute("select * from salesperson")+1231#自动生成售货员工号
                name=input("请输入您的姓名")
                sal=self.low_sal
                
                sql='insert into salesperson(work_id,name,salary) values(%d,\'%s\',%f)'%(work_id,name,sal)
                try:
                    cursor.execute(sql)
                    print("注册成功！")
                except:
                    print("未知错误！")
            elif reg=='q'or reg=='Q':
                break
            else:
                print("无效输入！")
                
    def commodity_register(self):
        '''实现货物登记功能'''
        while True:
            name=input("请输入要要登记货物名称：(输入q退出)")
            if name=='q'or name=='Q':
                break
            cursor.execute("select name from commodity")
            name_lis=list(map(lambda x:x[0],cursor.fetchall()))
            
            if name in name_lis:
                #已有货物进行登记
                cursor.execute('select * from commodity where name=\'%s\''%name)
                commodity_id,quantity,unit_price=cursor.fetchone()[0:3]
                
                num=int(input("请输入要登记货物数量："))
                quantity+=num
                sql="UPDATE `supermarket`.`commodity` SET `quantity` = %d, `unit_price` = %f, `name` = '%s' WHERE `commodity_id` = %d;"%(quantity,unit_price,name,commodity_id)
                try:
                    cursor.execute(sql)
                    print("登记成功！")
                    cursor.execute("select * from commodity where name='%s'"%name)
                    print("目前该商品信息为：",cursor.fetchone())
                except:
                    print('error!')
            else:
                #新品货物进行登记
                commodity_id=cursor.execute("select * from commodity")+10001
                quantity=int(input("请输入要登记货物数量："))
                unit_price=float(input("请输入要登记货物单价："))
                sql='INSERT INTO `supermarket`.`commodity`(`commodity_id`, `quantity`,`unit_price`, `name`) values(%d,%d,%f,\'%s\')'%(commodity_id,quantity,unit_price,name)
                try:
                    cursor.execute(sql)
                    print("登记成功！")
                    cursor.execute("select * from commodity where name='%s'"%name)
                    print("目前该商品信息为：",cursor.fetchone())
                except:
                    print("error!")
                    
                    
    def create_index(self,table,name):
        '''创建table表 name字段上的索引'''
        index_name=input("您想创建的索引名")
        sql="create index %s on %s(%s);"%(index_name,table,name)
        print(sql)
        try:
            cursor.execute(sql)
            print('创建成功！')
        except:
            print("未知错误！")
        
    def get_customer(self,name='',customer_id=0,key_word='',birth_time_start=None,birth_time_end=None):
        '''查询会员顾客的个人信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有会员顾客信息
        sql='select * from customer'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[-1]!=name:
                flag=0
            if customer_id and row[0]!=customer_id:
                flag=0
            if key_word and key_word not in row[-1]:
                flag=0
            if birth_time_start and row[1].__lt__(birth_time_start):
                flag=0
            if birth_time_end and row[1].__gt__(birth_time_end):
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("用户姓名：%s,会员账号：%d,用户生日："%(i[2],i[0]),i[1])
    
    def get_salesperson(self,name='',key_word='',work_id=0,max_bonus=0):
        '''查询售货员的个人信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有售货员信息
        sql='select * from salesperson'
        cursor.execute(sql)
        l=cursor.fetchall()
        out=[]
        sal=max(l,key=lambda x:x[2])[2]-2000
        for row in l:
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[1]!=name:
                flag=0
            if work_id and row[0]!=work_id:
                flag=0
            if key_word and key_word not in row[1]:
                flag=0
            if max_bonus and (row[2]-sal)>max_bonus:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("售货员姓名：%s,售货员账号：%d,售货员奖金："%(i[1],i[0]),i[2]-sal)
            
    def get_commodity(self,name='',key_word='',commodity_id=0):
        '''查询库存商品的信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有商品信息
        sql='select * from commodity'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[-1]!=name:
                flag=0
            if commodity_id and row[0]!=commodity_id:
                flag=0
            if key_word and key_word not in row[-1]:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("商品名称：%s,商品编号：%d,商品单价：%f，商品数量：%d"%(i[-1],i[0],i[2],i[1]))    
        
    def get_commodity_place(self,commodity_id=0,shelf_id=0):
        '''查询库存商品的摆放信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有商品摆放信息
        sql='select * from commodity_place'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            if commodity_id and row[1]!=commodity_id:
                flag=0
            if shelf_id and shelf_id !=row[2]:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("商品位置：%s,商品编号：%d,货架编号：%d，商品数量：%d"%(i[0],i[1],i[2],i[3]))   
    
    def get_order(self,order_id=0,time_start=None,time_end=None,discount=1):
        '''查询所有订单的信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有订单信息
        sql='select * from order1'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            if order_id and row[0]!=order_id:
                flag=0
            if time_start and datetime.date(row[1].year,row[1].month,row[1].day).__lt__(time_start):
                flag=0
            if time_end and datetime.date(row[1].year,row[1].month,row[1].day).__gt__(time_end):
                flag=0
            if discount!=1 and row[3]!=discount:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print('订单信息：',i) 
            
    def get_popular_commodity(self,month=None,day=None,week=None):
        '''统计每日、每周、每月的畅销产品信息'''
        #统计某日
        if not week and month and day:
            sql_s='where month(order_time)=%d and day(order_time)=%d'%(month,day)
        #统计某月
        elif not week and month and not day:
            sql_s='where month(order_time)=%d'%month
        #统计某周
        elif week and month and day:
            sql_s='where order_time between \''+str(datetime.date(2020,month,day))+'\' and \''+str(datetime.date(2020,month,day)+datetime.timedelta(days=7))+'\''
        
        #将sql语句粘贴起来并运行
        s1='with totalorder(commodity_id,number)as        (select commodity_id,sum(number)        from order1'
        s2='group by commodity_id)        select commodity.name as daybest,unit_price,number        from totalorder,commodity        where totalorder.number=(select max(number) from totalorder)        and totalorder.commodity_id=commodity.commodity_id;'
        sql=s1+'\n'+sql_s+'\n'+s2
        
        #得到结果
        cursor.execute(sql)
        for i in cursor.fetchall():
            print("销量最好的产品为%s，单价为%f,销售数量为%d"%(i[0],i[1],i[2]))
    
    def get_best_salesperson(self,month=None,day=None,week=None):
        '''统计每日、每周、每月的销售冠军'''
        #统计某日
        if not week and month and day:
            sql_s='where month(order_time)=%d and day(order_time)=%d'%(month,day)
        #统计某月
        elif not week and month and not day:
            sql_s='where month(order_time)=%d'%month
        #统计某周
        elif week and month and day:
            sql_s='where order_time between \''+str(datetime.date(2020,month,day))+'\' and \''+str(datetime.date(2020,month,day)+datetime.timedelta(days=7))+'\''
        
        s1='with totalorder(commodity_id,number)as        (select commodity_id,sum(number)        from order1'

        s2='group by commodity_id)        select distinct salesperson.work_id,salesperson.name as daybest_person        from totalorder,salesperson,order1        where totalorder.number=(select max(number) from totalorder)        and order1.commodity_id=totalorder.commodity_id and order1.work_id=salesperson.work_id;'
        
        sql=s1+'\n'+sql_s+'\n'+s2
        #得到结果
        cursor.execute(sql)
        for i in cursor.fetchall():
            print("销售冠军是：%s，编号为：%d"%(i[1],i[0]))
    def update_salary(self):
        '''售货员的工资和按照底薪加上其销量排序，
        最高销量的售货员发单月最高奖金2000元，
        其余人员的工资=底薪 + 2000 * 1/排名；
        底薪为每月销售额总量的60%除以员工总数；'''
        
        sql1='''update salesperson 
        set salary=0.6*(select sum(consumption_price)from order1 where month(order_time)='3');'''
        sql2='''update salesperson
        set salary=salary/(select count(work_id) from (select * from salesperson) as x);'''

        sql3='''with month_three(work_id,totalsale) as(
        select work_id,sum(consumption_price)
        from order1
        where month(order_time)='3'
        group by work_id)
        ,
        ordered(work_id,ranks) as (
        select salesperson.work_id,rank() over(order by month_three.totalsale desc)
        from salesperson left outer join month_three
        on salesperson.work_id=month_three.work_id)


        update salesperson
        set salary=(select salary+2000/ordered.ranks
        from ordered
        where salesperson.work_id=ordered.work_id);'''
        
        #分条执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        for row in cursor.fetchall():
            print(row)
        
    
    def get_rank_salesperson(self):
        '''统计售货员的年收入排名'''
        sql1='''update salesperson 
        set salary=0.6*(select sum(consumption_price)from order1);'''
        sql2='''update salesperson
        set salary=salary/(select count(work_id) from (select * from salesperson) as x);'''

        sql3='''with month_all(work_id,totalsale) as(
        select work_id,sum(consumption_price)
        from order1
        group by work_id)
        ,
        ordered(work_id,ranks) as (
        select salesperson.work_id,rank() over(order by month_all.totalsale desc)
        from salesperson left outer join month_all
        on salesperson.work_id=month_all.work_id)


        update salesperson
        set salary=(select salary+2000/ordered.ranks
        from ordered
        where salesperson.work_id=ordered.work_id);'''
        sql4='''select name,salary,rank()
        over(order by salary desc)
        from salesperson;'''
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        for row in cursor.fetchall():
            print(row)
    
    def get_top_20(self,name):
        '''给定顾客清单，分析该清单内顾客的购买癖好，该清单内顾客的top-20购买商品'''
        
        sql1='''select number,commodity_id
        from order1 natural join customer
        where order1.customer_id=customer.customer_id and
        customer.name in'''
        sql2='order by number desc limit 20;'
        sql=sql1+'\n'+str(name)+'\n'+sql2
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)
    
    def get_top_20_zhang(self):
        '''分析张姓的顾客的top-20购买商品'''
        sql='''with data(name,number,commodity_id) as (select name,number,commodity_id
        from order1 natural join customer
        where order1.customer_id=customer.customer_id and
        name like '张_%'
        order by number desc limit 20)
        select data.name,number,commodity.name
        from data,commodity
        where data.commodity_id=commodity.commodity_id;'''
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)

            
#主函数
def main():
    q=query()
    while True:
        choice=input("请输入您想使用的功能： 1（用户注册） 2（货物登记） 3（创建索引）q（退出）")
        if choice=='1':
            q.register()
        elif choice=='2':
            q.commodity_register()
        elif choice=='3':
            table=input("请输入想要创建索引的表名")
            name=input("请选择字段名")
            q.create_index(table,name)
        elif choice=='q':
            break
        else:
            print('无效输入！')
main()
l=list(cursor.fetchall())


# In[13]:


class query:
    def __init__(self):
        #基本配置
        config={
            'host':'127.0.0.1',
            'port':3306,
            'user':'root',
            'passwd':'20000822lty666',
            'db':'supermarket',
            'charset':'utf8'
            }

        conn=mdb.connect(**config) #建立连接
        #conn.autocommit(True)
        cursor=conn.cursor()       #获取游标
        sql='select * from salesperson'
        cursor.execute(sql)
        l=cursor.fetchall()
        self.low_sal=max(l,key=lambda x:x[2])[2]-2000 #售货员底薪
    
    
    def register(self):
        '''实现会员顾客或售货员的注册功能'''
        while True:
            reg=input("请输入想注册的角色：1（顾客会员） 2（售货员） q(退出)")
            if reg=='1':
                #输入信息
                customer_id=cursor.execute("select * from customer")+20183001 #自动生成会员卡号
                name=input("请输入您的姓名")
                year,month,day=tuple(map(int,input("请输入您生日的年月日").split()))
                birthdate=datetime.date(year,month,day)
             
                sql='INSERT INTO `supermarket`.`customer`(`customer_id`, `birthdate`, `name`) values(%d,\'%s\',\'%s\')'%(customer_id,birthdate,name)
                
                try:
                    cursor.execute(sql)
                    print("注册成功！")
                except:
                    print("未知错误！")
            elif reg=='2':
                work_id=cursor.execute("select * from salesperson")+1231#自动生成售货员工号
                name=input("请输入您的姓名")
                sal=self.low_sal
                
                sql='insert into salesperson(work_id,name,salary) values(%d,\'%s\',%f)'%(work_id,name,sal)
                try:
                    cursor.execute(sql)
                    print("注册成功！")
                except:
                    print("未知错误！")
            elif reg=='q'or reg=='Q':
                break
            else:
                print("无效输入！")
                
    def commodity_register(self):
        '''实现货物登记功能'''
        while True:
            name=input("请输入要要登记货物名称：(输入q退出)")
            if name=='q'or name=='Q':
                break
            cursor.execute("select name from commodity")
            name_lis=list(map(lambda x:x[0],cursor.fetchall()))
            
            if name in name_lis:
                #已有货物进行登记
                cursor.execute('select * from commodity where name=\'%s\''%name)
                commodity_id,quantity,unit_price=cursor.fetchone()[0:3]
                
                num=int(input("请输入要登记货物数量："))
                quantity+=num
                sql="UPDATE `supermarket`.`commodity` SET `quantity` = %d, `unit_price` = %f, `name` = '%s' WHERE `commodity_id` = %d;"%(quantity,unit_price,name,commodity_id)
                try:
                    cursor.execute(sql)
                    print("登记成功！")
                    cursor.execute("select * from commodity where name='%s'"%name)
                    print("目前该商品信息为：",cursor.fetchone())
                except:
                    print('error!')
            else:
                #新品货物进行登记
                commodity_id=cursor.execute("select * from commodity")+10001
                quantity=int(input("请输入要登记货物数量："))
                unit_price=float(input("请输入要登记货物单价："))
                sql='INSERT INTO `supermarket`.`commodity`(`commodity_id`, `quantity`,`unit_price`, `name`) values(%d,%d,%f,\'%s\')'%(commodity_id,quantity,unit_price,name)
                try:
                    cursor.execute(sql)
                    print("登记成功！")
                    cursor.execute("select * from commodity where name='%s'"%name)
                    print("目前该商品信息为：",cursor.fetchone())
                except:
                    print("error!")
                    
                    
    def create_index(self,table,name):
        '''创建table表 name字段上的索引'''
        index_name=input("您想创建的索引名")
        sql="create index %s on %s(%s);"%(index_name,table,name)
        print(sql)
        try:
            cursor.execute(sql)
            print('创建成功！')
        except:
            print("未知错误！")
        
    def get_customer(self,name='',customer_id=0,key_word='',birth_time_start=None,birth_time_end=None):
        '''查询会员顾客的个人信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有会员顾客信息
        sql='select * from customer'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[-1]!=name:
                flag=0
            if customer_id and row[0]!=customer_id:
                flag=0
            if key_word and key_word not in row[-1]:
                flag=0
            if birth_time_start and row[1].__lt__(birth_time_start):
                flag=0
            if birth_time_end and row[1].__gt__(birth_time_end):
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("用户姓名：%s,会员账号：%d,用户生日："%(i[2],i[0]),i[1])
    
    def get_salesperson(self,name='',key_word='',work_id=0,max_bonus=0):
        '''查询售货员的个人信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有售货员信息
        sql='select * from salesperson'
        cursor.execute(sql)
        l=cursor.fetchall()
        out=[]
        sal=max(l,key=lambda x:x[2])[2]-2000
        for row in l:
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[1]!=name:
                flag=0
            if work_id and row[0]!=work_id:
                flag=0
            if key_word and key_word not in row[1]:
                flag=0
            if max_bonus and (row[2]-sal)>max_bonus:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("售货员姓名：%s,售货员账号：%d,售货员奖金："%(i[1],i[0]),i[2]-sal)
            
    def get_commodity(self,name='',key_word='',commodity_id=0):
        '''查询库存商品的信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有商品信息
        sql='select * from commodity'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            
            if name and row[-1]!=name:
                flag=0
            if commodity_id and row[0]!=commodity_id:
                flag=0
            if key_word and key_word not in row[-1]:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("商品名称：%s,商品编号：%d,商品单价：%f，商品数量：%d"%(i[-1],i[0],i[2],i[1]))    
        
    def get_commodity_place(self,commodity_id=0,shelf_id=0):
        '''查询库存商品的摆放信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有商品摆放信息
        sql='select * from commodity_place'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            if commodity_id and row[1]!=commodity_id:
                flag=0
            if shelf_id and shelf_id !=row[2]:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print("商品位置：%s,商品编号：%d,货架编号：%d，商品数量：%d"%(i[0],i[1],i[2],i[3]))   
    
    def get_order(self,order_id=0,time_start=None,time_end=None,discount=1):
        '''查询所有订单的信息，如需指定查找范围，可在函数中指定参数'''
        #首先获取所有订单信息
        sql='select * from order1'
        cursor.execute(sql)
        
        out=[]
        for row in cursor.fetchall():
            #设置查询条件，如满足所有需求，则保留
            flag=1
            if order_id and row[0]!=order_id:
                flag=0
            if time_start and datetime.date(row[1].year,row[1].month,row[1].day).__lt__(time_start):
                flag=0
            if time_end and datetime.date(row[1].year,row[1].month,row[1].day).__gt__(time_end):
                flag=0
            if discount!=1 and row[3]!=discount:
                flag=0
            if flag:
                out.append(row)
        if not out:
            print('无查询结果！')
        for i in out:
            print('订单信息：',i) 
            
    def get_popular_commodity(self,month=None,day=None,week=None):
        '''统计每日、每周、每月的畅销产品信息'''
        #统计某日
        if not week and month and day:
            sql_s='where month(order_time)=%d and day(order_time)=%d'%(month,day)
        #统计某月
        elif not week and month and not day:
            sql_s='where month(order_time)=%d'%month
        #统计某周
        elif week and month and day:
            sql_s='where order_time between \''+str(datetime.date(2020,month,day))+'\' and \''+str(datetime.date(2020,month,day)+datetime.timedelta(days=7))+'\''
        
        #将sql语句粘贴起来并运行
        s1='with totalorder(commodity_id,number)as        (select commodity_id,sum(number)        from order1'
        s2='group by commodity_id)        select commodity.name as daybest,unit_price,number        from totalorder,commodity        where totalorder.number=(select max(number) from totalorder)        and totalorder.commodity_id=commodity.commodity_id;'
        sql=s1+'\n'+sql_s+'\n'+s2
        
        #得到结果
        cursor.execute(sql)
        for i in cursor.fetchall():
            print("销量最好的产品为%s，单价为%f,销售数量为%d"%(i[0],i[1],i[2]))
    
    def get_best_salesperson(self,month=None,day=None,week=None):
        '''统计每日、每周、每月的销售冠军'''
        #统计某日
        if not week and month and day:
            sql_s='where month(order_time)=%d and day(order_time)=%d'%(month,day)
        #统计某月
        elif not week and month and not day:
            sql_s='where month(order_time)=%d'%month
        #统计某周
        elif week and month and day:
            sql_s='where order_time between \''+str(datetime.date(2020,month,day))+'\' and \''+str(datetime.date(2020,month,day)+datetime.timedelta(days=7))+'\''
        
        s1='with totalorder(commodity_id,number)as        (select commodity_id,sum(number)        from order1'

        s2='group by commodity_id)        select distinct salesperson.work_id,salesperson.name as daybest_person        from totalorder,salesperson,order1        where totalorder.number=(select max(number) from totalorder)        and order1.commodity_id=totalorder.commodity_id and order1.work_id=salesperson.work_id;'
        
        sql=s1+'\n'+sql_s+'\n'+s2
        #得到结果
        cursor.execute(sql)
        for i in cursor.fetchall():
            print("销售冠军是：%s，编号为：%d"%(i[1],i[0]))
    def update_salary(self):
        '''售货员的工资和按照底薪加上其销量排序，
        最高销量的售货员发单月最高奖金2000元，
        其余人员的工资=底薪 + 2000 * 1/排名；
        底薪为每月销售额总量的60%除以员工总数；'''
        
        sql1='''update salesperson 
        set salary=0.6*(select sum(consumption_price)from order1 where month(order_time)='3');'''
        sql2='''update salesperson
        set salary=salary/(select count(work_id) from (select * from salesperson) as x);'''

        sql3='''with month_three(work_id,totalsale) as(
        select work_id,sum(consumption_price)
        from order1
        where month(order_time)='3'
        group by work_id)
        ,
        ordered(work_id,ranks) as (
        select salesperson.work_id,rank() over(order by month_three.totalsale desc)
        from salesperson left outer join month_three
        on salesperson.work_id=month_three.work_id)


        update salesperson
        set salary=(select salary+2000/ordered.ranks
        from ordered
        where salesperson.work_id=ordered.work_id);'''
        
        #分条执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        for row in cursor.fetchall():
            print(row)
        
    
    def get_rank_salesperson(self):
        '''统计售货员的年收入排名'''
        sql1='''update salesperson 
        set salary=0.6*(select sum(consumption_price)from order1);'''
        sql2='''update salesperson
        set salary=salary/(select count(work_id) from (select * from salesperson) as x);'''

        sql3='''with month_all(work_id,totalsale) as(
        select work_id,sum(consumption_price)
        from order1
        group by work_id)
        ,
        ordered(work_id,ranks) as (
        select salesperson.work_id,rank() over(order by month_all.totalsale desc)
        from salesperson left outer join month_all
        on salesperson.work_id=month_all.work_id)


        update salesperson
        set salary=(select salary+2000/ordered.ranks
        from ordered
        where salesperson.work_id=ordered.work_id);'''
        sql4='''select name,salary,rank()
        over(order by salary desc)
        from salesperson;'''
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        for row in cursor.fetchall():
            print(row)
    
    def get_top_20(self,name):
        '''给定顾客清单，分析该清单内顾客的购买癖好，该清单内顾客的top-20购买商品'''
        
        sql1='''select number,commodity_id
        from order1 natural join customer
        where order1.customer_id=customer.customer_id and
        customer.name in'''
        sql2='order by number desc limit 20;'
        sql=sql1+'\n'+str(name)+'\n'+sql2
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)
    
    def get_top_20_zhang(self):
        '''分析张姓的顾客的top-20购买商品'''
        sql='''with data(name,number,commodity_id) as (select name,number,commodity_id
        from order1 natural join customer
        where order1.customer_id=customer.customer_id and
        name like '张_%'
        order by number desc limit 20)
        select data.name,number,commodity.name
        from data,commodity
        where data.commodity_id=commodity.commodity_id;'''
        
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)

            
#主函数
def main():
    q=query()
    while True:
        choice=input("请输入您想使用的功能： 1（用户注册） 2（货物登记） 3（创建索引）q（退出）")
        if choice=='1':
            q.register()
        elif choice=='2':
            q.commodity_register()
        elif choice=='3':
            table=input("请输入想要创建索引的表名")
            name=input("请选择字段名")
            q.create_index(table,name)
        elif choice=='q':
            break
        else:
            print('无效输入！')
main()


# In[ ]:





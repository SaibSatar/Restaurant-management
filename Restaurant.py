from tkinter import*
import os
import sqlite3
from subprocess import call
from tkinter import messagebox
import tkinter as TK
 

# اگر فانکشنی داخل کلاس نوشته شود،به آن متد میگویندو باید سلف برای آنها نوشته شود
#اگر متغیری داخل کلاس باشد به آن اتربیوت میگویند
#برای استفاده از کلاس باید برای آن شی بسازیم
# منظور از * تمامی ستونهای یک پایگاه است

#region کلاس دیتابیس
class database:
    def __init__(self,db):# اینیت برای انتقال دیتابیس به اتربیوت است 
      self.__dbs_db=db # برای دیتابیس یک اتربیوت دلخواه میسازیم و متغیر دیتابیس را  داخل اتربویت میریزیم
      self.connection=sqlite3.connect(db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("""
                             CREATE TABLE IF NOT EXISTS [table_menu](
                             [ID] INT PRIMARY KEY NOT NULL UNIQUE, 
                             [Name] NVARCHAR(50) NOT NULL UNIQUE, 
                             [price] INT NOT NULL,
                             [Is_food] BOOL NOT NULL)WITHOUT ROWID; 
                             """) 
      self.cursor.execute("""
                               CREATE TABLE IF NOT EXISTS [table_reciepts]
                               (
                               [reciept_id] INT NOT NULL,
                               [menu_id] INT NOT NULL REFERENCES [table_menu] ([ID]), 
                               [count] INT,
                               [price]INT
                                  ); 
                               """)
      self.cursor.execute("""
                                CREATE VIEW IF NOT EXISTS view_menu_reciepts AS
                                SELECT table_reciepts.reciept_id,table_reciepts.menu_id,table_menu.Name,table_reciepts.price,table_reciepts.count,
                                (table_reciepts.count * table_reciepts.price) AS sum
                                FROM table_menu
                                INNER JOIN table_reciepts ON table_menu.ID == table_reciepts.menu_id
                               """)#درواقع تمام چیزی که باید داخل لیست باکس نمایش دهیم ویو است                                                                    
                            
      self.connection.commit()
      self.connection.close()#برای کمتر شدن حافظه کانکشن رو میبندیم
    
    def inserts(self,id,name,price,Is_food):
      self.connection=sqlite3.connect(self.__dbs_db)#یک کانکشن بر روی این دیتابیس باز کن
      self.cursor=self.connection.cursor()
      self.cursor.execute("INSERT INTO table_menu VALUES(?,?,?,?) " , (id,name,price,Is_food))#مقادیری که بهت میدم رو داخل تیبل منو بریز
      self.connection.commit()

    def get_menu_item(self,Is_food):#مقادیر منو را دریافت کن بر اساس ایزفود
       self.connection=sqlite3.connect(self.__dbs_db)
       self.cursor=self.connection.cursor()
       self.cursor.execute("SELECT * FROM table_menu WHERE Is_food=?",(Is_food,))#برای غذاها تورو و برای نوشیدنی ها فالس بر میگرداند
       result=self.cursor.fetchall()#چون تغیری روی دیتابیس انجام نمیدهیم که دائمی باشد از فچآل استفاده میکنیم
       return result

    def get_max_res_id(self):#متدی که بزرگترین آیدی تیبل رسیپتس را میگیرد 
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("SELECT MAX (reciept_id) FROM table_reciepts")
      result=self.cursor.fetchall()#چون تغیری روی دیتابیس انجام نمیدهیم که دائمی باشد از فچآل استفاده میکنیم
      return result

    def get_menu_item_by_name(self,item_name):#اطلاعات هر آیتم را میگیرد
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('SELECT * FROM table_menu WHERE name=?',(item_name,))
      result=self.cursor.fetchall()
      return result
    
    def insert_into_reciept(self,reciept_id,menu_id,count,price):# اطلاعات غذا من جمله قیمت را وارد تیبل رزیپتس میکند
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("INSERT INTO table_reciepts VALUES(?,?,?,?)",(reciept_id,menu_id,count,price))
      self.connection.commit()
      self.connection.close()
    
    def get_reciept_by_recieptid_menuid(self,reciept_id,menu_id):#صورتحسابهارا با توجه به آیدی صورتحساب و آیدی منو برمیگرداند
       self.connection=sqlite3.connect(self.__dbs_db)
       self.cursor=self.connection.cursor()
       self.cursor.execute("SELECT * FROM table_reciepts WHERE reciept_id=? and menu_id=?",(reciept_id,menu_id))
       result=self.cursor.fetchall()
       return result
    
    def increase_count(self,reciept_id,menu_id):# کانت را یکی یکی افزایش میدهد با توجه به آیدی صورتحساب و  آیدی منو
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('UPDATE table_reciepts SET count=count+1 WHERE reciept_id=? and menu_id=?',(reciept_id,menu_id))
      self.connection.commit()
      self.connection.close()
    
    def get_reciepts(self,reciept_id):#اطلاعات ویو را بر اساس آیدی صورتحساب برمیگرداند
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('SELECT * FROM view_menu_reciepts WHERE reciept_id=?',(reciept_id,))#وقتی میگیم تمامی ستون هارو برگردان یعنی تمامی اطلاعات رو برگردان
      result=self.cursor.fetchall()
      return result 
    
    def delete_item(self,reciept_id,menu_id):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('DELETE FROM table_reciepts WHERE reciept_id=? and menu_id=?',(reciept_id,menu_id))
      self.connection.commit()
      self.connection.close()
    
    def add_food_drink(self,reciept_id,menu_id):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('UPDATE table_reciepts SET count=count+1 WHERE reciept_id=? and menu_id=?',(reciept_id,menu_id))
      self.connection.commit()
      self.connection.close()
    
    def minus_item(self,reciept_id,menu_id):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('UPDATE table_reciepts SET count=count-1 WHERE reciept_id=? and menu_id=? and count>0' ,(reciept_id,menu_id))
      self.cursor.execute("DELETE FROM table_reciepts WHERE reciept_id=? and menu_id=? and count=0",(reciept_id,menu_id))
      self.connection.commit()
      self.connection.close()

    


      
      
#endregion 
      
#region وارد کردن دیتابیس
if os.path.isfile('restaurant.db')==FALSE:#اگر دیتابیس از قبل ساخته شده بود با این کد دیگر برنامه ارور نمیدهد
  db=database('restaurant.db') # شی کلاس را میسازیم
  db.inserts(1,'چلومرغ',22000,True) # متد اینسرت را ران میکند
  db.inserts(2,'چلوکباب کوبیده',33000,True)
  db.inserts(3,'چلوکباب مرغ',11000,True)
  db.inserts(4,'جوجه کباب با استخوان',20000,True)
  db.inserts(5,'جوجه کباب بدون استخوان',12000,False)
  db.inserts(6,'چلوخورشت فسنجان',10000,False)
  db.inserts(7,'چلوخورشت مرغ',13000,False)
  db.inserts(8,'چلوخورشت سبزی',33000,True)
  db.inserts(9,'چلوخورشت قیمه',11000,True)
  db.inserts(10,'چلوخورشت کرفس',20000,True)
  db.inserts(11,'چلوخورشت بادمجان',12000,False)
  db.inserts(12,'چلوخورشت لوبیا سبز',10000,False)
  db.inserts(13,'سبزی پلو با ماهی',13000,False)
  db.inserts(14,'باقالی پلو با ران',33000,True)
  db.inserts(15,'عدس پلو',11000,True)
  db.inserts(16,'ماش پلو',20000,True)
  db.inserts(17,'لوبیا پلو',12000,False)
  db.inserts(18,'نوشابه خانواده پپسی',10000,False)
  db.inserts(19,'نوشابه خانواده کولا',13000,False)
  db.inserts(20,'سون خانواده',33000,True)
  db.inserts(21,'دوغ گازدار خانواده',11000,True)
  db.inserts(22,'دوغ بدون گاز خانواده',20000,True)
  db.inserts(23,'دوغ محلی خانواده',12000,False)
  db.inserts(24,'دوغ آبعلی',10000,False)
  db.inserts(25,'نوشابه کوچک',13000,False)
  db.inserts(26,'فانتازا قوطی',33000,True)
  db.inserts(27,'کولا قوطی',11000,True)
  db.inserts(28,'پپسی قوطی',20000,True)
  db.inserts(29,'لیمونات شیشه ای',12000,False)
  db.inserts(30,'پپسی شیشه ای زرد',10000,False)
  db.inserts(31,'پپسی شیشه ای مشکی',13000,False)
  db.inserts(32,'ماشایر هلویی',33000,True)
  db.inserts(33,'ماشیر لیمویی',11000,True)
  
  
else:
  db=database('restaurant.db')#اگر دیتابیس را پاک کردیم دوباره میسازد
 #endregion 





#region تنظیمات کینتر
window=Tk()
window.grid_columnconfigure(0,weight=2)#پیکربندی ستونی= ستون 1 با اندیس 0 وزنی معادل 2 دارد
window.grid_columnconfigure(1,weight=3)
window.grid_rowconfigure(0,weight=1)#پیکربندی سطری=سطر 1 با اندیس 0 وزنی معادل 1 دارد
window.state('zoomed')#کینتر بصورت زوم شده باز میشود 
window.title('نرم افزار مدریت')
width=window.winfo_screenwidth()# پهنای اسکرین را بدست میاورد
heigh=window.winfo_screenheight()#طول اسکرین را بدست میاورد 
window.geometry('%dx%d'%(10,12))#به اندازه اسکرین مانیتور پنجره کینتر را باز میکند
#endregion


#region فرم دهی کینتر
soorat_label=LabelFrame(window,text='صورتحساب',bg='Powder blue',font=('Bnazanin',20,"bold"))
soorat_label.grid(row=0,column=0,sticky='nesw',padx=5,pady=5)
soorat_label.grid_columnconfigure(0,weight=1)#  اگر پیکربندی نکنیم،سایز اینترای ها کوچکتر میشود
soorat_label.grid_rowconfigure(1,weight=1)
entr_soorat=Entry(soorat_label,width=10,justify='center',font=('Bnazanin',20,'bold'),bd=20)#bd=3D model
entr_soorat.grid(row=0,column=0,sticky='nsew',padx=10,pady=10)

max_reciepts_num=db.get_max_res_id()#متد بزرگترین آیدی صورتحساب را ران میکند
#print(max_reciepts_num)=None[(None),]

if max_reciepts_num[0][0]==None:
  max_reciepts_num=0
  
else:
  max_reciepts_num=int(max_reciepts_num [0][0])

max_reciepts_num=int(max_reciepts_num)
max_reciepts_num+=1

entr_soorat.insert(0,max_reciepts_num)

list_soorat=Listbox(soorat_label,font=('Bnazanin',20,'bold'))
list_soorat.grid(row=1,column=0,sticky='nsew',padx=10,pady=10)
list_soorat.configure(justify=CENTER)

def enter_key(key):
  try:
    reciept_id=int(entr_soorat.get())
    load_reciepts(reciept_id)
  except:
    list_soorat.delete(0,'end')
  

entr_soorat.bind('<KeyRelease>',enter_key)

def load_reciepts(reciept_id):
  list_soorat.delete(0,'end')
  reciepts=db.get_reciepts(reciept_id)#اطلاعات ویو رو میگیره
  for reciept in reciepts:#پیمایش میکند (بعبارتی تمامی آیتم های داخل متغیر رو به نمایش درمیاورد)
    list_soorat.insert(0,("%s-%s-%s-%s-%s") %(reciept[1],reciept[2],reciept[3],reciept[4],reciept[5]))
    #menu_id,name,price,count,sum
  




#endregion

listbox_button=LabelFrame(soorat_label,bg='Powder blue',text='calculate',font='bold')#لیبل فریم ایجاد شده که داخلش کلید است 
listbox_button.grid(row=2,column=0,sticky='nsew',padx=10,pady=10)
listbox_button.grid_columnconfigure(0,weight=1)
listbox_button.grid_columnconfigure(1,weight=1)
listbox_button.grid_columnconfigure(2,weight=1)
listbox_button.grid_columnconfigure(3,weight=1)

def delete_line():
  reciept_id=int(entr_soorat.get())
  menu=(list_soorat.get(ACTIVE))
  menu_id=menu.split('-')[0]
  db.delete_item(reciept_id,menu_id)
  load_reciepts(reciept_id)


delet_button=Button(listbox_button,text='حذف سطر',font=('Bnazanin',20,'bold'),command=delete_line)
delet_button.grid(row=0,column=0)


def new_fac():
  list_soorat.delete(0,'end')
  max_num=db.get_max_res_id()
  
  if max_num[0][0]==None:
    max_num=0

  else:
     max_num=int(max_num[0][0])

  max_num+=1
  entr_soorat.delete(0,'end')
  entr_soorat.insert(0,max_reciepts_num)

sum_button=Button(listbox_button,text='فاکتور جدید',font=('Bnazanin',20,'bold'),command=new_fac)
sum_button.grid(row=0,column=1)

def add_plus():
  reciept_id=int(entr_soorat.get())
  menu=(list_soorat.get(ACTIVE))
  menu_id=menu.split('-')[0]
  db.add_food_drink(reciept_id,menu_id)
  load_reciepts(reciept_id)


plus_button=Button(listbox_button,text='+',font=('Bnazanin',20,'bold'),command=add_plus)
plus_button.grid(row=0,column=2)

def minus():
  reciept_id=int(entr_soorat.get())
  menu=(list_soorat.get(ACTIVE))
  menu_id=menu.split('-')[0]
  db.minus_item(reciept_id,menu_id)
  load_reciepts(reciept_id)


dig_button=Button(listbox_button,text='-',font=('Bnazanin',20,'bold'),command=minus)
dig_button.grid(row=0,column=3)






menu_label=LabelFrame(window,text='منوی نوشیدنی و غذا',bg='Powderblue',font=('Bnazanin',20,"bold"))
menu_label.grid(row=0,column=1,sticky='nsew',padx=5,pady=5)

menu_label.grid_columnconfigure(0,weight=1)
menu_label.grid_columnconfigure(1,weight=1)
menu_label.grid_rowconfigure(0,weight=1)

soda_frame=LabelFrame(menu_label,text='نوشیدنی',bg='Powder blue',font='bold')
soda_frame.grid(row=0,column=0,sticky='nesw')

food_frame=LabelFrame(menu_label,text='غذاها',bg='powder blue',font='bold')
food_frame.grid(row=0,column=1,sticky='nsew')
soda_frame.grid_columnconfigure(0,weight=1)
soda_frame.grid_rowconfigure(0,weight=1)
food_frame.grid_columnconfigure(0,weight=1)
food_frame.grid_rowconfigure(0,weight=1)

list_box_drink=Listbox(soda_frame,font=('Bnazanin',20,'bold'))
list_box_drink.grid(sticky='nsew')#تمام فضای سلولی که هستی رو بگیر
list_box_drink.configure(justify=LEFT)

def add_drink(event):#اگر ایونت نباشد هم کار میکند
  item_name=db.get_menu_item_by_name(list_box_drink.get(ACTIVE))#نامی که قراره از داخل لیست باکس ارسال گردد
  menu_id=item_name[0][0]
  drink_name=item_name[0][1]
  price=item_name[0][2]
  reciepts_id=int(entr_soorat.get())
  result=db.get_reciept_by_recieptid_menuid(reciepts_id,menu_id)#بررسی میکنیم برای آیدی های صورتحساب و منو ثبتی انجام شده است یا خیر
  if len(result)==0:
    db.insert_into_reciept(reciepts_id,menu_id,1,price)
  else:
    db.increase_count(reciepts_id,menu_id)
  
  load_reciepts(reciepts_id)

  
 
  
  
list_box_drink.bind('<Double-Button>',add_drink)
list_box_food=Listbox(food_frame,font=('Bnazanin',20,'bold'))
list_box_food.grid(sticky='nsew')


def add_food(event):#اگر ایونت نباشد هم کار میکند
 item_name=db.get_menu_item_by_name(list_box_food.get(ACTIVE))#نامی که قراره از داخل لیست باکس ارسال گردد
 menu_id=item_name[0][0]
 drink_name=item_name[0][1]
 price=item_name[0][2]
 reciepts_id=int(entr_soorat.get())
 result=db.get_reciept_by_recieptid_menuid(reciepts_id,menu_id)#بررسی میکنیم برای آیدی های صورتحساب و منو ثبتی انجام شده است یا خیر
 if len(result)==0:
  db.insert_into_reciept(reciepts_id,menu_id,1,price)
 else:
  db.increase_count(reciepts_id,menu_id)
 load_reciepts(reciepts_id)
  


  
  
list_box_food.bind('<Double-Button>',add_food)


drinks=db.get_menu_item(False)
for drink in drinks:#پیمایش کن 
  list_box_drink.insert('end',drink[1])#اندیس یکم را نمایش بده

foods=db.get_menu_item(True)
for food in foods:
  list_box_food.insert('end',food[1])

button_frame=LabelFrame(window,bg='Powderblue',text='status',font='bold',fg='Black')
button_frame.grid(row=1,column=1,padx=5,pady=5)

def exit_program():
  message_exit=TK.messagebox.askquestion('خروج','آیا قصد خروج دارید ؟',icon='warning')
  if message_exit=='yes':
    window.destroy()
window.protocol("WM_DELETE_WINDOW",exit_program)

button_exit=Button(button_frame,text='خروج',command=exit_program)
button_exit.grid(row=0,column=0,padx=5,pady=5)

def open_calc():
  call(['calc.exe'])


button_calc=Button(button_frame,text='ماشین حساب',command=open_calc)
button_calc.grid(row=0,column=1,padx=5,pady=5)

#total_fram=LabelFrame(window,bg='Powderblue',text='Total price')
#total_fram.grid(row=1,column=0,padx=10,pady=10)

#list_total=Listbox(total_fram,bg='White')
#list_total.grid(row=1,column=0,sticky='nsew')
#list_total.config(justify=LEFT)


window.mainloop()

     
    

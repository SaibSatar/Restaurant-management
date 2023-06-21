# Restaurant-management
you can make your database with your own progam or use sample code:








class database:


    def __init__(self,db): 
      self.__dbs_db=db 
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
                               """)                                                                
                            
      self.connection.commit()
      self.connection.close()
    
    def inserts(self,id,name,price,Is_food):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("INSERT INTO table_menu VALUES(?,?,?,?) " , (id,name,price,Is_food))
      self.connection.commit()

    def get_menu_item(self,Is_food):
       self.connection=sqlite3.connect(self.__dbs_db)
       self.cursor=self.connection.cursor()
       self.cursor.execute("SELECT * FROM table_menu WHERE Is_food=?",(Is_food,))
       result=self.cursor.fetchall()
       return result

    def get_max_res_id(self): 
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("SELECT MAX (reciept_id) FROM table_reciepts")
      result=self.cursor.fetchall()#چون تغیری روی دیتابیس انجام نمیدهیم که دائمی باشد از فچآل استفاده میکنیم
      return result

    def get_menu_item_by_name(self,item_name):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('SELECT * FROM table_menu WHERE name=?',(item_name,))
      result=self.cursor.fetchall()
      return result
    
    def insert_into_reciept(self,reciept_id,menu_id,count,price):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute("INSERT INTO table_reciepts VALUES(?,?,?,?)",(reciept_id,menu_id,count,price))
      self.connection.commit()
      self.connection.close()
    
    def get_reciept_by_recieptid_menuid(self,reciept_id,menu_id):
       self.connection=sqlite3.connect(self.__dbs_db)
       self.cursor=self.connection.cursor()
       self.cursor.execute("SELECT * FROM table_reciepts WHERE reciept_id=? and menu_id=?",(reciept_id,menu_id))
       result=self.cursor.fetchall()
       return result

    def increase_count(self,reciept_id,menu_id):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('UPDATE table_reciepts SET count=count+1 WHERE reciept_id=? and menu_id=?',(reciept_id,menu_id))
      self.connection.commit()
      self.connection.close()
    
    def get_reciepts(self,reciept_id):
      self.connection=sqlite3.connect(self.__dbs_db)
      self.cursor=self.connection.cursor()
      self.cursor.execute('SELECT * FROM view_menu_reciepts WHERE reciept_id=?',(reciept_id,))
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

    


      
      
ارد کردن دیتابیس
if os.path.isfile('restaurant.db')==FALSE:
  db=database('restaurant.db') 
  db.inserts(1,چلومرغ',22000,True)
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
  db=database('restaurant.db')


this code make database and some function to use it

# Restaurant-management









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

    


      
      

if os.path.isfile('restaurant.db')==FALSE:

  db=database('restaurant.db') 
  
  #db.insert(id,'name of food',price,is food?)
  
  db.insert(1,'pizza',2000,True)

  else:
  db=database('restaurant.db')

  # if you have drink,you should write False for (is food?) question

  
  





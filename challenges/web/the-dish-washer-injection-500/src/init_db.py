import pymysql

db = pymysql.connect("localhost", "adminuser", "oarlkbvpamoqisjfpmqlezknovremhk", "dishwashers_db")
cursor = db.cursor()
cursor.execute("""CREATE TABLE dishwashers (
   inserted_by VARCHAR(255),
   id VARCHAR(255),
   dishwasher_object TEXT,
   PRIMARY KEY ( id ))""")
db.commit()
db.close()

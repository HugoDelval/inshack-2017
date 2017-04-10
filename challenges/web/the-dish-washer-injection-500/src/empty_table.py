import pymysql

db = pymysql.connect("localhost", "adminuser", "oarlkbvpamoqisjfpmqlezknovremhk", "dishwashers_db")
cursor = db.cursor()
insert_str = "INSERT INTO dishwashers VALUES ('{inserted_by}', '{id}', '{object}')"
cursor.execute("DELETE FROM dishwashers")
cursor.execute(insert_str.format(inserted_by="Gary McKinnon", id="ly6Bkn1qUgSt7wbGiqU3PSHUDVi4s7D27DrUsJDZdJbqqIenTe", object='!!python/object:src.DishWasher {brand: no idea, cost: 1000, cve: dont care, id: ly6Bkn1qUgSt7wbGiqU3PSHUDVi4s7D27DrUsJDZdJbqqIenTe,\n  name: Boarf}\n'))
cursor.execute(insert_str.format(inserted_by="LulzSec", id="atq9kr0vSC9zsb4sinUgipQ5OUDhzQh8SdsRHgZnavhjZMrZjs", object='!!python/object:src.DishWasher {brand: no clue, cost: 10800, cve: my ass, id: atq9kr0vSC9zsb4sinUgipQ5OUDhzQh8SdsRHgZnavhjZMrZjs,\n  name: Mmmmmf}\n'))
cursor.execute(insert_str.format(inserted_by="Adrian Lamo", id="Gi3IA8RodtmoBSQFRbCxOsZEwaiTcoXOxczJVlemea7bOusi4I", object='!!python/object:src.DishWasher {brand: crappy corp, cost: 123456789, cve: you\n    wish, id: Gi3IA8RodtmoBSQFRbCxOsZEwaiTcoXOxczJVlemea7bOusi4I, name: W.C.}\n'))
cursor.execute(insert_str.format(inserted_by="Jonathan James", id="w4J1cZtl09PT0VaMBZILk1dKwhD4TKwATX6grlAnZGusXqtazg", object='!!python/object:src.DishWasher {brand: Micro, cost: 987654321, cve: dont be so\n    smart, id: w4J1cZtl09PT0VaMBZILk1dKwhD4TKwATX6grlAnZGusXqtazg, name: Tssssk}\n'))
db.commit()
db.close()

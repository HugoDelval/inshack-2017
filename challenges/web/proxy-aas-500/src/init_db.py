#!/usr/bin/python3
from index import db, Port
db.create_all()
for p in range(1024, 65536):
    port = Port(p)
    db.session.add(port)
db.session.commit()

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Blog_database import Admin,Blog_data,Base


engine = create_engine('sqlite:///Blog_database.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

admin=Admin(Id=1,Name="Hemanth_Pulicharla",About="A techno enthuast")
admin.hash_password('28997479')
session.add(admin)
session.commit()

blog_data1=Blog_data(Id=1,head="Testingscenario",Para1="hhhhhhhhhhhhkkkvvvvvvvvvvvvvvvvvvvvvvvvvwvfiuffffvbbbbbbbbbbbbbbblkkkkhlllllllllabbuaeeeeeeeeeeerhbjallaaaaaaaaaaaaaaaljrkvbaaaaaaaaakjjnmnvaavjbbbbbbkjr,bvrrrrrrrrrrrrrrrrrrrrrrramvajkkkkkkkkkkkkkkkkkkkkkqeeeeeeeeeeeerkjbajjjjjqalavbbbbbbbbssseviikjbbrrvjauvwefhhhhhhhhjcjwkkewwek",links="www.google.com",file="empty")
session.add(blog_data1)
session.commit()

blog_data2=Blog_data(Id=2,head="Testingscenario",Para1="hhhhhhhhhhhhkkkvvvvvvvvvvvvvvvvvvvvvvvvvwvfiuffffvbbbbbbbbbbbbbbblkkkkhlllllllllabbuaeeeeeeeeeeerhbjallaaaaaaaaaaaaaaaljrkvbaaaaaaaaakjjnmnvaavjbbbbbbkjr,bvrrrrrrrrrrrrrrrrrrrrrrramvajkkkkkkkkkkkkkkkkkkkkkqeeeeeeeeeeeerkjbajjjjjqalavbbbbbbbbssseviikjbbrrvjauvwefhhhhhhhhjcjwkkewwek",links="www.google.com",file="empty")
session.add(blog_data2)
session.commit()

print("Yes you got it!")
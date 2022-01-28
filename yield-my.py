
################3

#działa!!!!!
#
def pr():
     print("Abc")
     a = yield
     while True:
             print(a)
             a += 1
             yield

f=pr()
f.send(None) 
f.send(1) #tu mogę podstawić dowolną wartość początkową
next(f)

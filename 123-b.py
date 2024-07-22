import base64
import os
y=os.stat('C:\\Users\\Administrator\\Desktop\\python-2.7.18.amd64 (1).msi')
print(y.st_size)
with open('C:\\Users\\Administrator\\Desktop\\python-2.7.18.amd64 (1).msi','rb') as f:
    print(f)
    #a=f.read()
    #base64_str = base64.b64encode(f.read())
    #print(base64_str)
'''
with open('C:\\Users\\Administrator\\Desktop\\python-2.7.18.amd64 (2).msi','wb') as f1:
    f1.write(a)'''
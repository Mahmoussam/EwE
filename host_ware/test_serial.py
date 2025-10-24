from E_Serial import *


for i in range(254):
    AcknowledgeMessage()
m1 = AcknowledgeMessage()
m2 = WriteMessage(1 , 2)
print(m1 , '\n' , m2)
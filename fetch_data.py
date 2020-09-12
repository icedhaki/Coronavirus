# Importing pandas 
import pandas as pd 
import xlsxwriter

url = "https://www.michigan.gov/coronavirus/0,9753,7-406-98159-523641--,00.html"
  
table = pd.read_html(url)[3]
table.to_excel("data.xlsx") 

table1 = pd.read_html(url)[4]
table1.to_excel("data1.xlsx")


df = pd.read_excel('data1.xlsx', sheet_name='Sheet1') # can also index sheet by name or fetch all sheets
mylist = df['Bed Occupancy %'].tolist()
# delete last element
mylist.pop(45)
print(mylist)

# remove last character from each string in list
newlist = list(map(lambda i: i[ : -1], mylist)) 

# calculate score for bed occupancy
for i in range(0, len(newlist)): 
    newlist[i] = float(newlist[i])/100 

print(newlist)

df1 = pd.read_excel('data.xlsx', sheet_name='Sheet1') # can also index sheet by name or fetch all sheets
print(df1)

df1.insert(8,"Bed occupancy",newlist,True)

n95 = df1['N95 Masks'].tolist()
surg = df1['Surgical Masks'].tolist()
gown = df1['Surgical Gowns'].tolist()
eye = df1['Eye Protection'].tolist()
glove = df1['Gloves'].tolist()

for i in range(0,len(n95)):
    if(n95[i]=="21+ days"):
        n95[i]=1
    elif(n95[i]=="15-21 days"):
        n95[i]=0.75
    elif(n95[i]=="7-14 days"):
        n95[i]=0.5
    else:
        n95[i]=0.25

for i in range(0,len(surg)):
    if(surg[i]=="21+ days"):
        surg[i]=1
    elif(surg[i]=="15-21 days"):
        surg[i]=0.75
    elif(surg[i]=="7-14 days"):
        surg[i]=0.5
    else:
        surg[i]=0.25

for i in range(0,len(gown)):
    if(gown[i]=="21+ days"):
        gown[i]=1
    elif(gown[i]=="15-21 days"):
        gown[i]=0.75
    elif(gown[i]=="7-14 days"):
        gown[i]=0.5
    else:
        gown[i]=0.25

for i in range(0,len(eye)):
    if(eye[i]=="21+ days"):
        eye[i]=1
    elif(eye[i]=="15-21 days"):
        eye[i]=0.75
    elif(eye[i]=="7-14 days"):
        eye[i]=0.5
    else:
        eye[i]=0.25

for i in range(0,len(glove)):
    if(glove[i]=="21+ days"):
        glove[i]=1
    elif(glove[i]=="15-21 days"):
        glove[i]=0.75
    elif(glove[i]=="7-14 days"):
        glove[i]=0.5
    else:
        glove[i]=0.25

score = []
for i in range(0,len(glove)):
    val=(n95[i])*(surg[i])*(gown[i])*(eye[i])*(glove[i])*(newlist[i])
    score.append(val)


df1.insert(3,"N95 masks scores",n95,True)
df1.insert(5,"Surgery masks scores",surg,True)
df1.insert(7,"Gowns scores",gown,True)
df1.insert(9,"Eye scores",eye,True)
df1.insert(11,"Glove scores",glove,True)




df1.insert(14,"final score",score,True)
df1.to_excel("data.xlsx")

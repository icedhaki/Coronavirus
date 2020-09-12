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
print(df1)

n95 = df1['N95 Masks'].tolist()
names = df1['Health System/Hospital'].tolist()

print(n95)

for i in range(0,len(n95)):
    if(n95[i]=="21+ days"):
        n95[i]=1
    elif(n95[i]=="15-21 days"):
        n95[i]=0.75
    elif(n95[i]=="7-14 days"):
        n95[i]=0.5
    else:
        n95[i]=0.25

print(n95)

df1.insert(2,"N95 masks",n95,True)



df1.to_excel("data.xlsx")

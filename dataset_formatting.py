import pandas as pd
import numpy as np
from numpy import nan as Nan

terror=pd.read_csv('./input/globalterrorismdb_0617dist.csv',encoding='ISO-8859-1')
terror.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
terror=terror[['Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
terror['casualities']=terror['Killed']+terror['Wounded']

#This is a basic table
terror = terror[["Year", "Month", "Killed", "Wounded", "casualities"]]

#This is the table that we can mess with
terror1 = terror.groupby(['Year', 'Month']).agg(['size', 'sum']).reset_index()
terror1.columns = [' '.join(col).strip() for col in terror1.columns.values]
terror1 = terror1.drop(["Wounded size", "casualities size"], axis=1)
terror1 = terror1.rename(index=str, columns={"Killed size": "num attacks"})
terror1 = terror1[terror1["Month"] != 0]

#Add 1993 Nan values
sub_terror_1993 = pd.DataFrame(np.array([[1993, i, Nan,Nan, Nan, Nan] for i in range(1, 13)]))
sub_terror_1993.columns = terror1.columns
sub_terror_1993["Year"] = sub_terror_1993["Year"].astype(int)
sub_terror_1993["Month"] = sub_terror_1993["Month"].astype(int)

terror2 = pd.concat([terror1[:276], sub_terror_1993, terror1[276:]]).reset_index().drop(["index"], axis=1)
terror2.to_csv("./input/editted_input.csv", index=False)
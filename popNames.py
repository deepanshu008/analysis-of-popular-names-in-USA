# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 03:05:36 2018

@author: Deepanshu Sharma
"""

#%%
####ANS6(a)
import pandas as pd
import zipfile as zp
zip = zp.ZipFile('D:\\NCSU\\SEM 3\\ISE 589 (Python)\\Exam 2\\Exam_2\\names.zip' , 'r')		
fileList1 = zip.namelist()
fileList = [x for x in fileList1 if x != 'NationalReadMe.pdf']
df = pd.DataFrame(columns=["Name", "Sex", "Count", "Year"])
print(df)
for file in fileList:
	dat1 = pd.read_csv(zip.open(file),sep =',', names = ["Name", "Sex", "Count"])
	dat1["Year"] = file
	df = pd.concat([df, dat1])
	df = df.reset_index(drop=True)
df['Year'] = df['Year'].map(lambda x: x.lstrip('yob').rstrip('.txt'))
df["Count"] = df["Count"].astype(int)
df["Year"] = df["Year"].astype(int)
print("The total number of records across all years from 1880-2017 are:", len(df))
#%%
#################ANS6(b)
#print(df)
namecount = df.groupby(["Name", "Sex"])["Count"].sum() #######Shows the name as parent group with sex as subgroup along with count
print(namecount)
#%%
####ANS6(c)
import seaborn as sns
group = df.groupby(["Name", "Year"])["Count"].sum()
print(group)
name = ['Matthew', 'John', 'Evan', 'Ethan']
group = group.to_frame().reset_index()
group = group.loc[group['Name'].isin(name)]
sns.set(style='darkgrid')
sns.lmplot('Year', 'Count', data=group, hue='Name', fit_reg=False)

#%%
####ANS6(d)	 Female List###############################
f = ["F"]
years = list(range(1880,2018))
femalelist = df.loc[df['Year'].isin(years) & df['Sex'].isin(f)]
#print(df1)
PopFemales = femalelist.groupby(["Year"]).apply(lambda x: x.nlargest(10, 'Count'))
print(PopFemales)
#%%
####ANS6(d) Male List###############################
m = ["M"]
malelist = df.loc[df['Year'].isin(years) & df['Sex'].isin(m)]
#print(df1)			
Popmales = malelist.groupby(["Year"]).apply(lambda x: x.nlargest(10, 'Count'))
print(Popmales)			

#%%ANS6(e)
#reduced_df  = namecount[(namecount['Sex'] == 'F') | (namecount['Sex'] == 'M')]
femalelist1 = df.loc[df['Sex'].isin(f)]
femalelist1 = femalelist1.groupby(["Name"])["Count"].sum()
femalelist1 = femalelist1.to_frame().reset_index()
#print(femalelist1)
malelist1 = df.loc[df['Sex'].isin(m)]
malelist1 = malelist1.groupby(["Name"])["Count"].sum()
malelist1 = malelist1.to_frame().reset_index()
#print(malelist1)
k = pd.merge(femalelist1, malelist1, on=["Name"])
k = k.rename(columns={'Count_x': 'Female_Count', 'Count_y': 'Male_Count'})
k['Ratio'] = k['Male_Count']/k['Female_Count']
print(k)
Unisexnames = k[k['Ratio'].between(0.25, 4, inclusive=True)]
print(Unisexnames)													   
					
#%%
######ANS6(f)
import seaborn as sns
#####assuming popularity means the total number of times the name is used across all years
#####given it falls in the unisex name criteria (ratio between 0.25 to 4)
Unisexnames['Total_Count'] = Unisexnames['Female_Count'] + Unisexnames['Male_Count'] 
#print(k1)				
PopUnisex = Unisexnames.nlargest(5,'Total_Count')	
print(PopUnisex)
pop = PopUnisex["Name"].tolist()  ####List of top 5 unisex names
print(pop)
PopUniyearcount = df.groupby(["Name", "Year"])["Count"].sum() ####series from the main dataset to get count per year for a given name
PopUniyearcount = PopUniyearcount.to_frame().reset_index()   ##### series to dataframe conversion
#print(PopUniyearcount)
Popname = PopUniyearcount.loc[PopUniyearcount['Name'].isin(pop)] ####### getting only the values from the top 5 names list
print(Popname)
sns.set(style='darkgrid')
sns.lmplot('Year', 'Count', data=Popname, hue='Name', fit_reg=False)
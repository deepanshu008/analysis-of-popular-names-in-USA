# -*- coding: utf-8 -*-
"""
Created on Fri Nov 01 21:22:40 2018

@author: Deepanshu Sharma
"""

#%%

'''
The following will read the zipfile containing all the text files within it with 3 columns which are name,sex and count. The text
files has names which are already sorted in terms of the number of times a name is recorded. More info about the dataset can be found
at: https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data

The dataframe created from the text files will also have a year column added to it along with the 3 mentioned above
'''

import pandas as pd
import zipfile as zp
import seaborn as sns

zip = zp.ZipFile('D:\\names.zip' , 'r')		
fileList1 = zip.namelist()
fileList = [x for x in fileList1 if x != 'NationalReadMe.pdf'] ####not reading the info file
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

'''
printing the total number of records across all years
'''

print("The total number of records across all years from 1880-2017 are:", len(df))

#%%

'''
the number of times that each name was used, separately for boys and girls across all years
'''

namecount = df.groupby(["Name", "Sex"])["Count"].sum() #######Shows the name as parent group with sex as subgroup along with count
print(namecount)


#%%

'''
A single plot showing the popularity of the name 'Matthew', 'John', 'Evan', 'Ethan' across the years. 
'''

import seaborn as sns
group = df.groupby(["Name", "Year"])["Count"].sum()
print(group)
name = ['Matthew', 'John', 'Evan', 'Ethan']
group = group.to_frame().reset_index()
group = group.loc[group['Name'].isin(name)]
sns.set(style='darkgrid')
sns.lmplot('Year', 'Count', data=group, hue='Name', fit_reg=False)

#%%
'''
the 10 most popular names based on ‘M’ or ‘F’ for every year
'''

f = ["F"]
years = list(range(1880,2018))
femalelist = df.loc[df['Year'].isin(years) & df['Sex'].isin(f)]
#print(df1)
PopFemales = femalelist.groupby(["Year"]).apply(lambda x: x.nlargest(10, 'Count'))
print(PopFemales)   ####popular female names


#%%
m = ["M"]
malelist = df.loc[df['Year'].isin(years) & df['Sex'].isin(m)]
#print(df1)			
Popmales = malelist.groupby(["Year"]).apply(lambda x: x.nlargest(10, 'Count'))
print(Popmales)	    #popular male names	

'''
concatening the two dataframes into one by joining them on the basis of a name and finding names which are used for both females
and males #UnisexNames
'''

femalelist1 = df.loc[df['Sex'].isin(f)]
femalelist1 = femalelist1.groupby(["Name"])["Count"].sum()
femalelist1 = femalelist1.to_frame().reset_index()

malelist1 = df.loc[df['Sex'].isin(m)]
malelist1 = malelist1.groupby(["Name"])["Count"].sum()
malelist1 = malelist1.to_frame().reset_index()

k = pd.merge(femalelist1, malelist1, on=["Name"])
k = k.rename(columns={'Count_x': 'Female_Count', 'Count_y': 'Male_Count'})
k['Ratio'] = k['Male_Count']/k['Female_Count']
print(k)

'''
Identifying the unisex names where the ratio between the boys and girls total is between 1 to 4 and 4 to 1
'''

Unisexnames = k[k['Ratio'].between(0.25, 4, inclusive=True)]
print(Unisexnames)													   
					
#%%
'''
Plotting the popularity vs year for the top 5 unisex names
'''

#####assuming popularity means the total number of times the name is used across all years
#####given it falls in the unisex name criteria (ratio between 0.25 to 4)

Unisexnames['Total_Count'] = Unisexnames['Female_Count'] + Unisexnames['Male_Count'] 				
PopUnisex = Unisexnames.nlargest(5,'Total_Count')	
print(PopUnisex)
pop = PopUnisex["Name"].tolist()  ####List of top 5 unisex names
print(pop)
PopUniyearcount = df.groupby(["Name", "Year"])["Count"].sum() ####series from the main dataset to get count per year for a given name
PopUniyearcount = PopUniyearcount.to_frame().reset_index()   ##### series to dataframe conversion
Popname = PopUniyearcount.loc[PopUniyearcount['Name'].isin(pop)] ####### getting only the values from the top 5 names list
sns.set(style='darkgrid')
sns.lmplot('Year', 'Count', data=Popname, hue='Name', fit_reg=False)

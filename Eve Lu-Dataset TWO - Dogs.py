#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[18]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[19]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx")


# In[20]:


df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[21]:


df.shape


# In[22]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[23]:


# Each row is an animal in the zoo.


# In[24]:


# Spayed or Neut means: whether the ovaries, fallopian tubes and uterus of are removed from the animals


# In[25]:


# Guard or Trained means: whether the animals are trained by the zoo stuff


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[26]:


# First need to remove spaces in column's name

df.columns = df.columns.str.replace(" ","")


# In[27]:


df.PrimaryBreed.value_counts().head(10)


# In[28]:


df.PrimaryBreed.value_counts().head(10).plot()


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[29]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values= ["Unknown"])
df.columns = df.columns.str.replace(" ","")


# In[30]:


df.PrimaryBreed.value_counts().head(10).plot()


# ## What are the most popular dog names?

# In[31]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values= ["Unknown","UNKNOWN"])
df.columns = df.columns.str.replace(" ","")
df.AnimalName.value_counts()


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[32]:


df[df.AnimalName.str.contains("Max",na=False)].AnimalName.value_counts()
# 515 dogs named Max
# 30 dogs named Maxwell


# ## What percentage of dogs are guard dogs?

# In[33]:


df.GuardorTrained.value_counts(normalize=True)


# ## What are the actual numbers?

# In[34]:


df.GuardorTrained.value_counts()
# only 51 dogs are trained/guard dogs.


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[35]:


df.GuardorTrained.value_counts()
# it might be because the computer filter "NaN" & empty blank to read?


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[36]:


# dropna=True meaning Don't include counts of NaN!!
df.GuardorTrained.value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[37]:


df[df.GuardorTrained == "Yes"].PrimaryBreed.value_counts().head()
# German Shepherd Dog is the top dog breed for guard dogs


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[38]:


df['AnimalBirth'].apply(lambda birth: birth.year)


# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[39]:


zn = pd.read_csv("zipcodes-neighborhoods.csv")
zn


# In[40]:


# zn: the dataframe you're about to merge
# left_on: the index column name from left dataframe (your original dataframe)
# right_on: the index column name from left dataframe (the dataframe you're about to merge)
merged = df.merge(zn, left_on='OwnerZipCode', right_on='zip')
merged


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[79]:


merged.groupby(by="neighborhood").PrimaryBreed.value_counts().groupby(level=0).nlargest(1)


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[191]:


# method 1 (but can't really see the male dogs data here...)
df[df.SpayedorNeut == "No"].groupby(by="AnimalGender").PrimaryBreed.value_counts()


# In[192]:


# method 2 (create 2 varibles!)
# Female dogs that are least likely to be spayed ---> Yorkshire Terrier
df.AnimalGender == "F"
df_female = df[df.AnimalGender == "F"]
df_female[df_female.SpayedorNeut == "No"].PrimaryBreed.value_counts()


# In[193]:


# Male dogs that are least likely to be spayed ---> Yorkshire Terrier
df.AnimalGender == "M"
df_male = df[df.AnimalGender == "M"]
df_male[df_male.SpayedorNeut == "No"].PrimaryBreed.value_counts()


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[194]:


df["monochrome"] = ""


# In[195]:


df_3color = df[df.AnimalThirdColor.isna()]


# In[196]:


df_2color = df_3color[df_3color.AnimalSecondaryColor.isna()]


# In[197]:


df_1color = df_2color[df_2color.AnimalDominantColor.isin(["BLACK","WHITE","Gray","GRAY"])]


# In[198]:


#df = df.drop("monochrome", axis = 1)

df_1color.monochrome = True


# In[199]:


df_1color.monochrome.value_counts()

# There 6959 animals are monochrome.
## but how should I SAVE df_1color.monochrome = True back to the main dataframe?


# ## How many dogs are in each borough? Plot it in a graph.

# In[1]:


merged.borough.value_counts()#.plot()


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[77]:


# method 1 (with one line!)
merged.groupby(by="borough").PrimaryBreed.value_counts().groupby(level=0).nlargest(5).plot(kind="bar")


# In[70]:


# Tips for myself in case I forget!!:
# .groupby(level=0) 其实意味着你在原来valuecount的基础上，重新按照现存的两个变量来分类（这里分别为borough & PrimaryBreed）
# 如果level = 0 那么就如题干，得出每一个区的每个狗的品种数量（value_counts)--->.nlargest(5)是用来限制top 5的，可以随时修改
# 如果level = 1 那么得出的结果就是 ---> 每种狗品种在每个区的数量，按数量排序 --->.nlargest(5)同样是用来限制top 5，可以随时修改


# In[71]:


# method 2 (create five different varibles and then take the top 5 number)

merged_Manhattan = merged[merged.borough == "Manhattan"]
merged_Manhattan.PrimaryBreed.value_counts().head(5)


# In[72]:


merged_Brooklyn = merged[merged.borough == "Brooklyn"]
merged_Brooklyn.PrimaryBreed.value_counts().head(5)


# In[73]:


merged_Queens = merged[merged.borough == "Queens"]
merged_Queens.PrimaryBreed.value_counts().head(5)


# In[74]:


merged_Bronx = merged[merged.borough == "Bronx"]
merged_Bronx.PrimaryBreed.value_counts().head(5)


# In[75]:


merged_StatenIsland  = merged[merged.borough == "Staten Island"]
merged_StatenIsland.PrimaryBreed.value_counts().head(5)


# In[ ]:





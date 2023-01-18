#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd


# In[38]:


# cleaned tract level ses data
# availiable from https://github.com/geomarker-io/dep_index
df_tract = pd.read_csv('data/Tract_clustering_dataset_2017.csv') 


# In[39]:


# tract to zipcode (not zcta) mapping file
# availiable from https://www.huduser.gov/portal/datasets/usps_crosswalk.html
df_tract_to_zip = pd.read_excel('data/TRACT_ZIP_122017.xlsx') 


# In[40]:


df_tract_to_zip['zip'] = df_tract_to_zip.zip.astype('str')
df_tract_to_zip.zip = df_tract_to_zip.zip.str.zfill(5)


# In[110]:


# merge, get 3-digit-zip
df_zip = df_tract.merge(df_tract_to_zip[['zip','tract','res_ratio']],left_on='census_tract_fips',right_on='tract')
df_zip['ZIP3'] = df_zip.zip.str[:3]


# In[111]:


# weight by population
df_zip['pop_weights'] = df_zip.POPULATION*df_zip.res_ratio


# In[113]:


df_zip = df_zip[df_zip.pop_weights != 0] # remove 0 population records to avoid divided by zero error


# In[114]:


def weighted(x, cols, w="pop_weights"):
    return pd.Series(np.average(x[cols], weights=x[w], axis=0), cols)


# In[115]:


# weighted average for seven features
df_zip3 = df_zip.groupby(by='ZIP3').apply(weighted,
        ['fraction_assisted_income', 'fraction_high_school_edu', 
         'median_income', 'fraction_no_health_ins',
       'fraction_poverty', 'fraction_vacant_housing', 'dep_index'])


# In[117]:


df_zip3.reset_index(inplace=True)


# In[118]:


df_zip3.to_csv('ZIP3_SES_2017.csv',index=False)


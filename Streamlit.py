import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Tax Revenue Data")

st.markdown(
    """
    <style>
    .main {
    background-color:#FBF9E6;
    }
    </style>
    """,
    unsafe_allow_html=True)

st.header('TAX REVENUE ANALYSIS')

df=pd.read_csv('Cleaned.csv')

years = list(df['FISCAL_YEAR'].unique())
years.sort(reverse=True)
    
acc_category  = list(df['ACC_CODE'].unique())
acc_category.append('ALL')
acc_category[0],acc_category[1]=acc_category[1],acc_category[0]

area  = list(df['NAME'].unique())
area.append('ALL')

#static
col1,col2,col3=st.columns(3)
with col1:
    df_group_year = df[['FISCAL_YEAR','TODAYCOLL']].groupby(['FISCAL_YEAR'],as_index=False).sum()
    df_group_year.replace(np.nan,0,inplace=True)
    
    st.subheader("Yearwise Total Collection")
    fig1 = plt.figure(figsize=(7,4.5))
    plt.bar(df_group_year['FISCAL_YEAR'], df_group_year['TODAYCOLL']/10000000,alpha=0.5)
    plt.xlabel('Fiscal Year',fontsize = 14)
    plt.ylabel('Total Revenue (in crores)',fontsize = 14)
    plt.xticks(rotation = 60,fontsize = 14)
    plt.yticks(fontsize = 14)
    st.pyplot(fig1)

with col2:
    df_group_code = df[['ACC_CODE','TODAYCOLL']]
    df_group_code = df_group_code.groupby(['ACC_CODE'],as_index=False).sum()
    df_group_code.replace(np.nan,0,inplace=True)
    
    st.subheader("Category-wise Revenue")
    fig2=plt.figure(figsize =(6, 6))
    plt.pie(df_group_code['TODAYCOLL'],radius=1.1)
    plt.legend(df_group_code['ACC_CODE'],fontsize = 12,title ="Categories",loc ="upper center",bbox_to_anchor =(0.5, 0.08),ncol=3)
    st.pyplot(fig2)

with col3:
    df_group_area = df[['NAME','TODAYCOLL']]
    df_group_area = df_group_area.groupby(['NAME'],as_index=False).sum()
    df_group_area=df_group_area.sort_values(by='TODAYCOLL',ascending=False,ignore_index=True)
    df_group_area.replace(np.nan,0,inplace=True)
    df_group_area.drop(df_group_area.index[10:],inplace=True)
    
    st.subheader("Ward-wise Total Collection")
    fig3 = plt.figure(figsize=(7,4.75))
    plt.bar(df_group_area['NAME'], df_group_area['TODAYCOLL']/10000000, alpha=0.5)
    plt.xlabel('Ward',fontsize=14)
    plt.ylabel('Total Revenue (in crores)',fontsize=14)
    plt.xticks(rotation = 60,fontsize=14)
    plt.yticks(fontsize=14)
    st.pyplot(fig3)

#filters
col1,col2,col3=st.columns(3)
with col1:
    year_filter=st.selectbox('Select financial year',years)
with col2:
    category_filter=st.selectbox('Select category',acc_category)
with col3:
    area_filter=st.selectbox('Select area',area)

col1,col2,col3,col4=st.columns(4)

with col1:

    df_group_year['pchange']=df_group_year['TODAYCOLL'].pct_change()
    pc=df_group_year.loc[df_group_year['FISCAL_YEAR'] == year_filter].reset_index()
    
    def delt(x):
        if x=='2012-2013':
            return ''
        elif x!='2012-2013':
            return str(round(pc['pchange'][0]*100,2))+" %"
        else:
            pass
    r = df_group_year[df_group_year['FISCAL_YEAR'] == year_filter].reset_index()['TODAYCOLL'][0]
    st.metric(label="Total revenue in FY: "+str(year_filter), value="₹ "+ str(round(r/10000000,2))+"Cr", delta=delt(year_filter))

    ydf=df[(df['FISCAL_YEAR'] == year_filter) | ('ALL' == year_filter)]
    df_group_code = ydf[['ACC_CODE','TODAYCOLL']].groupby(['ACC_CODE'],as_index=False).sum()
    df_group_code.replace(np.nan,0,inplace=True)

with col2:
    p=df_group_code[df_group_code['ACC_CODE']=='Property Tax'].reset_index()['TODAYCOLL'][0]
    st.metric(label="Revenue from Property tax in: "+str(year_filter), value="₹ "+ str(round(p/10000000,2))+"Cr")

with col3:
    w=df_group_code[df_group_code['ACC_CODE']=='Water Charges'].reset_index()['TODAYCOLL'][0]
    st.metric(label="Revenue from Water tax in: "+str(year_filter), value="₹ "+ str(round(w/10000000,2))+"Cr")

col1,col2=st.columns(2)

with col1:
    st.write("Category-wise breakdown for FY: "+str(year_filter))
    fig4=plt.figure(figsize =(5, 5))
    plt.pie(df_group_code['TODAYCOLL'],radius=1.1)
    plt.legend(df_group_code['ACC_CODE'],title ="Categories",loc ="upper center",bbox_to_anchor =(0.5, 0.06),ncol=3,fontsize=12)
    st.pyplot(fig4)
    
with col2:
    st.write("Areas with highest revenue from: "+str(category_filter)+" in: "+str(year_filter))
    cydf=ydf[(ydf['ACC_CODE'] == category_filter) | ('ALL' == category_filter)]
    df_group_area=cydf[['NAME','TODAYCOLL']].groupby(['NAME'],as_index=False).sum().sort_values(by='TODAYCOLL',ascending=False,ignore_index=True)         
    df_group_area.replace(np.nan,0,inplace=True)
    df_group_area.drop(df_group_area.index[10:],inplace=True)
    
    fig5 = plt.figure(figsize=(7,3.75))
    plt.bar(df_group_area['NAME'], df_group_area['TODAYCOLL']/10000000,alpha=0.5)
    plt.xlabel('Ward',fontsize = 14)
    plt.ylabel('Revenue (in crores)',fontsize = 14)
    plt.xticks(rotation = 60,fontsize = 14)
    plt.yticks(fontsize = 14)
    st.pyplot(fig5)

col1,col2=st.columns(2)

acydf=cydf[(cydf['NAME'] == area_filter) | ('ALL' == area_filter)]

m=acydf['TODAYCOLL'].sum()    
col4.metric(label="Revenue: "+str(category_filter)+", "+str(area_filter)+", "+str(year_filter), value="₹ "+ str(round(m/10000000,2))+"Cr")
    
    
    
    
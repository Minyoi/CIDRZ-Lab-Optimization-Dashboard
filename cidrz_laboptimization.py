# -*- coding: utf-8 -*-
"""
Created on Thu May 15 18:59:52 2025

@author: Minyoi.Maimbolwa
"""
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import altair as alt
import streamlit as st
from streamlit_gsheets import GSheetsConnection



st.set_page_config(
    page_title="Lab Optimization Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")


df = pd.DataFrame()
df1 = pd.DataFrame()
df1_1 = pd.DataFrame()
df1_2 = pd.DataFrame()
df2 = pd.DataFrame()
df2_1 = pd.DataFrame()
df1_2 = pd.DataFrame()
df3 = pd.DataFrame()
df3_1 = pd.DataFrame()
df3_2 = pd.DataFrame()

with st.sidebar:
    st.title('🏂 CIDRZ Lab Optimization dashboard')

    
    
    file = st.file_uploader("Please upload the lab data extract below", type={"xlsx"})
    
    if file is not None:
        df = pd.read_excel(file, sheet_name='Sheet 1 - TB XTRACT-042025')
        #st.write(df)      

    
        df['sampleid_testcode'] = df['PATIENT ID'].astype(str) + '-'+ df['ACCESSION NUMBER'].astype(str)
        df['rec_date'] = pd.to_datetime(df['RECEIVE DATE'],dayfirst=True, format="%Y-%m-%d %H:%M:%S.000")
        df['month_processed'] = df['rec_date'].dt.to_period('M')
        df['year_processed'] = df['rec_date'].dt.to_period('Y')
        a = ['AFBST','XPUT','CULTB','XPRIF']
        new_df = df[df['TEST CODE'].isin(a)]
        pivoted = new_df.pivot(index=["sampleid_testcode","RECEIVE DATE", "month_processed","year_processed"], columns="TEST CODE", values="TEST RESULT")
        new_pivoted = pivoted.reset_index()
    
    
        new_pivoted['smear_result'] = np.where(new_pivoted['AFBST']=='NAFB',0,np.where(new_pivoted['AFBST']=='2AFB',1,np.where(new_pivoted['AFBST']=='MTBND',0,np.where(new_pivoted['AFBST']=='1AFB',1,np.where(new_pivoted['AFBST']=='3AFB',1,np.where(new_pivoted['AFBST']=='ZTEST',2,np.where(new_pivoted['AFBST']=='SAFB',1,np.nan)))))))
        new_pivoted['smear_lowgrade'] = np.where(new_pivoted['AFBST']=='NAFB',0,np.where(new_pivoted['AFBST']=='2AFB',0,np.where(new_pivoted['AFBST']=='MTBND',0,np.where(new_pivoted['AFBST']=='1AFB',1,np.where(new_pivoted['AFBST']=='3AFB',0,np.where(new_pivoted['AFBST']=='SAFB',1,np.nan))))))
        new_pivoted['xpert_result'] = np.where(new_pivoted['XPUT']=='MTBND',0,np.where(new_pivoted['XPUT']=='ERR',2,np.where(new_pivoted['XPUT']=='MTBVL',1,np.where(new_pivoted['XPUT']=='Mycobacteria Tuberculosis Trace Detected',1,np.where(new_pivoted['XPUT']=='MTBL',1,np.where(new_pivoted['XPUT']=='MTBH',1,np.where(new_pivoted['XPUT']=='ZTEST',6,np.where(new_pivoted['XPUT']=='Mycobacteria  Tuberculosis Trace Detected',1,np.where(new_pivoted['XPUT']=='Mycobacteria Tuberculosis Detected Trace',1,np.where(new_pivoted['XPUT']=='MTBM',1,np.where(new_pivoted['XPUT']=='INSUF',8,np.where(new_pivoted['XPUT']=='ND',0,np.where(new_pivoted['XPUT']=='Mycobacterium Tuberculosis Trace detected',1,np.nan)))))))))))))
        new_pivoted['culture_result'] = np.where(new_pivoted['CULTB']=='TBCP',0,np.where(new_pivoted['CULTB']=='TBCN',0,np.where(new_pivoted['CULTB']=='TBCC',4,np.where(new_pivoted['CULTB']=='INSUF',5,np.where(new_pivoted['CULTB']=='ZTEST',3,np.where(new_pivoted['CULTB']=='TF1',2,np.where(new_pivoted['CULTB']=='MOTT',1,np.where(new_pivoted['CULTB']=='NEG',0,np.where(new_pivoted['CULTB']=='TF2',2,np.where(new_pivoted['CULTB']=='MTBC',1,np.nan))))))))))
        new_pivoted['rif_result'] = np.where(new_pivoted['XPRIF']=='RRND',0,np.where(new_pivoted['XPRIF']=='ZTEST',2,np.where(new_pivoted['XPRIF']=='NA',4,np.where(new_pivoted['XPRIF']=='INSUF',5,np.where(new_pivoted['XPRIF']=='RRIN',6,np.where(new_pivoted['XPRIF']=='RRDT',1,np.nan))))))
    
    
        culture_df = new_pivoted[['month_processed','year_processed' ,'culture_result']]
        xpert_df = new_pivoted[['month_processed','year_processed', 'xpert_result']]
        smear_df = new_pivoted[['month_processed','year_processed', 'smear_result']]
        smearlg_df = new_pivoted[['month_processed','year_processed', 'smear_lowgrade']]
        rif_df = new_pivoted[['month_processed','year_processed', 'rif_result']]
    
        # Processing for the culture summaries
        df1 = culture_df['month_processed'].value_counts().rename_axis('unique_values').reset_index(name='counts')
        df1=pd.crosstab(index=culture_df['month_processed'], columns=culture_df['culture_result'])
        df1 = df1.rename(columns = {0.0:'Negative', 1.0:'Positive',2.0:'TF', 3.0:'Z_test',4.0:'Contaminated',5.0:'Insufficient'})
        df1_1 = df1.copy()
        df1_1['total_samples'] = df1[['Contaminated','Negative','TF']].sum(axis=1) 
        df1_1['perc_contaminated'] = df1_1['Contaminated']/df1_1['total_samples'] * 100
        df1_1['perc_negative'] = df1_1['Negative']/df1_1['total_samples'] * 100
        df1_2 = df1_1.copy()
        df1_2.drop(['Contaminated', 'Negative', 'TF', 'Z_test','total_samples'], axis='columns', inplace=True)

        #dfc = df1.copy()
        #dfc = dfc.reset_index()
        #dfc['year_processed'] = pd.PeriodIndex(dfc['month_processed']).asfreq('Y')
        #dfc.set_index('month_processed', inplace=True)
    
    
        # Processing for the xpert summaries
        df2=pd.crosstab(index=xpert_df['month_processed'], columns=xpert_df['xpert_result'])
        df2 = df2.rename(columns = {0.0:'MTB_Not_detected', 1.0:'MTB_Detected',2.0:'Error', 6.0:'Z_test',8.0:'Insufficient'})
        df2_1 = df2.copy()
        df2_1['total_samples'] = df2[['Insufficient','Error','MTB_Detected','MTB_Not_detected']].sum(axis=1) 
        df2_1['perc_mtbdetected'] = df2_1['MTB_Detected']/df2_1['total_samples'] * 100
        df2_1['perc_error'] = df2_1['Error']/df2_1['total_samples'] * 100
        df2_2 = df2_1.copy()
        df2_2.drop(['Insufficient', 'Error', 'MTB_Detected', 'MTB_Not_detected','Z_test','total_samples'], axis='columns', inplace=True)
    
    
        # Processing for the smear summaries
        df3=pd.crosstab(index=smear_df['month_processed'], columns=smear_df['smear_result'])
        df3 = df3.rename(columns = {0.0:'TB_Not_detected', 1.0:'TB_Detected',2.0:'Z_test'})
        df3_1 = df3.copy()
        df3_1['total_samples'] = df3[['TB_Not_detected','TB_Detected']].sum(axis=1) 
        df3_1['perc_positive'] = df3_1['TB_Detected']/df3_1['total_samples'] * 100
        df3_1['perc_negative'] = df3_1['TB_Not_detected']/df3_1['total_samples'] * 100
        df3_2 = df3_1.copy()
        df3_2.drop(['TB_Not_detected', 'TB_Detected', 'Z_test','total_samples'], axis='columns', inplace=True)
        
        
        #Low grade processing
        df4=pd.crosstab(index=smear_df['month_processed'], columns=smearlg_df['smear_lowgrade'])
        df4 = df4.rename(columns = {0.0:'Not_Lowgrade', 1.0:'Low_Grade'})
        df4_1 = df4.copy()
        df4_1['total_smear'] = df4[['Not_Lowgrade','Low_Grade']].sum(axis=1) 
        df4_1['perc_lowgrade'] = df4_1['Low_Grade']/df4_1['total_smear'] * 100
        
        df_smear_join = df4_1.join(df3_1, how='inner')
        
        quarter_list = list(culture_df.month_processed.unique())[::-1] 
       
        selected_quarter = st.selectbox('List of quarters processed', quarter_list, index=len(quarter_list)-1)
        df_selected_quarter = culture_df[culture_df.month_processed == selected_quarter]
        df_selected_quarter_sorted = df_selected_quarter.sort_values(by="culture_result", ascending=False)
    
         
        # Processing for the rif summaries
        

    

col = st.columns((3, 3, 3), gap='medium')

with col[0]:
    st.markdown('#### Culture')
    
    if file is not None:    
        st.write('Total Culture Samples processed')
        df1_1 = df1_1.reset_index() 
        df1_1['month_processed'] = df1_1['month_processed'].astype(str)
        st.bar_chart(df1_1,x="month_processed",y="total_samples")
        st.write("Culture Results")
        st.write(df1)
        st.write("Culture Result Trends")
        df1_2 = df1_2.reset_index()
        #st.write(df1_2)
        df1_2['month_processed'] = df1_2['month_processed'].astype(str)
        st.line_chart(df1_2, x='month_processed')
       
        with st.expander('Key', expanded=True):
            st.write('''
                - Culture Lab data processed upto ''' + str(max(quarter_list)) + '''
                ''')   

with col[1]:
    st.markdown('#### Xpert')
    if file is not None:
        st.write('Total Xpert Samples processed')
        df2_1 = df2_1.reset_index() 
        df2_1['month_processed'] = df2_1['month_processed'].astype(str)
        st.bar_chart(df2_1, x="month_processed", y="total_samples")
        st.write("Xpert results")
        st.write(df2)
        st.write("Xpert Result Trends")
        df2_2 = df2_2.reset_index()
        #st.write(df2_2)
        df2_2['month_processed'] = df2_2['month_processed'].astype(str)
        st.line_chart(df2_2, x='month_processed')

        
     
        with st.expander('Key', expanded=True):
            st.write('''
                - Xpert Lab data processed upto ''' + str(max(quarter_list)) + '''
                ''')   

with col[2]:
    st.markdown('#### Smear')
    if file is not None:
        st.write('Total Smear Samples processed')
        df3_1 = df3_1.reset_index() 
        df3_1['month_processed'] = df3_1['month_processed'].astype(str)
        st.bar_chart(df3_1,x='month_processed', y="total_samples")
        st.write("Smear results")
        st.write(df3)
       # st.write(df3_1)
        st.write("Smear Result Trends")
        df3_2 = df3_2.reset_index()
        #st.write(df3_2)
        df3_2['month_processed'] = df3_2['month_processed'].astype(str)
        #st.line_chart(df3_2, x='month_processed')
        df_smear_join = df_smear_join.reset_index()
        
        df_smear_join.drop(['Not_Lowgrade', 'Low_Grade','total_samples','Z_test', 'TB_Detected','TB_Not_detected','total_smear','perc_negative'], axis='columns', inplace=True)
        df_smear_join['month_processed'] = df_smear_join['month_processed'].astype(str)
        st.line_chart(df_smear_join, x='month_processed')
        
        #st.write(df_smear_join)
        with st.expander('Key', expanded=True):
            st.write('''
                - Smear Lab data processed upto ''' + str(max(quarter_list)) + '''
    
                ''')   




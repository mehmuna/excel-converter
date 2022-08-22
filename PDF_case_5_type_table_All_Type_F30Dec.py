import warnings
from tika import parser # pip install tika
import os
import tabula
import pandas as pd
import numpy as np
import camelot
import re
import os
import glob
import collections
#import PDF_case_5_type_Part_1_F29DEC as part1
from PDF_case_5_type_Part_1_F30DEC import pdf_part_first
from PDF_case_5_type_9_7_1Jan2021 import pdf_part_first_9_7
from UseCase_5_type_6_8_F import type_img_6_8
#from Practices import addNumbers, multiplyNumbers
#from PDF_case_5_type_table_All_Type_F30Dec import pdf_part_first
#file_list=(glob.glob("D:/STCS/my_work/ComputerVision/Invoice_project/InvoiceProjectInput/usecase4/Input/*.pdf"))
#file_list=(glob.glob(r"Input/*.pdf"))
#file_list=(glob.glob(r"C:\Users\mubashir khan\OCRproject_Final\Input\*.pdf"))
#file_list=(glob.glob(r"C:\Users\mubashir khan\OCRproject_Final\InvoiceProjectInput1\usecase5\Input\*.pdf"))
file_list=(glob.glob(r"Input\*.pdf"))

try:

    for file_path in file_list:
            #file_path=(os.path.join(r,file))

        # PdfPath = file_path#'InvoiceProjectInput/usecase5/Input/Type-10/COC-95238-1-1.pdf'

            PdfPath = file_path#'InvoiceProjectInput/usecase5/Input/Type-10/COC-95238-1-1.pdf'




            print ("PdfPath-------",PdfPath)
            head, tail = os.path.split(PdfPath.strip())
            pdfName = tail.split(".")[0]
            print ("pdfName :",pdfName)
            raw = parser.from_file(PdfPath)
            PdfFile_convertText=raw['content'].strip()
            delText = re.sub(r'^https?:\/\/.*[\r\n]*', '', PdfFile_convertText, flags=re.MULTILINE)
            
            #print ("delText  ===",delText)
            if (len(delText.strip())<55):
                print ("file name is :  ",tail)
                try:
                    imagePart1,imagepart2=type_img_6_8(PdfPath,pdfName)
                    print ("imagePart1-----------")
                    print (imagePart1)
                    print ("imagePart2-----------")
                    print (imagepart2)
                    writer = pd.ExcelWriter('outPut_usecase5/'+pdfName+'.xlsx')
                    imagePart1.to_excel(writer,'Sheet1',encoding='utf-8-sig')
                    imagepart2.to_excel(writer,'Sheet2',encoding='utf-8-sig')
                    writer.save()
                    #break
                except:
                    pass

            #########################
            ########### call part1 file
            try:
                type_9_7=list (pdf_part_first_9_7(file_path,pdfName,PdfFile_convertText).columns)
                print ("type_9_7 ======= ",type_9_7)
                column_name_9_7=['Created_By', 'requestNo', 'Purchase_order', 'Order_Description','Budget', 'Receiving']
                if (collections.Counter(list (pdf_part_first_9_7(file_path,pdfName,PdfFile_convertText).columns))==collections.Counter(column_name_9_7)):

                    #part1_df=''
                    part1_df=pdf_part_first_9_7(file_path,pdfName,PdfFile_convertText)
                    print ("i am in type 9 and type 7 part condition")
            except:
                pass

            try:
                type_ALL=list (pdf_part_first(file_path,pdfName,PdfFile_convertText).columns)
                print ("type_ALL ======= ",type_ALL)
                column_name_9_7=['Created_By', 'requestNo', 'Purchase_order', 'Order_Description','Budget', 'Receiving']
                #if (collections.Counter(list (pdf_part_first(file_path,pdfName).columns))!=collections.Counter(column_name_9_7)):
                if ((type_ALL)==(column_name_9_7)):
                    pass
                else:
                    #part1_df=''
                    part1_df=pdf_part_first(file_path,pdfName,PdfFile_convertText)
                    print (" part-1,part-2,part-3,4,5,6,7,8,9,10     part-1,part-2,part-3,4,5,6,7,8,9,10==== ",list(part1_df.columns))
                    #print ("part1_df   ----------.....................................................",part1_df)
            except:
                pass



            #https://www.analyticsvidhya.com/blog/2020/08/how-to-extract-tabular-data-from-pdf-document-using-camelot-in-python/
            import camelot

            tables = camelot.read_pdf(PdfPath,flavor='stream', pages='all')


            number_of_table = len(tables)
            number_of_table

            def Empty_row_rmv(df1):
                for i , r in df1.iterrows():

                    #print(type (r['E']), (r['E']))
                    if (('Item ID' in r['E']) or ('Item ID' in r['B']) or ('Item ID' in r['C']) ):
                        #print (r)
                        df1 = df1.iloc[1:,:]
                    if ('Item ID' in r['B']):
                        print ("Item ID   ==",r['B'])
                        df1 = df1.iloc[1:,:]
                    if ((r["D"]=='') & (r["E"]=='')):
                        df1 = df1.iloc[1:,:]
                    if ('Receiving Details' in r['A']):
                        new_header = df1.iloc[0] #grab the first row for the header
                        #print ("new_header  use case 9 ===== ",new_header)
                        df1 = df1[1:] #take the data less the header row
                        #print ("df1----------9 case",df1)
                        df1.columns = new_header #set the header row as the df header
                        #print ("df1.columns  use case  ====",df1.columns)

                    return df1


            # In[ ]:





            # In[31]:


            def remove_empty_row_df(df,columnName):
                df[columnName].replace('', np.nan, inplace=True)
                df.dropna(subset=[columnName], inplace=True)
                return df


            # In[32]:


            def merge_row_D(df2,temp_df1_index_new,temp_lst_D):

                for j in temp_df1_index_new:
                    if (j==1):


                        #print (y,", i==",i,', j== ',j)
                        if(df2.loc[j,'D']):
                            #print (y,", i==",i,', j== ',j)
                            temp=df2.loc[j,'D']
                        if (not df2.loc[j+1,'E']):
                            #print ("hello",df2.loc[i+1,'D'])
                            temp_lst_D[j]=temp+" "+df2.loc[j+1,'D']

                    if (j>1):
                        if (df2.loc[j,'E']):
                            if(not df2.loc[j,'D']):

                                temp1=df2.loc[j-1,'D']

                                temp3=df2.loc[j+1,'D']
                                temp_lst_D[j]=temp1+" "+temp3
                            if (df2.loc[j,'D']):

                                temp1 = df2.loc[j-1,'D']
                                temp2=df2.loc[j,'D']

                                temp3=df2.loc[j+1,'D']
                                temp_lst_D[j]=temp1+" "+temp2+" " +temp3
                return temp_lst_D


            # In[33]:


            def map_Drow_Erow(mergeRow_Dict,df2_temp):
                for key, value in mergeRow_Dict.items():
                    df2_temp.loc[df2_temp.index == key, 'D'] = value
                return df2_temp


            # In[ ]:





            # In[34]:


            FinalDataFrame = pd.DataFrame([]) ## create DataFrame
            FinalDataFrame_tabula = pd.DataFrame([]) ## create DataFrame
            FinalDataFrame_1Col = pd.DataFrame([]) ## create DataFrame
            if (number_of_table==1):
                try:
                    #print ("number_of_table condition ===",number_of_table)
                    List_data = tabula.read_pdf(PdfPath,multiple_tables=True,pages="all") ## pages="all" use for extract table data all pages in pdf
                    df_tabula =List_data[0]
                    dict_df=df_tabula.to_dict('records')
                    #columnsName = ['A','B','C','D','E','F']
                    #dict_df.columns=columnsName
                    FinalDataFrame_tabula = FinalDataFrame_tabula.append(dict_df,ignore_index = True)
                except:
                    pass
            for i in range (1,number_of_table):
                #print ("i : ",i,", number_of_table  ==",number_of_table)
                df1=tables[i].df
                #print ("length of column :",len(df1.columns)," list of column daoud==",list (df1.columns))

            ######## condition for column len==1
                if (len(df1.columns)==1):
                    try:
                        #from dateutil.parser import parse
                        temp_list=[]
                        for i , r in df1.iterrows():
                            text = re.sub(r'^https?:\/\/.*[\r\n]*', '', r[0], flags=re.MULTILINE)
                            temp_list.append([text])
                        x=0
                        y=0
                        for i,ele in enumerate(temp_list):
                            if any("Item" in s for s in ele):
                                x=i
                                #print (i)
                            if any("Total" in s for s in ele):
                                y=i
                        temp=temp_list[x+1:y]
                        if (len(temp)==0):
                            List_data = tabula.read_pdf(PdfPath,multiple_tables=True,pages="all") ## pages="all" use for extract table data all pages in pdf
                            df_tabula =List_data[0]
                            dict_df=df_tabula.to_dict('records')

                            FinalDataFrame_tabula = FinalDataFrame_tabula.append(dict_df,ignore_index = True)

                        else:
                            dictData={}
                            list_A=[]
                            list_B=[]
                            list_C=[]
                            list_D=[]
                            list_E=[]
                            list_F=[]
                            temp_txt=[]
                            for i,ele in enumerate(temp):

                                temp_str=''.join(temp[i])
                                temp_str=temp_str.split()
                                #print (len(temp_str))
                                if (len(temp_str)<5):
                                    print (temp_str)
                                    temp_txt.append(' '.join(temp_str))
                                if (len(temp_str)>5):
                                    list_A.append(temp_str[0])
                                    list_B.append(temp_str[1])
                                    list_C.append(temp_str[2])
                                    list_D.append(' '.join(temp_str[3:-2]))
                                    list_E.append(temp_str[-2])
                                    list_F.append(temp_str[-1])

                            dictData['A']=list_A
                            dictData['B']=list_B
                            dictData['C']=list_C
                            dictData['D']=list_D
                            dictData['E']=list_E
                            dictData['F']=list_F
                            FinalDataFrame_1Col=pd.DataFrame(dictData)




                    except:
                        pass

                if (len(df1.columns)==6):
                    try:

                        columnsName = ['A','B','C','D','E','F']
                        df1.columns=columnsName
                        #print ("df1.columns ==",df1.columns)

                        df1=Empty_row_rmv(df1)
                        #print ("Hello------------------",list (df1.columns))
                        #print ("helo&&&&&&&&&&&&&&&&&&&&&&&&",df1.head())
                        if (list (df1.columns)==['Item Sequence','Item ID','Item Description','Unit Price','Item Quantity','Line Total']):
                            #print ("condition true ===========================================")
                            dict_df=df1.to_dict('records')
                            FinalDataFrame_tabula = FinalDataFrame_tabula.append(dict_df,ignore_index = True)
                            break
                        #df1_non_epty =remove_empty_row_df(df1,columnsName)

                        #temp=df1_non_epty['B'].isnull().sum()
                        #print ("df1_non_epty   ",temp)
                        # Start # select the one column and get the list of non empty row in df
                        temp_df1=df1[['E']]
                        before_procss=temp_df1.shape[0]
                        #print ("temp_df1.shape   == ",temp_df1.shape)
                        temp_df1 = remove_empty_row_df(temp_df1,'E')
                        temp_df1_index =list (temp_df1.index)## index list of non empty value column "E" ect.

                        ####### end #########
                        #print ("temp_df1  :",temp_df1.head())
                        #print ("temp_df1.shape After   == ",temp_df1.shape)
                        after_procss=temp_df1.shape[0]
                        if (after_procss==before_procss-1):

                            #print ("after_procss==before_procss-1")
                            index_list = list(temp_df1.index)
                            #print ("index_list  ===",index_list)
                            F_df =df1[df1.index.isin(index_list)] ## filter df from index values
                            F_df =Empty_row_rmv(F_df)
                            #print ("F_df   -- ",F_df.head())
                            dict_df=F_df.to_dict('records')
                            FinalDataFrame = FinalDataFrame.append(dict_df,ignore_index = True)
                            #FinalDataFrame.append(F_df) ## append dataframe
                        else:


                            ### process column "D" and Mearge the rows according column "E" condition
                            df2=df1.copy()
                            temp_df2=df1[['D']] ## filter column "D"
                            temp_df1_index_new= temp_df1_index ##remove last value due to last value , after that no more value
                            temp_df1_index_new=temp_df1_index[:-1]
                            temp_df1_index_new
                            temp_lst_D={}
                            mergeRow_Dict=merge_row_D(df2,temp_df1_index_new,temp_lst_D)
                            df2_temp=df2[["D","E"]]
                            df2_temp=map_Drow_Erow(mergeRow_Dict,df2_temp)
                            df2_temp=remove_empty_row_df(df2_temp,'E')
                            #print ("i  == ",i," , df2_temp == ",df2_temp)
                            df3=df2.copy()
                            df3=remove_empty_row_df(df3,'E')
                            df3=df3.drop(['D', 'E'], axis=1)
                            result_df = pd.concat([df3, df2_temp], axis=1, sort=False)
                            result_df =result_df[["A","B","C","D","E","F"]]
                            dict_df=result_df.to_dict('records')
                            FinalDataFrame = FinalDataFrame.append(dict_df,ignore_index = True)
                            #print ("i  ===",i,"  ,last line-------------------result_df   =",result_df.head())
                            #FinalDataFrame.append(result_df)


                    except:
                        pass



            # In[35]:


            FinalDataFrame


            # In[36]:



            FinalDataFrame1 = Empty_row_rmv(FinalDataFrame)
            Final_df_len=len(FinalDataFrame)
            FinalDataFrame1


            # In[37]:


            print (FinalDataFrame_tabula.shape[0])
            tabula_df_len=len(FinalDataFrame_tabula)
            #print ("type FinalDataFrame_tabula",type (FinalDataFrame_tabula))
            FinalDataFrame_tabula


            # In[38]:


            df_1col_len=len(FinalDataFrame_1Col)
            FinalDataFrame_1Col


            # In[39]:


            FinalDataFrame=FinalDataFrame_1Col.copy()


            # In[40]:


            def final_col_name(df_F):
                FinalDataFrame=df_F
                FinalDataFrame.iloc[:,0] = FinalDataFrame.iloc[:,0].str.replace(",","").astype(float)
                #print ("dtypes :",FinalDataFrame.dtypes)
                sum_column=FinalDataFrame.iloc[:,0].sum()
                addNew_row=[sum_column,'','','','','Total']
                df_new_line = pd.DataFrame([addNew_row], columns=list(FinalDataFrame.columns) )
                df_Final = pd.concat([FinalDataFrame,df_new_line], ignore_index=True)
                dct = {'A':'المجموع', 'B':'الکمیة','C':'سعر الوحدة','D':'وصف العنصر', 'E':'Item ID','F':'رقم العنصر'}
                Col_Names= list(df_Final.columns)
                df_Final.columns= map(dct.get, Col_Names)
                return df_Final


            # In[ ]:





            # In[41]:


            if (df_1col_len!=0):
                try:

                    df_F=FinalDataFrame_1Col.copy()
                    if ('Item ID' in list(df_F.columns)):
                        print (df_F.columns)
                    else:
                        df_F=final_col_name(df_F)
                        #print ("first else condition", type(df_F))
                        writer = pd.ExcelWriter('outPut_usecase5/'+pdfName+'.xlsx')
                        part1_df.to_excel(writer,'Sheet1',encoding='utf-8-sig')
                        df_F.to_excel(writer,'Sheet2',encoding='utf-8-sig')
                        writer.save()
                except:
                    pass


            # In[42]:


            if (tabula_df_len!=0):
                try:

                    df_F=FinalDataFrame_tabula.copy()
                    if ('Item ID' in list(df_F.columns)):
                        writer = pd.ExcelWriter('outPut_usecase5/'+pdfName+'.xlsx')
                        part1_df.to_excel(writer,'Sheet1',encoding='utf-8-sig')
                        df_F.to_excel(writer,'Sheet2',encoding='utf-8-sig')
                        writer.save()
                        #print (df_F.columns)
                    else:
                        print (df_F)
                except:
                    pass



            # In[43]:


            if (Final_df_len!=0):
                try:

                    df_F=FinalDataFrame1.copy()
                    if ('Item ID' in list(df_F.columns)):
                        print (df_F.columns)
                    else:
                        df_F=final_col_name(df_F)
                        #print (" last else condition",df_F)
                        writer = pd.ExcelWriter('outPut_usecase5/'+pdfName+'.xlsx')
                        part1_df.to_excel(writer,'Sheet1',encoding='utf-8-sig')
                        df_F.to_excel(writer,'Sheet2',encoding='utf-8-sig')
                        writer.save()
                except:
                    pass
except:
        
    #except:
    #print ("pdfName :",pdfName)
    print ("Sorry i could not process this file last  ===== ", pdfName)

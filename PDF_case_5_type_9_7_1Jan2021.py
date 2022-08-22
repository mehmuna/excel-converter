import warnings
from tika import parser # pip install tika
import pandas as pd
import numpy as np

import os
import re
def pdf_part_first_9_7(file_path,pdfName,PdfFile_convertText):


    PdfPath = file_path#'InvoiceProjectInput/usecase5/Input/Type-10/COC-95238-1-1.pdf'
    print ("PdfPath   fifferent file",PdfPath)
    #head, tail = os.path.split(PdfPath.strip())
    #pdfName = tail.split(".")[0]
    #print ("pdfName :",pdfName)

    #raw = parser.from_file(PdfPath)
    ##https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
    import re

    txtFilePath='InvoiceProjectInput/usecase5/txtFileOutput_2/'
    text_file = open(txtFilePath+pdfName+".txt", "w",encoding='utf-8')
    n = text_file.write(PdfFile_convertText)
    text_file.close()
    import re
    itemList=[]
    serhWord_index=[]
    serhWord_name=[]
    searchKeyWord=['موافق']
    file1 = open(txtFilePath+pdfName+".txt", 'r',encoding='utf-8')
    Lines = file1.readlines()
    #print ("Lines: ",len(Lines))
    count = 0
    # Strips the newline character
    for line in Lines:

        #print("Line{}: {}".format(count, line.strip()))
        Eng_lineNumber = format(count)
        string_data = format(line.strip())
        if (3<len(string_data)<60):
            itemList.append(string_data)




        count= count+1
    filter_item=[]
    key_pdf=[]

    ######################################
    flag1=0
    flag2=0
    for count,ele in enumerate (itemList):

        if (('عملة الفاتورة' in ele)):
            flag1=1
            print ("yes")
        if ('التلخیص' in ele):
            flag2=1
            print ("second if")

        else:
            pass
    ################################
    if (flag1==0 & flag2==0):
        for count,ele in enumerate (itemList):

            if ('RRP' in ele):
                #print ("ele first length==: ",len(ele)," length== ",ele)
                if (len(ele)>3):
                    Receiving=ele
                    Receiving=Receiving.split()

                    Receiving = [i for i in Receiving if 'RRP' in i] ## filter item by substring
                    Receiving=''.join(Receiving)
                    #print ("Receiving   =",Receiving)
                    regex = re.compile('[^a-zA-Z0-9]')
                    Receiving=regex.sub(' ', Receiving.strip())

                    #print ("Receiving  ",Receiving)
                    filter_item.append(Receiving.strip())
                    key_pdf.append("Receiving")


            if ('APPROVED' in ele):
                Created_By = ele.replace("APPROVED","") ## remove the "APPROVED" from string
                #print ("Created_By----------------",Created_By)
                filter_item.append(Created_By)
                key_pdf.append ("Created_By")
                requestNo=itemList[count+1]
                requestNo=requestNo.split()[0]
                #print ("requestNo      ===  ",requestNo)
                filter_item.append(requestNo)
                key_pdf.append("requestNo")

            if ('BLANKET' in ele):
                #print ("ele first  BLANKET : ",ele)
                if (len("BLANKET")<len(ele)):
                    temp=ele.split()
                    Purchase_order=temp[0]
                    print ("Purchase_order   ---",Purchase_order)

                    Order_Description= temp[1:-1]
                    Order_Description = ' '.join(Order_Description)
                    print ("Order_Description   ---",Order_Description)
                    filter_item.append(Purchase_order)
                    key_pdf.append("Purchase_order")
                    filter_item.append(Order_Description)
                    key_pdf.append("Order_Description")
                    #print (temp)
                index_1=count+1
                if (len(ele)>3):

                    Budget=itemList[index_1]
                    Budget=Budget.split()[0]
                    #print ("Budget  :",Budget)
                    filter_item.append(Budget)
                    key_pdf.append("Budget")
                if (len("BLANKET")==len(ele)):
                    Order_Description = itemList[count-2]+" "+itemList[count-1]
                    #print ("Order_Description   --",Order_Description)
                    Purchase_order= itemList[count-3]
                    #print ("Purchase_order  ====",Purchase_order)
                    filter_item.append(Purchase_order)
                    key_pdf.append("Purchase_order")
                    filter_item.append(Order_Description)
                    key_pdf.append("Order_Description")


        try:


            a,b,c,d,e,f = filter_item
            a,b,c,d,e,f= [str(e) for e in [a,b,c,d,e,f]]
            a=[a];b=[b];c=[c];d=[d];e=[e];f=[f]
            df_firstPart = pd.DataFrame(list (zip(a,b,c,d,e,f)),columns =key_pdf)
            #if (list (df_firstPart.columns))==()
        except:
            pass
    else:
        df_firstPart=''


    # In[120]:




    return df_firstPart


# In[ ]:

import warnings
from tika import parser # pip install tika
import pandas as pd
import numpy as np

import os
import re
def pdf_part_first(file_path,pdfName,PdfFile_convertText):


    PdfPath = file_path#'InvoiceProjectInput/usecase5/Input/Type-10/COC-95238-1-1.pdf'
    #print ("PdfPath   fifferent file",PdfPath)
    #head, tail = os.path.split(PdfPath.strip())
    #pdfName = tail.split(".")[0]
    #print ("pdfName :",pdfName)

    #raw = parser.from_file(PdfPath)
    ##https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
    import re

    txtFilePath='InvoiceProjectInput/usecase5/txtFileOutput_1/'
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
    #itemList_1=list(set(itemList))
    try:

        filter_item=[]
        for count,ele in enumerate (itemList):
            if ('RRP' in ele):
                #print ("ele first length==: ",len(ele)," length== ",ele)
                if (len(ele)>3):
                    #print ("ele   =",ele)
                    filter_item.append(ele)

            if ('عملة الفاتورة' in ele):## these for type-3,10
                temp=itemList[count+1]
                if ((temp[:1].isdigit() == True) & (temp[:2].isdigit() == True) & (temp[:3].isdigit() == True) & (temp[:4].isdigit() == True)):
                    #print ("itemList[count+1] +^^^^^^",itemList[count+1])
                    filter_item.append("@"+itemList[count+1])

            if ('Project Duration' in ele): ## these for type-3 ,10
                temp=itemList[count+1]
                print ("Project Duration  ----")
                if ((temp[:1].isdigit() == True) & (temp[:2].isdigit() == True) & (temp[:3].isdigit() == True) & (temp[:4].isdigit() == True)):
                    filter_item.append("@"+itemList[count+1])
            if ('قطاع التطبیقات' in ele):## these for type-3 ,10
                temp=itemList[count+1]
                if ((temp.isdigit()== True)):

                    #print ("ele.isdigit()== True======= and length==4 ===",itemList[count],",    ", len(itemList[count]))
                    if ((len(temp)==4)):
                        if (re.match('^[1-9]*$',temp)):## check numric string does not contain 0
                            filter_item.append(temp)


            if ('التلخیص' in ele):
                #print ("ele first التلخیص: ",ele, "count التلخیص ::",count, ", itemList  ==",itemList[count+3])
                filter_item.append(itemList[count-1])
                if (re.match("^[A-Za-z0-9 ]*$",itemList[count-2] )): ## "my_little_string",this is used to check if the string is English or non english
                    #print ("itemList[count-2]  -------------------------------------------  :",itemList[count-2])
                    filter_item.append(itemList[count-2])
                else:
                    string = itemList[count+1]
                    if ('APPROVED' in string):
                        string = string.replace("APPROVED","") ## remove the "APPROVED" from string
                        filter_item.append(string)

                filter_item.append(itemList[count-3])
                filter_item.append(itemList[count+3])
                index_1=count+3
                if (len(ele)>3):
                    #print ("itemList[index_1]:",itemList[index_1])
                    filter_item.append(itemList[index_1])
                        #filter_item.append(itemList[index_1])
            if (('عملیة رقم' in ele) or ('التلخیص') in ele):
                #print ("itemList[count+4]   : ",itemList[count+4])
                temp_list=[]
                if ('عملیة رقم' in ele):
                    #print ("عملیة رقم in line first: ",ele)
                    temp_list.append(ele)
                    index_1=count+1
                    temp_list.append(itemList[index_1])
                    #print ("temp_list :",temp_list)
                    index_1=count+2
                else:
                    temp_list.append(itemList[count+4])
                    index_1=count+4+1
                    temp_list.append(itemList[index_1])
                    #print ("temp_list :",temp_list)
                    index_1=count+4+2


                if (itemList[index_1]=='BLANKET'):
                    pass
                else:
                    temp_list.append(itemList[index_1])
                teamp_word=''.join(temp_list)
                #print ("teamp_word ::",teamp_word)
                teamp_word=teamp_word.strip("- ")
                filter_item.append((teamp_word))
            if ('BLANKET' in ele):
                #print ("ele first  BLANKET : ",ele)
                index_1=count+1
                if (len(ele)>3):
                    #print ("itemList[index_1]:",itemList[index_1])
                    filter_item.append(itemList[index_1])

    except:
        pass


    #################################################33


    filter_ItemList=filter_item
    filter_ItemList


    # In[618]:


    filter_ItemList= set(filter_item)
    filter_ItemList=list(filter_ItemList)
    filter_ItemList.sort()
    #print (filter_ItemList)
    #s = s.replace(',', '')
    filter_ItemList_new=[]
    for ele in filter_ItemList:
        ele = ele.replace(',', '')
        filter_ItemList_new.append(ele)
        #print (ele)
    filter_ItemList=filter_ItemList_new
    filter_ItemList


    latgest_string = (max(filter_ItemList , key = len)) ## check the largest string  in list
    #print ("latgest_string length :",len (latgest_string))
    #print ("latgest_string  :",(latgest_string))
    latgest_string_index=filter_ItemList.index(latgest_string) # get index of largest string
    #print ("latgest_string_index ::",latgest_string_index)


    if (latgest_string[0].isdigit()==True):



        data = [latgest_string]

        def is_valid_date(date_str):
            try:
                parser.parse(date_str)
                return True
            except:
                return False

        update_list_ele = [' '.join([w for w in line.split() if not is_valid_date(w)]) for line in data]
        update_list_ele = ''.join(update_list_ele)
        #print("update_list_ele == ",update_list_ele)
        filter_ItemList[latgest_string_index]=update_list_ele
        #print ("filter_ItemList  :",filter_ItemList)

        ################# Recheck the largest list again after operations
        latgest_string = (max(filter_ItemList , key = len)) ## check the largest string  in list
        #print ("latgest_string length :",len (latgest_string))
        #print ("latgest_string  :",(latgest_string))
        latgest_string_index=filter_ItemList.index(latgest_string) # get index of largest string
        #print ("latgest_string_index ::",latgest_string_index)

    import re
    final_ItemList=[]
    month_list=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
    temp_counter=[]
    Num_temp_counter=[]
    word_list=[] # map original word value(copy from pdf) that we extract from program
    largest_list =len((max(filter_ItemList , key = len))) ## check the largest string len in list
    temp_list= list(range(0, len(filter_ItemList)))
    for count,ele in enumerate (filter_ItemList):
        ## start # condition for only extract the alphabet string
        temp = ele.replace(" ", "")
        temp=temp.strip()
        temp = temp.isalpha()
        if (temp == True):
            #print ("filter_ItemList[count]===%%%",filter_ItemList[count])#اسم الموظف(بالعربي)
            final_ItemList.append(filter_ItemList[count])
            temp_counter.append(count)
            word_list.append("اسم الموظف(بالعربي)")


        if ((len(ele) <10)):
            #print ("ele ----------- :", ele, ", count -------- :",count)
            #print (" filter_ItemList[count]   <10 ====&&&& ",filter_ItemList[count])

            if ("@" in filter_ItemList[count]):
                word_list.append("رقم الموظف")
                number = re.search(r'\d+', filter_ItemList[count]).group()
                #print ("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@== ",filter_ItemList[count])
                final_ItemList.append(number)
            else:
                final_ItemList.append(filter_ItemList[count])

            if ((filter_ItemList[count].isdigit() == True)):
                #print ("----------*************** filter_ItemList[count].isdigit() ******",filter_ItemList[count])



                Num_temp_counter.append(count)

                if (len(Num_temp_counter)==1):
                    #print ("Num_temp_counter^^^^^ ",filter_ItemList[count],"  ,",Num_temp_counter, ", length = ",len(Num_temp_counter))
                    word_list.append("رقم التقریر") ## for 145555  add key bez 2 condition execute at atime
                if (len(Num_temp_counter)==2):
                    #print ("Num_temp_counter^^^^^ ",filter_ItemList[count],"  ,",Num_temp_counter, ", length = ",len(Num_temp_counter))
                    if (len(filter_ItemList[count])==4):
                        word_list.append("الإدارة العامة")#append("اإلدارة العامة")

                    word_list.append("رقم اتفاقیة الشراء") #for 92336  add key  bez 2 condition execute at atime
            else:
                match = re.search("\d",filter_ItemList[count])

                if (match.start(0)==1):
                    if (not "@" in filter_ItemList[count]):

                        #print ("filter_ItemList[count]  رقم الموظف ele condition  ==",filter_ItemList[count])
                        word_list.append("رقم الموظف")
                        final_ItemList.append(filter_ItemList[count])
                    #print ("yes")
                else:
                    pass
                    #print ("no")



            temp_counter.append(count)
            #word_list.append("رقم التقریر")
        if ((ele[:1].isdigit() == True) & (ele[:2].isdigit() == True) & (len(ele)>12)):
            engWord=format(line.strip())
            input_string = filter_ItemList[count]
            #print ("input_string := ",input_string)
            engWord = re.findall('([0-9. ]*)\W*.*', input_string) ## use for filter the numaric value before alphabet in string
            engWord =''.join(engWord)
            #print ("engWord  price --------------------------------------::::= ",engWord,",  length ====",len(engWord))
            if (len(engWord)>5):
                #print ("------------------------------------- len(engWord)>5==== ")

                final_ItemList.append(engWord)
                temp_counter.append(count)
                word_list.append("میزانیة اتفاقیة الشراء")
            else:
                final_ItemList.append(engWord)
                temp_counter.append(count)
                word_list.append("رقم اتفاقیة الشراء")

            #final_ItemList.append(filter_ItemList[count])
        if (("BLANKET" in ele) & (len(ele)>15)):
            engWord = ele.lstrip('0123456789.- ')## remove numric value at beggining of string
            final_ItemList.append(engWord)
            word_list.append("وصف اتفاقیة الشراء")
            #print ("BLANKET line ele ------------------------: ", engWord, ", ele  == ", len(ele))


        if ("RRP" in ele):
            #print ("ele length == ",len(ele))
            engWord=format(filter_ItemList[count].strip())
                #print ("engWord: ",engWord)
            temp_regex=re.sub('\W', ' ', engWord)


            for item in temp_regex.split():
                if len(item)>7:
                    #print ("item > 7",item)
                    temp_item=item
                    temp_item = [i.split('\t', 1)[0] for i in temp_item]
                    temp_item=temp_item[-10:]
                    engWord = ''.join(temp_item)
                    #print ("engWord if len(item)>7: -------  ===++ ",engWord)
                    final_ItemList.append(engWord)
                    word_list.append("محضر إستلام")
                    temp_counter.append(count)


        if (("عملیة رقم" in ele) or (count==latgest_string_index)):
            #print ("latgest_string_index  ::::::::::::::::::::::::",latgest_string_index)
            if (("عملیة رقم" in ele)):
                #print ("عملیة رقم   : ",ele,", count max: ",count)
                engWord=format(filter_ItemList[count].strip())
                regex = re.compile('[^a-zA-Z0-9]')
                engWord=regex.sub(' ', engWord.strip())
                engWord =re.sub(r' +', ' ', engWord) ## remove extra space between wor from string in
                final_ItemList.append(engWord)
                word_list.append("وصف اتفاقیة الشراء")
                #print ("engWord if ((عملیة رق in ele)):  --------",engWord)
            else:
                item_len=[(i)  for i in month_list if i in ele]
                if (len(item_len)==0):

                    #print ("عملیة رقم   : ",ele,", count max: ",count)
                    engWord=format(filter_ItemList[count].strip())
                    regex = re.compile('[^a-zA-Z0-9]')
                    engWord=regex.sub(' ', engWord.strip())
                    engWord =re.sub(r' +', ' ', engWord) ## remove extra space between wor from string in
                    #print ("engWord    MMMMMMax string :",engWord)
                    if ("RRP" in engWord):
                        pass
                    else:
                        final_ItemList.append(engWord)
                        word_list.append('وصف اتفاقیة الشراء')


    string_list=final_ItemList # remove the substring from sting other element
    final_ItemList_F=filter(lambda x: [x for i in string_list if x in i and x != i] == [], string_list)
    final_ItemList_F=list(final_ItemList_F)
    final_ItemList_F

    final_ItemList_F = list(dict.fromkeys(final_ItemList_F)) # remove dublicate part one
    word_list  = list(dict.fromkeys(word_list)) # remove dublicate part one
    ##################  PART- 2 Code Start , Tabular Data ##############################################################################################
    ##################  PART- 2 Code Start , Tabular Data ##############################################################################################
    ##################  PART- 2 Code Start , Tabular Data ##############################################################################################



    #########################################################################################
    ##############################################################
    try:

        a,b,c,d,e,f,g,h = final_ItemList_F
        a,b,c,d,e,f,g,h= [str(e) for e in [a,b,c,d,e,f,g,h]]
        a=[a];b=[b];c=[c];d=[d];e=[e];f=[f];g=[g];h=[h]
        df_firstPart = pd.DataFrame(list (zip(a,b,c,d,e,f,g,h)),columns =word_list)
        #return df_firstPart
    except:
        pass
    try:
        a,b,c,d,e,f,g = final_ItemList_F
        a,b,c,d,e,f,g= [str(e) for e in [a,b,c,d,e,f,g]]
        a=[a];b=[b];c=[c];d=[d];e=[e];f=[f];g=[g]
        df_firstPart = pd.DataFrame(list (zip(a,b,c,d,e,f,g)),columns =word_list)
        #return df_firstPart
    except:
        pass
    return df_firstPart

"""

    print ("df_firstPart ===== ",df_firstPart)
    writer = pd.ExcelWriter(r+'/output/'+pdfName+'.xlsx')
    df_firstPart.to_excel(writer,'Sheet1',encoding='utf-8-sig')
    #df_Final.to_excel(writer,'Sheet2',encoding='utf-8-sig')
    writer.save()
except :
    pass
try:


    a,b,c,d,e,f,g = final_ItemList_F
    a,b,c,d,e,f,g= [str(e) for e in [a,b,c,d,e,f,g]]
    a=[a];b=[b];c=[c];d=[d];e=[e];f=[f];g=[g]
    df_firstPart = pd.DataFrame(list (zip(a,b,c,d,e,f,g)),columns =word_list)
    writer = pd.ExcelWriter(r+'/output/'+pdfName+'.xlsx')
    df_firstPart.to_excel(writer,'Sheet1',encoding='utf-8-sig')
    #df_Final.to_excel(writer,'Sheet2',encoding='utf-8-sig')
    writer.save()
except:
    pass
"""

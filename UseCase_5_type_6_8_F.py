#https://towardsdatascience.com/a-table-detection-cell-recognition-and-text-extraction-algorithm-to-convert-tables-to-excel-files-902edcf289ec
#import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

#from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from tika import parser # pip install tika
import tabula

def type_img_6_8(PdfPath,pdfName):


    #PdfPath = 'InvoiceProjectInput/usecase5/Input/Type-6/COC-94059-1-1.pdf'
    #print ("PdfPath---imgfile =====",PdfPath)
    #head, tail = os.path.split(PdfPath.strip())
    #print ("imgfile =====",PdfPath)
    #pdfName = tail.split(".")[0]
    #print ("pdfName :",pdfName)
    outputpath="img_outPut/" ## pdf convert into image folder
    txt_file="txt_folder/" ## image to txt file folder
    #remove files from folder
    import os
    import shutil
    from pdf2jpg import pdf2jpg
    def removeFile_from_folder(folder):

        for root, dirs, files in os.walk(folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    try:
        removeFile_from_folder(outputpath)
    except:
        pass
    try:
        removeFile_from_folder(txt_file)
    except:
        pass


    # In[73]:


    result = pdf2jpg.convert_pdf2jpg(PdfPath, outputpath, pages="ALL") ## convert pdf to image


    # In[74]:


    result


    # In[75]:


    result[0].keys()


    # In[76]:


    tempPath=result[0].get('output_jpgfiles')
    #tempPath = ''.join(tempPath)
    tempPath


    # In[77]:


    ## adjust the file name
    for i in tempPath:

        head, tail = os.path.split(i.strip())
        temp=tail.split(".")
        print ("temp== ",temp)
        temp.remove("pdf")
        print ("temp== ",temp)
        temp = '.'.join(temp)
        print ("temp== ",temp)
        os.rename(i,'img_outPut/'+temp)


    # In[78]:


    #remove all data from
    import shutil
    shutil.rmtree(head)


    # In[79]:


    ## check list of file
    import glob
    file_list=(glob.glob(outputpath+"*.jpg"))
    file_list

    def type6_8_part2(file,df_part2):
        img = cv2.imread(file,0)
        #thresholding the image to a binary image
        thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        #inverting the image
        img_bin = 255-img_bin
        #cv2.imwrite(file_path+'cv_inverted.png',img_bin)
        #Plotting the image to see the output
        #plotting = plt.imshow(img_bin,cmap='gray')
        #plt.show()
        # Length(width) of kernel as 100th of total width
        kernel_len = np.array(img).shape[1]//100
        # Defining a vertical kernel to detect all vertical lines of image
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        # Defining a horizontal kernel to detect all horizontal lines of image
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        #Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
        #cv2.imwrite(file_path+"vertical.jpg",vertical_lines)
        #Plot the generated image
        #plotting = plt.imshow(image_1,cmap='gray')
        #plt.show()
        #Use horizontal kernel to detect and save the horizontal lines in a jpg
        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
        #cv2.imwrite(file_path+"horizontal.jpg",horizontal_lines)
        #Plot the generated image
        #plotting = plt.imshow(image_2,cmap='gray')
        #plt.show()
        # Combine horizontal and vertical lines in a new third image, with both having same weight.
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        #Eroding and thesholding the image
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #cv2.imwrite(file_path+"img_vh.jpg", img_vh)
        bitxor = cv2.bitwise_xor(img,img_vh)
        bitnot = cv2.bitwise_not(bitxor)
        #Plotting the generated image
        #plotting = plt.imshow(bitnot,cmap='gray')
        #plt.show()
        # Detect contours for following box detection
        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        def sort_contours(cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
            reverse = False
            i = 0
            # handle if we need to sort in reverse
            if method == "right-to-left" or method == "bottom-to-top":
                reverse = True
            # handle if we are sorting against the y-coordinate rather than
            # the x-coordinate of the bounding box
            if method == "top-to-bottom" or method == "bottom-to-top":
                i = 1
            # construct the list of bounding boxes and sort them from top to
            # bottom
            boundingBoxes = [cv2.boundingRect(c) for c in cnts]
            (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
            key=lambda b:b[1][i], reverse=reverse))
            # return the list of sorted contours and bounding boxes
            return (cnts, boundingBoxes)

        # Sort all the contours by top to bottom.
        contours, boundingBoxes = sort_contours(contours, method='top-to-bottom')
        #Creating a list of heights for all detected boxes
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        #Get mean of heights
        mean = np.mean(heights)

        #(w<100 and h<500) need to be change these value its depend on file size
        #Create list box to store all boxes in
        box = []
        # Get position (x,y), width and height for every contour and show the contour on image
        for c in contours:

            x, y, w, h = cv2.boundingRect(c)
            if (w<1000 and h<2000):#w<1000 and h<2000--usecase-6
                image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                box.append([x,y,w,h])
        #plotting = plt.imshow(image,cmap='gray')
        #plt.show()

        #Creating two lists to define row and column in which cell is located
        row=[]
        column=[]
        j=0
        #Sorting the boxes to their respective row and column
        for i in range(len(box)):
            if(i==0):
                column.append(box[i])
                previous=box[i]
            else:
                if(box[i][1]<=previous[1]+mean/2):
                    column.append(box[i])
                    previous=box[i]
                    if(i==len(box)-1):
                        row.append(column)
                else:
                    row.append(column)
                    column=[]
                    previous = box[i]
                    column.append(box[i])
        #print(column)
        #print(row)
        #calculating maximum number of cells
        countcol = 0
        for i in range(len(row)):
            countcol = len(row[i])
            if countcol > countcol:
                countcol = countcol
        #Retrieving the center of each column
        center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center=np.array(center)
        center.sort()


        #Regarding the distance to the columns center, the boxes are arranged in respective order
        finalboxes = []
        for i in range(len(row)):
            lis=[]
            for k in range(countcol):
                lis.append([])
            for j in range(len(row[i])):
                diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
                minimum = min(diff)
                indexing = list(diff).index(minimum)
                lis[indexing].append(row[i][j])
            finalboxes.append(lis)

        #from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        outer=[]
        for i in range(len(finalboxes)):
            for j in range(len(finalboxes[i])):
                inner=''
                if(len(finalboxes[i][j])==0):
                    outer.append(' ')
                else:
                    for k in range(len(finalboxes[i][j])):
                        y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                        finalimg = bitnot[x:x+h, y:y+w]
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                        border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                        resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                        dilation = cv2.dilate(resizing, kernel,iterations=1)
                        erosion = cv2.erode(dilation, kernel,iterations=1)


                        out = pytesseract.image_to_string(erosion)
                        if(len(out)==0):
                            out = pytesseract.image_to_string(erosion, config='--psm 3')
                        inner = inner +" "+ out
                    outer.append(inner)

        #Creating a dataframe of the generated OCR list
        arr = np.array(outer)
        dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
        #print(dataframe)
        #data = dataframe.style.set_properties(align="left")
        df_part2=dataframe
        return df_part2


    # In[82]:


    ## make the structures data for type-6 and dataframe
    def final_df_type_6(df,dictData_DF):
        dictData={}
        Item_sequence_L=[]
        Item_ID_L=[]
        Item_Description_L=[]
        Line_total_L=[]
        item_Quantity_L=[]

        df_0 =df.iloc[:,[0]]
        for i , r in df_0.iterrows():
            list_rows= (df_0.iloc[i,0])
            text = re.sub('[^0-9 ]', '', list_rows)
            text =text.strip()
            print ("text=== ",text,len(text))
            if (len(text)!=0):
                Item_sequence_L.append(text)
        ########### second column
        df_1 =df.iloc[:,[1]]

        for i , r in df_1.iterrows():


            list_rows= (df_1.iloc[i,0])
            text = re.sub('[^0-9 ]', '', list_rows)
            text =text.strip()
            print ("text=== ",text,len(text))
            if (len(text)!=0):
                Item_ID_L.append(text)
        ################# third column
        df_3 =df.iloc[:,[2]]

        for i , r in df_3.iterrows():

            my_str = r #"| (hey) \n\n th..~!ere20"
            list_rows= (df_3.iloc[i,0])
            if (i==0):
                list_rows= (df_3.iloc[i,0])
                text = re.sub('[^a-zA-Z ]', '', list_rows)
                #list_rows =list_rows.strip()
                Item_Description = text[text.find('Item Description') + len("Item Description"): ]
                if (len(Item_Description)!=0):
                        Item_Description_L.append(Item_Description.strip())

                #print (text)
                numaric = re.sub('[^0-9 ]', '', list_rows)
                numaric= numaric.split()
                item_Quantity =numaric[0]
                item_Quantity_L.append(item_Quantity)
                Line_total =numaric[1]
                Line_total_L.append(Line_total)

            else:
                if (len((df_3.iloc[i,0]))!=0):


                    list_rows= (df_3.iloc[i,0])
                    text = re.sub('[^a-zA-Z ]', '', list_rows)
                    text =text.strip()
                    Item_Description = text#[text.find('Item Description') + len("Item Description"): ]
                    if (len(Item_Description)!=0):
                        Item_Description_L.append(Item_Description)
                    print (text)
                    numaric = re.sub('[^0-9 ]', '', list_rows)
                    numaric= numaric.split()
                    print (numaric)
                    if (len(numaric)==2):

                        item_Quantity =numaric[0]
                        item_Quantity_L.append(item_Quantity)
                        Line_total =numaric[1]
                        Line_total_L.append(Line_total)
        dictData['Item_sequence']=Item_sequence_L
        dictData['Item_ID']=Item_ID_L
        dictData['Item_Description']=Item_Description_L
        dictData['item_Quantity']=item_Quantity_L
        dictData['Line_total']=Line_total_L
        dictData_DF=pd.DataFrame(dictData)
        return dictData_DF


    # In[83]:


    ######## ## make the structures data for type-8 and  dataframe
    def final_df_type_8(df,dictData_DF):

        df_new =df.iloc[:,[0,1]]
        dictData={}
        tableData=[]
        totalData=[]
        list_data_Char=[]
        list_data_0=[]
        list_data_1=[]
        list_data_2=[]
        list_data_3=[]
        data_list=[]
        char_list=[]

        for i , r in df_new.iterrows():

            my_str = r #"| (hey) \n\n th..~!ere20"
            list_rows= (df_new.iloc[i,1])

            list_rows = re.sub('[^a-zA-Z0-9 () ]', '', list_rows)
            list_rows =list_rows.strip()
            if (len(list_rows)!=0):
                if ('Total' in list_rows):
                    totalData.append(list_rows)
                else:

                    list_rows=list_rows[list_rows.find('19980') + 1: ]
                    print ("i=== ",i," ,      ===, ",list_rows)
                    tableData.append(list_rows)


        for count, value in enumerate(tableData):


            list_item= tableData[count].split()
            len_list= len(list_item)
            #list_data_Char.append(len_list-3)
            temp_index=len_list-3

            char_list.append(list (range(1,temp_index)))
            temp_a=list (range(1,temp_index))
            x=itemgetter(*temp_a)(list_item)

            list_data_Char.append(x)
            list_data_0.append(list_item[0])
            list_data_1.append(list_item[-1])
            list_data_2.append(list_item[-2])
            list_data_3.append(list_item[-3])


        dictData['Item ID']=list_data_0
        dictData['المجموع']=list_data_1
        dictData['وصف العنصر']=list_data_Char
        dictData['سعر الوحدة']=list_data_3
        dictData['الكمية']=list_data_2


        dictData_DF=pd.DataFrame(dictData)
        return dictData_DF

    from operator import itemgetter
    df_part2=''
    dictData_DF=''
    flag_img=0
    for file in file_list:

        try:
            df_part2=type6_8_part2(file,df_part2)
            print ("file==== ",file, len(df_part2.columns))
            if (len(df_part2.columns)==3):

                try:
                    flag_img=1
                    print ("flag_img==",flag_img)
                    dictData_DF=final_df_type_6(df_part2,dictData_DF)
                    os.remove(file)

                except:
                    pass
            if (len(df_part2.columns)==2):
                try:
                    flag_img=2
                    dictData_DF=final_df_type_8(df_part2,dictData_DF)
                    print ("flag_img==",flag_img)
                except:
                    pass

        except:
            pass
    #file=r'C:\Users\Daoud\Documents\project\akram_project\Invoice_usecases\Data_code\Final\Img_UseCase3\Code\pdf_convert_img_output\8.jpg'


    # In[89]:


    ################# OCR -- IMAGE to txt
    def part_1_img_txt(file,outputpath,txt_file,itemList):
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename = "{}.jpg".format(os.getpid())
        head, tail = os.path.split(file.strip())
        pdfName = tail
        print ("pdfName if  :",pdfName)
        filename_new=pdfName[:-4]+'_gray.jpg'
        print (" filename_new ",filename_new)
        cv2.imwrite(outputpath+filename_new, gray)
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        text= pytesseract.image_to_string(Image.open(outputpath+filename_new), lang='eng')
        new_file_name = filename_new[:-4]
        print("new_file_name:  ",new_file_name)
        new_file_name = new_file_name
        print ("new_file_name update == ",new_file_name)
        text_file_path = new_file_name + '.txt'
        text_file = open(txt_file+text_file_path, "w+")
        text_file.write("%s" % text)
        text_file.close()
        #itemList=[]
        searchKeyWord=['موافق']
        file1 = open(txt_file+text_file_path, 'r',encoding='cp1252')
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
        return itemList


    # In[90]:


    def part_1_type8(filter_item,key_pdf,itemList):

        for count,ele in enumerate (itemList):
            if ('RRP' in ele):
                #print ("ele first length==: ",len(ele)," length== ",ele)
                if (len(ele)>3):
                    Receiving=ele
                    Receiving=Receiving.split()

                    Receiving = [i for i in Receiving if 'RRP' in i] ## filter item by substring
                    Receiving=''.join(Receiving)
                    print ("Receiving   =",Receiving)
                    regex = re.compile('[^a-zA-Z0-9]')
                    Receiving=regex.sub(' ', Receiving.strip())

                    print ("Receiving  ",Receiving)
                    filter_item.append(Receiving.strip())
                    key_pdf.append("Receiving")


            if ('APPROVED' in ele):
                Created_By = ele.replace("APPROVED","") ## remove the "APPROVED" from string
                print ("Created_By----------------",Created_By)
                filter_item.append(Created_By)
                key_pdf.append ("Created_By")
                requestNo=itemList[count-3]
                requestNo=requestNo.split()[0]
                print ("requestNo      ===  ",requestNo)
                filter_item.append(requestNo)
                key_pdf.append("requestNo")

            if ('BLANKET' in ele):
                #print ("ele first  BLANKET : ",ele)
                if (len("BLANKET")<len(ele)):
                    temp=ele.split()
                    #print ("Purchase_order   ---",temp)
                    Purchase_order=temp[1]
                    print ("Purchase_order   ---",Purchase_order)

                    Order_Description= temp[1:-1]
                    Order_Description = ' '.join(Order_Description)
                    print ("Order_Description   ---",Order_Description)
                    filter_item.append(Purchase_order)
                    key_pdf.append("Purchase_order")
                    #filter_item.append(Order_Description)
                    #key_pdf.append("Order_Description")
                    #print (temp)
                index_1=count+1
                if (len(ele)>3):

                    Budget=itemList[index_1]
                    Budget=Budget.split()[0]
                    #print ("Budget  :",Budget)
                    #filter_item.append(Budget)
                    #key_pdf.append("Budget")
                if (len("BLANKET")==len(ele)):
                    Order_Description = itemList[count-1]+" "+itemList[count-2]
                    print ("Order_Description   --",Order_Description)
                    Purchase_order= itemList[count-3]

        return filter_item,key_pdf


    # In[91]:


    def df_part_1_type8(filter_item,key_pdf,df_firstPart):
        try:
            a,b,c,d = filter_item
            a,b,c,d= [str(e) for e in [a,b,c,d]]
            a=[a];b=[b];c=[c];d=[d]
            df_firstPart = pd.DataFrame(list (zip(a,b,c,d)),columns =key_pdf)
        except:
            pass
        return df_firstPart



    # In[ ]:





    # In[92]:


    def part_1_type6(filter_item,key_pdf,itemList):
        #itemList_1=list(set(itemList))

        for count,ele in enumerate (itemList):
            if ('RRP' in ele):
                #print ("ele first length==: ",len(ele)," length== ",ele)
                if (len(ele)>3):
                    Receiving=ele
                    Receiving=Receiving.split()

                    Receiving = [i for i in Receiving if 'RRP' in i] ## filter item by substring
                    Receiving=''.join(Receiving)
                    print ("Receiving   =",Receiving)
                    regex = re.compile('[^a-zA-Z0-9]')
                    Receiving=regex.sub(' ', Receiving.strip())

                    print ("Receiving  ",Receiving)
                    filter_item.append(Receiving.strip())
                    key_pdf.append("Receiving")
            if ('Summary' in ele):
                print ("itemList[count-3]==== ",itemList[count-3])
                filter_item.append(itemList[count-3])
                key_pdf.append("Created_By")
                filter_item.append(itemList[count-4])
                key_pdf.append("Employee ID")
                filter_item.append(itemList[count+4])
                key_pdf.append("Request No")#Purchase Order
                filter_item.append(itemList[count+6])
                key_pdf.append("Purchase Order")#PO Budget
                filter_item.append(itemList[count+8])
                key_pdf.append("PO Budget")#PO Budget

        return filter_item,key_pdf


    # In[93]:


    def df_part_1_type6(filter_item,key_pdf,df_firstPart):
        try:

            a,b,c,d,e,f = filter_item
            a,b,c,d,e,f= [str(e) for e in [a,b,c,d,e,f]]
            a=[a];b=[b];c=[c];d=[d];e=[e];f=[f]
            df_firstPart = pd.DataFrame(list (zip(a,b,c,d,e,f)),columns =key_pdf)
        except:
            pass
        return df_firstPart



    # In[94]:


    file_list_update = file_list=(glob.glob(outputpath+"*.jpg"))
    file_list_update


    # In[95]:



    itemList=[]
    filter_item=[]
    key_pdf=[]
    df_firstPart=''
    for file in file_list_update:
        try:
            itemList= part_1_img_txt(file,outputpath,txt_file,itemList)
        except:
            pass
        if (flag_img==2):

            try:
                print ("------------------part 8")
                filter_item,key_pdf= part_1_type8(filter_item,key_pdf,itemList)
                df_firstPart=df_part_1_type8(filter_item,key_pdf,df_firstPart)
            except:
                pass
        if (flag_img==1):

            try:
                #itemList= part_1_img_txt(file,outputpath,txt_file,itemList)
                print ("------------------part 6")
                filter_item,key_pdf= part_1_type6(filter_item,key_pdf,itemList)
                df_firstPart=df_part_1_type6(filter_item,key_pdf,df_firstPart)
            except:
                pass


    return df_firstPart,dictData_DF



# In[ ]:

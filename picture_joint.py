# coding: utf-8

# In[ ]:

# -*- coding:utf8 -*-
import os
from PIL import Image
import pandas as pd



# In[ ]:


#三个层级的文件，生成具体地址文件
def index_dir(file_path):
    filelistend=[]
    temp_list=[f for f in os.listdir(file_path) if not f.startswith('.')] #put file name from file_path in temp_list
    for temp_list_each in temp_list:
        pathName=file_path + '/' + temp_list_each
        #print (pathName)
        temp_list_1=[f for f in os.listdir(pathName) if not f.startswith('.')]
        #temp_list_1=os.listdir(pathName)
        for temp_list_i in temp_list_1:
            pathName_1=pathName + '/' + temp_list_i   
            filelist = os.listdir(pathName_1)
            for j in filelist:
                filelistend.append(pathName_1 + '/' + j)
    return filelistend


# In[ ]:


#九宫格地址  
def sudoku_adress(path):
    path_i=index_dir(path)
    sudoku_adress=[]
    for i in range(len(path_i)):
        row_index=path_i[i].split("/")[-2]
        col_index=path_i[i].split("/")[-1].replace('.png','')

        row=row_index[4:]
        col=col_index[4:]
        row_1=('R000'+hex(int(row,16)-1)[2:]).upper()
        col_1=('C000'+hex(int(col,16)-1)[2:]).upper()
        row_11=('R000'+hex(int(row,16)+1)[2:]).upper()
        col_11=('C000'+hex(int(col,16)+1)[2:]).upper()

        sudoku_s=[row_index,
                  col_index,
                  row_1+'/'+col_1,
                  row_1+'/'+col_index,
                  row_1+'/'+col_11,
                  row_index+'/'+col_1,
                  row_index+'/'+col_11,
                  row_11+'/'+col_1,
                  row_11+'/'+col_index,
                  row_11+'/'+col_11]
        sudoku_adress.append(sudoku_s)
    adress_data=pd.DataFrame(sudoku_adress,columns=['row_index','col_index','sudoku1_adress','sudoku2_adress','sudoku3_adress'
                                      ,'sudoku4_adress','sudoku6_adress','sudoku7_adress','sudoku8_adress'
                                      ,'sudoku9_adress'])
    return adress_data


# In[ ]:


#九宫格拼接图片
def picture_merge1(path1,save_path,adress_data):
    row_index=adress_data['row_index'].values.tolist()
    col_index=adress_data['col_index'].values.tolist()
    for m in range(len(character_data)):
        im_new = Image.new('RGB', (768,768), (0, 0, 0))

        a=[character_data.loc[m,i] for i in character_data.columns[2:]]

        row_loc=row_index[m]
        col_loc=col_index[m]

        im2=Image.open(path1+'/'+row_loc+'/'+col_loc+'.png')
        im_new.paste(im2,(256,256))

        for z in range(8):
            if a[z]!='':
                try:
                    im=Image.open(path1+'/'+a[z]+'.png')
                    if z<3:
                        im_new.paste(im,(256*z,0))
                    elif z==3:
                        im_new.paste(im,(0,256))
                    elif z==4:
                        im_new.paste(im,(512,256))
                    else:
                        im_new.paste(im,(256*(z-5),512))
                except:
                    continue
         #保存图片
        im_new = im_new.convert('RGBA')
        # im_new = im_new.resize((1512,1512),Image.ANTIALIAS)
        im_new.save(save_path+'/'+'%s_%s.png'%(row_loc,col_loc))



# In[ ]:


if __name__ == '__main__':
    path='data/tile'
    path1='data/tile/L18'
    save_path='data/picture_merge'
    character_data=sudoku_adress(path)
    picture_merge1(path1,save_path,character_data)





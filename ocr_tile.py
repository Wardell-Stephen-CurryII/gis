#!/usr/bin/env python
# coding: utf-8


import os
from aip import AipOcr
import pandas as pd


class BaiDuOcr:
    def __init__(self):
        # 切割的文字保存的位置
        self.save_path = 'data/cut'
        self.APP_ID = '21673472'
        self.API_KEY = 'r4uGGCloexzu0nyy8Pi7KIGx'
        self.SECRET_KEY = 'W3zWj1c904xjzlfEW84dZkAwRem2f3yB'

    # 读入图片
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    # 文字识别
    def character_recognition(self):
        result = []
        for path_j in os.listdir(self.save_path):
            z = self.save_path + '/' + path_j
            try:
                client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
                image = self.get_file_content(z)
                adress_character = client.basicGeneral(image)['words_result']
                result.append([path_j, str(adress_character)])
            except:
                continue
                # 输出识别结果
        # pd.DataFrame(result,columns=['path','words']).to_csv('/Users/liwenyan/Desktop/result.csv')
        return pd.DataFrame(result, columns=['path', 'words'])

    # 文字识别
    def character_recognition_once(self,word_path):
        try:
            client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
            image = self.get_file_content(word_path)
            adress_character = client.basicGeneral(image)['words_result']
        except:
            return
        return adress_character

    # 合并多排文字
    def merge_word(self,word_path):
        words = self.character_recognition_once(word_path)
        words_str = ''
        if words:
            for item in words:
                words_str += item['words']
        return words_str


if __name__ == '__main__':
    bdocr = BaiDuOcr()
    character_data = bdocr.character_recognition()

import os
import pandas as pd
from tile import Tile
import time


def main():
    # 读取图片位置
    path = 'data/picture_merge'
    # 切割的文字保存的位置
    save_path = 'data/cut'
    tile = Tile()
    # 批量切割图片
    all_detail = []
    for path_i in os.listdir(path):
        img_path = path + '/' + path_i
        # img_path = 'data/picture_merge/R000183C8_C00034ACF.png'
        box_gather = tile.picture_detection(img_path,path_i)
        number_detail = tile.picture_recognition_once(img_path, box_gather, save_path)
        if len(number_detail) != 0:
            all_detail += number_detail
    print(all_detail)
    # all_detail = tile.remove_duplication(all_detail)
    result = pd.DataFrame(all_detail)
    header = ['cut_path', '文字_x', '文字_y', '图标_x', '图标_y', '图标类型', '图标代码', '中心图行', '中心图列', '文字', '轮廓',
              '文字_x转换后', '文字_y转换后', '文字行转换后', '文字列转换后', '图标_x转换后', '图标_y转换后', '图标行转换后', '图标列转换后']
    result.to_csv('data/result/瓦片数据20210429_1.csv', header=header)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
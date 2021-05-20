import cv2
from icon.icon03 import Icon
from tile import character_poixy


# 切割图片文字部分
def picture_cut(img_path, row_index, col_index):
    img = cv2.imread(img_path)
    icon = Icon()
    icon_data = icon.match_icon_more(img)
    icon_list = []
    for i in range(len(icon_data)):
        icon_x = icon_data[i][0]
        icon_y = icon_data[i][1]
        icon_name = icon_data[i][2]
        icon_code = icon_data[i][3]
        if 255 < icon_x <= 511 and 255 < icon_y <= 511:
            word_x_sql, word_y_sql, row_256_word, col_256_word = character_poixy(icon_x, icon_y, row_index, col_index)
            print([word_x_sql, word_y_sql, row_256_word, col_256_word, icon_x, icon_y, icon_name, icon_code])
            icon_list.append([word_x_sql, word_y_sql, row_256_word, col_256_word, icon_x, icon_y, icon_name, icon_code])
    print(icon_list)
    return icon_list


if __name__ == '__main__':
    # img_path = 'data/picture_merge_3/R000183B3_C00034AD4.png'
    img_path = 'data/picture_merge_3/R000183B1_C00034ADF.png'
    r = 'R000183B1'
    c = 'C00034ADF'
    icon_list = picture_cut(img_path, r, c)

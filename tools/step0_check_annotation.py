import os
import shutil
import json
from tqdm import tqdm

class_name_to_idx_map = {'51':0, '52':1, '53':2, '54':3, '55':4, 
                            '61':5, '62':6, '63':7, '64':8, '65':9, 
                            '71':10, '72':11, '73':12, '74':13, '75':14,
                            '81':15, '82':16, '83':17, '84':18, '85':19,

                            '11': 20, '16': 21,
                            '21': 22, '26': 23,
                            '31': 24, '36': 25,
                            '41': 26, '46': 27,

                            'doubleteeth': 28,
                            'crown': 29,

                            '51_stain':0,'52_stain':1, '53_stain':2, '54_stain':3, '55_stain':4, 
                            '61_stain':5, '62_stain':6, '63_stain':7, '64_stain':8, '65_stain':9, '63_stan':7,
                            '71_stain':10, '72_stain':11, '73_stain':12, '74_stain':13, '75_stain':14, 
                            '81_stain':15, '82_stain':16, '83_stain':17, '84_stain':18, '85_stain':19, 
                            '71_stian':10,

                            '52_retainedteeth':1,
                            '53_retainedteeth':2,
                            '75_discoloration':14,
                            '51_discoloration':0,
                            '51_retainedteeth':0,
                            '61_retainedteeth':5,
                            '62_retainedteeth':6,
                            '64_retainedteeth':8,
                            '63_retainedteeth':7,
                            '54_retainedteeth':3,
                            '74_retainedteeth':13,
                            '61_discoloration':5,

                            '55_crown':29,
                            '84_crown':29,
                            '74_crown':29,
                            
                            "55'":4,
                            '622':6,
                            '110': 15, # 81
                            # '585':19,
                            # '875':14,

                            '72\\3':28,
                            '72/3':28,
                            '82/83':28,
                            '81/82': 28,
                
                            # '42':16,
                            # '32':11,
                            # '22': 0,
                            # '23': 0, 
                            # '24': 0,
                            # '25': 0,

                            }

def contains_letters(s):
    return any(c.isalpha() for c in s)

def correct_coordinates(top_left, bottom_right):
    # 解构坐标点
    x1, y1 = top_left
    x2, y2 = bottom_right
    
    # 确保 (x1, y1) 是左上角，(x2, y2) 是右下角
    correct_top_left = (min(x1, x2), min(y1, y2))
    correct_bottom_right = (max(x1, x2), max(y1, y2))
    
    return correct_top_left, correct_bottom_right

def check_and_resave_jsons(json_folder, save_folder):

    images = [f for f in os.listdir(json_folder) if os.path.isfile(os.path.join(json_folder, f))]
    image_folder_list = images
    
    class_set = set()
    for _json in image_folder_list:
        src_json = os.path.join(json_folder, _json)
        if '.DS_Store' in src_json:
            continue
        # print(src_json)
        with open(src_json, 'r') as f_json:
            json_data = json.load(f_json)
        json_data['imageData'] = ''
        for _item in json_data['shapes']:
            if _item["shape_type"] == "rectangle":
                if _item['label'].startswith('mouth'):
                    if '_' not in _item['label']:
                        print(_item['label'])
                    else:
                        if int(_item['label'].split('_')[1]) > 7:
                            _item['label'] = 'mouth_7'
                    # print(src_json)
                    assert len(_item['label'].split('_')) == 2
                    assert _item['label'].split('_')[0] == 'mouth'
                    assert int(_item['label'].split('_')[1]) > 0 and int(_item['label'].split('_')[1]) <= 7
                    if int(_item['label'].split('_')[1]) != 7:
                        class_set.add(_item['label'].split('_')[1])
                    # for point convert cases
                    top_left = _item['points'][0]
                    bottom_right = _item['points'][1]
                    top_left, bottom_right = correct_coordinates(top_left, bottom_right)
                    _item['points'][0] = top_left
                    _item['points'][1] = bottom_right

                elif _item['label'] in class_name_to_idx_map.keys():
                    top_left = _item['points'][0]
                    bottom_right = _item['points'][1]
                    top_left, bottom_right = correct_coordinates(top_left, bottom_right)
                    _item['points'][0] = top_left
                    _item['points'][1] = bottom_right
                elif 'crown' in _item['label']:
                    _item['label'] = 'crown'
                elif "_" in _item['label']:
                    class_name = _item['label'].split('_')[0]
                    if class_name in class_name_to_idx_map.keys():
                        _item['label'] = class_name
                    else:
                        print(src_json)
                        print(_item['label'] + " is bad class name !!!")
                elif '/' in _item['label'] or '\\' in _item['label']:
                    class_name = 'doubleteeth'
                    _item['label'] = class_name
                elif _item['label'].isdecimal() and len(_item['label']) == 2:
                    _item['label'] = str(int(_item['label']) + 40)
                else:
                    print(_item['label'])
                    # import pdb; pdb.set_trace()
            
        with open(os.path.join(save_folder, _json) ,"w") as f_w:
            json.dump(json_data, f_w)
    if len(class_set) != 6:
        print(json_folder + ' is less than 6 classes !!! Pls fixed it !!!')
        # import pdb; pdb.set_trace()


def organize_data(root_dir):
    # annotation_folder_name = ''
    # image_folder_name = ''
    # for folder in os.listdir(root_dir):
    #     if 'post' in folder:
    #         annotation_folder_name = folder
    #     else:
    #         image_folder_name = folder

    folder_prefixes = []  # Collect folder prefixes for checking
    for folder in os.listdir(root_dir):
        if not 'post' in folder:
            continue
        if 'checked' in folder:
            continue
        folder_path = os.path.join(root_dir, folder)
        if os.path.isdir(folder_path):
            data_folders = os.listdir(folder_path)
            for data_folder in tqdm(data_folders):
                data_path = os.path.join(folder_path, data_folder)

                if os.path.isdir(data_path):
                    if contains_letters(data_folder):
                        folder_prefix = f"{folder}_{data_folder.split('.')[0]}"
                    else:
                        folder_prefix = f"{folder}_{data_folder}"
                        
                    folder_prefixes.append(folder_prefix)
                    json_folder = data_path
                    json_save_dir = os.path.join(root_dir, folder + '_checked', data_folder)
                    os.makedirs(json_save_dir, exist_ok=True)
                    check_and_resave_jsons(json_folder, json_save_dir)

# 输入多个根目录路径
root_directories = "/home/jinghao/projects/dental_plague_detection/dataset/27_1_2025_revision/"

date = [ '12_5',  '9_26',]
# root_directories = ["/home/hust/haojing/dental_plague_dataset/10_24", ]
# root_directories = '/home/hust/haojing/dental_plague_dataset/raw_data'
# resaved_json_dir = '/home/hust/haojing/dental_plague_dataset/raw_data/resaved_json'

for root_dir in date:
    root_dir = os.path.join(root_directories, root_dir)
    # single_path = os.path.join(root_directories, root_dir)
    organize_data(root_dir)
import os
import json
from pycocotools.coco import COCO
from PIL import Image, ImageDraw

def visualize_coco_annotations(image_folder, annotation_file, output_folder):
    # 初始化COCO对象
    coco = COCO(annotation_file)
    
    # 获取所有图片的ID
    img_ids = coco.getImgIds()
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历所有图片ID
    for img_id in img_ids:
        # 获取图片信息
        img_info = coco.loadImgs(img_id)[0]
        img_path = os.path.join(image_folder, img_info['file_name'])
        
        # 打开图片
        image = Image.open(img_path)
        draw = ImageDraw.Draw(image)
        
        # 获取该图片的所有标注
        annotations_ids = coco.getAnnIds(imgIds=img_id)
        annotations = coco.loadAnns(annotations_ids)
        
        # 遍历所有标注
        for annotation in annotations:
            # 获取标注的坐标
            x, y, w, h = annotation['bbox']
            x2, y2 = x + w, y + h
            
            # 绘制标注框
            draw.rectangle([x, y, x2, y2], outline='red', width=3)
            
            # 绘制类别标签
            label = coco.loadCats(annotation['category_id'])[0]['name']
            # print(label)
            # draw.text((x, y - 10), label, fill='red')
        
        # 保存图片
        output_path = os.path.join(output_folder, img_info['file_name'])
        image.save(output_path)
        
        # 清理
        del draw


# 使用示例
image_folder = '/home/jinghao/projects/dental_plague_detection/dataset/11_12_for_pseudo_labels_bbox/images'
annotation_file = 'output_coco.json'
output_folder = '/home/jinghao/projects/dental_plague_detection/dataset/11_12_for_pseudo_labels_bbox/visual_check'

visualize_coco_annotations(image_folder, annotation_file, output_folder)

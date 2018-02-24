import os, sys, random
import xml.etree.ElementTree as ET
import mxnet as mx


classes = ["RBC", "WBC", "Platelets"]
ratio = 0.9
path = '../../BCCD'


def gen_det_rec(classes, dataset_dir, ratio=1):
    assert ratio <= 1 and ratio >= 0
    img_dir = os.path.join(dataset_dir, "JPEGImages")
    label_dir = os.path.join(dataset_dir, "Annotations")
    img_names = os.listdir(img_dir)
    img_names.sort()
    label_names = os.listdir(label_dir)
    label_names.sort()
    file_num = len(img_names)
    assert file_num==len(label_names)

    idx_random = list(range(file_num))
    random.shuffle(idx_random)
    idx_train=idx_random[:int(file_num*ratio)+1]
    idx_val=idx_random[int(file_num*ratio)+1:]

    with open("train.lst", "w") as train_lst:
        print("Writing in train.lst...")
        if idx_val:
            with open("val.lst", "w") as val_lst:
                print("Writing in val.lst...")

                for idx in range(file_num):
                    each_img_path = os.path.join(img_dir, img_names[idx])
                    each_label_path = os.path.join(label_dir, label_names[idx])
                    tree = ET.parse(each_label_path)
                    root = tree.getroot()
                    size = root.find('size')
                    width = float(size.find('width').text)
                    height = float(size.find('height').text)
                    label = []
                    label.append(str(idx))
                    label.append('4\t5\t'+str(width)+'\t'+str(height))
                    
                    for obj in root.iter('object'):
                        cls_name = obj.find('name').text
                        if cls_name not in classes:
                            continue
                        cls_id = classes.index(cls_name)
                        xml_box = obj.find('bndbox')
                        xmin = float(xml_box.find('xmin').text) / width
                        ymin = float(xml_box.find('ymin').text) / height
                        xmax = float(xml_box.find('xmax').text) / width
                        ymax = float(xml_box.find('ymax').text) / height
                        for i in [cls_id, xmin, ymin, xmax, ymax]:
                            label.append(str(i))

                    label.append(each_img_path)
                    label = '\t'.join(label)
                    if idx in idx_train:
                        train_lst.write(label+'\n')
                    else:
                        val_lst.write(label+'\n')

gen_det_rec(classes, path, ratio)
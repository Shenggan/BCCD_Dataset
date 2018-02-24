from mxnet import gluon
from mxnet import image
from mxnet import nd
import matplotlib as mpl
import matplotlib.pyplot as plt

data_shape = (480, 640)
batch_size = 64
data_dir = '../../BCCD'

def get_iterators(data_shape, batch_size):
    class_names = ["RBC", "WBC", "Platelets"]
    num_class = len(class_names)
    train_iter = image.ImageDetIter(
        batch_size=batch_size,
        data_shape=(3, data_shape[0], data_shape[1]),
        path_imgrec=data_dir+'train.rec',
        path_imgidx=data_dir+'train.idx',
        shuffle=True,
        mean=True,
        rand_crop=1,
        min_object_covered=0.95,
        max_attempts=200)
    val_iter = image.ImageDetIter(
        batch_size=batch_size,
        data_shape=(3, data_shape[0], data_shape[1]),
        path_imgrec=data_dir+'val.rec',
        shuffle=False,
        mean=True)
    return train_iter, val_iter, class_names, num_class

train_data, test_data, class_names, num_class = get_iterators(
    data_shape, batch_size)

batch = test_data.next()

def box_to_rect(box, color, linewidth=3):
    """convert an anchor box to a matplotlib rectangle"""
    box = box.asnumpy()
    return plt.Rectangle(
        (box[0], box[1]), box[2]-box[0], box[3]-box[1],
        fill=False, edgecolor=color, linewidth=linewidth)

_, figs = plt.subplots(3, 3, figsize=(6,6))
for i in range(3):
    for j in range(3):
        img, labels = batch.data[0][3*i+j], batch.label[0][3*i+j]
        # (3L, 256L, 256L) => (256L, 256L, 3L)
        img = img.transpose((1, 2, 0))
        img = img.clip(0,255).asnumpy()/255
        fig = figs[i][j]
        fig.imshow(img)
        for label in labels:
            label[1] *= data_shape[1]
            label[3] *= data_shape[1]
            label[2] *= data_shape[0]
            label[4] *= data_shape[0]
            if label[0] == 0:
                rect = box_to_rect(label[1:5],'red',0.5)
            elif label[0] == 1:
                rect = box_to_rect(label[1:5],'green',0.5)
            elif label[0] == 2:
                rect = box_to_rect(label[1:5],'blue',0.5)
            else:
                rect = box_to_rect(label[1:5],'black',2)
            fig.add_patch(rect)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)

plt.show()

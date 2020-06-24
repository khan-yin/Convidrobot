
import os
import numpy as np
import copy
import datetime
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
import torch.nn as nn
import torchvision
from torchvision import datasets, models, transforms
import torch.optim as optim

from PIL import Image
import skimage
from skimage import io, transform
from sklearn.metrics import confusion_matrix

EPOCHS = 16
BATCH_SIZE = 64
data_dir = "../input/chest-xray-pneumonia/chest_xray/chest_xray"
model_dir = "../output"
TEST = 'test'
TRAIN = 'train'
VAL = 'val'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def data_transforms(phase):
    if phase == TRAIN:
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    if phase == VAL:
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    if phase == TEST:
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    return transform

def load_data():
    print("Loading dataset")
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms(x))
                      for x in [TRAIN, VAL, TEST]}

    dataloaders = {TRAIN: torch.utils.data.DataLoader(image_datasets[TRAIN], batch_size=BATCH_SIZE, shuffle=True),
                   VAL: torch.utils.data.DataLoader(image_datasets[VAL], batch_size=1, shuffle=True),
                   TEST: torch.utils.data.DataLoader(image_datasets[TEST], batch_size=1, shuffle=True)}
    dataset_sizes = {x: len(image_datasets[x]) for x in [TRAIN, VAL]}
    classes = image_datasets[TRAIN].classes
    class_names = image_datasets[TRAIN].classes
    return dataloaders, dataset_sizes, class_names

def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated
    plt.show()

def preview_data():
    dataloaders, dataset_sizes, class_names = load_data()
    # Get a batch of training data
    inputs, classes = next(iter(dataloaders[TRAIN]))

    # Make a grid from batch
    out = torchvision.utils.make_grid(inputs)

    # imshow(out, title=[class_names[x] for x in classes])
    print("label: " + str([class_names[x] for x in classes]))
    imshow(out, title="batch data")

if __name__ == '__main__':
    preview_data()


import torch
import cv2
import argparse
from utils.vis_helper import vis_demo
from utils.data_preprocess import preprocess
from utils.model_helper import build_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
parser = argparse.ArgumentParser(description="Test code of DSALVANet")
parser.add_argument("-w", "--weight", type=str, default="./checkpoints/checkpoint_200.pth", help="Path of weight.")
parser.add_argument("-i", "--img", type=str, help="Path of image.")
parser.add_argument("-b", "--boxes", type=str, help="Path of boxes.")

if __name__ == '__main__':
    args = parser.parse_args()
    img_path,boxes_path,weight_path = args.img, args.boxes, args.weight
    with open(boxes_path, "r") as f:
        lines = f.readlines()
        ori_boxes = []
        for line in lines:
            data = line.split()
            ori_boxes.append(list(map(int,data)))
    src_img = cv2.imread(img_path)
    query, supports = preprocess(src_img, ori_boxes,device)
    model = build_model(weight_path,device)
    output = model(query,supports)
    vis_output = vis_demo(src_img,ori_boxes,output)
    cv2.imwrite("./output/output.jpg",vis_output)
    print('Finish.')
import cv2
import numpy as np
import torch

def apply_scoremap(image, scoremap, alpha=0.5):
        np_image = np.asarray(image, dtype=np.float)
        scoremap = (scoremap * 255).astype(np.uint8)
        scoremap = cv2.applyColorMap(scoremap, cv2.COLORMAP_JET)
        scoremap = cv2.cvtColor(scoremap, cv2.COLOR_BGR2RGB)
        return (alpha * np_image + (1 - alpha) * scoremap).astype(np.uint8)

def vis_demo(src_img, boxes, model_output):
        pre_cnt = int(torch.sum(model_output))
        h_orig, w_orig = src_img.shape[0], src_img.shape[1]
        density_pred = model_output.squeeze(0)
        density_pred = density_pred.permute(1, 2, 0)  # c x h x w -> h x w x c
        density_pred = density_pred.cpu().detach().numpy()
        density_pred = cv2.resize(density_pred, (w_orig, h_orig))
        density_pred = (density_pred - density_pred.min()) / (density_pred.max() - density_pred.min())
        output = apply_scoremap(src_img, density_pred)
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
        for box in boxes:
            y1, x1, y2, x2 = box
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(output, "Result:{0}".format(pre_cnt), (10,30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 255), 2)
        return output 
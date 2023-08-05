
import pandas as pd
from segmentation_pipeline.impl.datasets import PredictionItem
import os
from segmentation_pipeline.impl import rle
import imageio
from segmentation_pipeline import segmentation

from keras.optimizers import Adam
class SegmentationRLE:

    def __init__(self,path,imgPath):
        self.data=pd.read_csv(path);
        self.values=self.data.values;
        self.imgPath=imgPath;
        self.ddd=self.data.groupby('ImageId');
        self.masks=self.ddd['ImageId'];
        self.ids=list(self.ddd.groups.keys())
        pass

    def __getitem__(self, item):
        pixels=self.ddd.get_group(self.ids[item])["EncodedPixels"]
        return PredictionItem(self.ids[item] + str(), imageio.imread(os.path.join(self.imgPath,self.ids[item])),
                              rle.masks_as_image(pixels) > 0.5)

    def isPositive(self, item):
        pixels=self.ddd.get_group(self.ids[item])["EncodedPixels"]
        for mask in pixels:
            if isinstance(mask, str):
                return True;
        return False

    def __len__(self):
        return len(self.masks)

ds = SegmentationRLE ("F:/all/train_ship_segmentations.csv","D:/train_ships/train")
from skimage.morphology import binary_opening, disk
import numpy as np
def main():
    #segmentation.execute(ds, "ship_config.yaml")
    # cfg=segmentation.parse("fpn/ship_config.yaml")
    # cfg.fit(ds)
    # cfg = segmentation.parse("linknet/ship_config.yaml")
    # cfg.fit(ds)
    # cfg = segmentation.parse("psp/ship_config.yaml")
    # cfg.fit(ds)
    cfg = segmentation.parse("fpn-resnext2/ship_config.yaml")
    cfg.fit(ds,foldsToExecute=[3])
    #print("A")
    num=0;


    #cfg.predict_to_directory("F:/all/test_v2","F:/all/test_v2_seg",batchSize=16)

    out_pred_rows=[]

    def onPredict(id,img,d):
        out_pred_rows=d["pred"]
        good=d["good"]
        num = d["num"]
        cur_seg = binary_opening(img.arr > 0.5, np.expand_dims(disk(2), -1))
        cur_rles = rle.multi_rle_encode(cur_seg)
        if len(cur_rles) > 0:
            good = good + 1;
            for c_rle in cur_rles:
                out_pred_rows += [{'ImageId': id, 'EncodedPixels': c_rle}]
        else:
            out_pred_rows += [{'ImageId': id, 'EncodedPixels': None}]
        num = num + 1;
        d["good"]=good
        d["num"] = num

        pass

    d={"pred": out_pred_rows, "good": 0, "num": 0}
    cfg.predict_in_directory("F:/all/test_v2",[0,2],3,onPredict,d,ttflips=True)
    submission_df = pd.DataFrame(out_pred_rows)[['ImageId', 'EncodedPixels']]
    submission_df.to_csv('mySubmission.csv', index=False)
    print("Good:"+str(d["good"]))
    print("Num:" + str(d["num"]))
if __name__ == '__main__':
    main()
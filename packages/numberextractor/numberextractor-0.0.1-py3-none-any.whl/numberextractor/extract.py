from digitpkg import digitextractor
from digitpkg import digitUtil
from keras.models import load_model
import scipy
import scipy.ndimage.morphology
import math
import numpy as np
import cv2
class numberExtractor:
    def __init__(self, modelfile):
        self.model = load_model(modelfile)
    def extract_from_image(self, imagefile, numberindex, imgsize):
        results = digitextractor.extract_from_image(imagefile, imgsize)
        digitimgs = digitUtil.getSortedDictionaryImages(results, numberindex)

        result = 0
        i = 0
        for di in digitimgs:
            i+=1
            di = cv2.copyMakeBorder(di, math.ceil(imgsize/5),  math.ceil(imgsize/5),  math.ceil(imgsize/5),  math.ceil(imgsize/5), cv2.BORDER_CONSTANT, None, (255,255,255))
            di = cv2.resize(di, (imgsize, imgsize))
            di = cv2.cvtColor(di, cv2.COLOR_BGR2GRAY)
            di = cv2.bitwise_not(di)
            infdi = di.reshape(1, imgsize, imgsize, 1)
            infdi = infdi.astype('float32')
            infdi /=255
            res = self.model.predict(infdi)
            digit = np.argmax(res[0], axis=0)
        
            result += (digit*math.pow(10, len(digitimgs)-i))
        return result




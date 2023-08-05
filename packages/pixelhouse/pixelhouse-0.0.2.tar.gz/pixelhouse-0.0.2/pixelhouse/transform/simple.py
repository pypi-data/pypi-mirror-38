import numpy as np
import cv2
from ..artist import Artist, constant

class scale(Artist):
    fx = constant(0.5)
    fy = constant(None)
    args = ("fx", "fy")
    
    def __call__(self, cvs, t=0.0):
        
        fx, fy = self.fx(t), self.fy(t)
        if fy is None:
            fy = fx
            
        cvs._img =  cv2.resize(cvs.img, (0,0), fx=fx, fy=fy)

class translate(Artist):
    x = constant(0.5)
    y = constant(0.0)
    args = ("x", "y")
    
    def __call__(self, cvs, t=0.0):
        x = cvs.transform_length(self.x(t))
        y = cvs.transform_length(self.y(t))
        
        M = np.float32([[1,0,x],[0,1,y]])
        cvs._img =  cv2.warpAffine(cvs.img, M, cvs.shape[:2])
    
class rotate(Artist):
    theta = constant(np.pi/4)
    args = ("theta",)
    
    def __call__(self, cvs, t=0.0):
        theta = cvs.transform_angle(self.theta(t))

        cols, rows = cvs.shape[:2]
        M = cv2.getRotationMatrix2D((cols//2,rows//2), theta, 1)
        cvs._img = cv2.warpAffine(cvs.img,M,(cols,rows))

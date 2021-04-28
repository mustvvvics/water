# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 20:22:49 2021

@author: Mustvvvics
"""

import cv2
import os
import numpy as np
import time

def CalculationHigh(h):
        RealyHighMax = 13
        CameraHighMax = 321

        if h > 0 :
                high =  (RealyHighMax / CameraHighMax) * h
        else:
                high = 0
        return high
        
# def readCamera():


        
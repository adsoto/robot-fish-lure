import math
import velocityPredictor as vp
import numpy as np
import cv2

totalPrevList = []


class idtracker:

    def __init__(self, fishInTank):
        self.id_count = 1
        self.fishInTank = fishInTank
        self.vp = vp.velocityPredictor(r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\videos\background.png")
        prevList = []

    def update(self, objects_rect):
        global totalPrevList

        currentList = []
        
        if totalPrevList == []:
            for fish in objects_rect:
                x, y, t, w, h = fish
                currentList.append([self.id_count, x, y, t, w, h])
                self.id_count += 1
            totalPrevList.append(currentList)

        elif len(totalPrevList) == 1: # second frame

            for prevFish in totalPrevList[0]:
                id, pfx, pfy, pft, pfw, pfh = prevFish
                pfcx = (pfx + pfx + pfw) // 2
                pfcy = (pfy + pfy + pfh) // 2
                minDist = math.dist((objects_rect[0][0], objects_rect[0][1]), 
                                         (pfcx, pfcy)) # baseline distance
                closestFish = objects_rect[0]                
                for fish in objects_rect:
                    x, y, t, w, h = fish
                    cx = (x + x + w) // 2
                    cy = (y + y + h) // 2
                    
                    dist = math.dist((cx, cy), (pfcx, pfcy))
                    if dist<minDist: # finding shortest distance between current fish and fish from previous frame
                        minDist = dist
                        closestFish = fish
                        
                xCoord, yCoord, time, width, height = closestFish
                currentList.append([id, xCoord, yCoord, time, width, height])
            totalPrevList.append(currentList)

        else:
            currentList = self.vp.assignIDs(totalPrevList, objects_rect)
            totalPrevList.append(currentList)

        return currentList
    
if __name__ == '__main__':
    foregroundpath = r"C:\Users\ginar\OneDrive\Documents\robot-fish-lure-code-refactor\videos\use_for_velocities.avi"
    capture = cv2.VideoCapture(foregroundpath)
    ret, frame = capture.read()
    tracker = idtracker(3)
    tracker.update([[1,2,100,1,1], [50, 40, 100,1, 1], [300,400,100,1,1]])
    tracker.update([[5, 5, 200, 1, 1], [55, 45, 200, 1, 1], [305, 405, 200, 1, 1]])
    tracker.update([[20, 10, 300, 1, 1], [70, 50, 300, 1, 1], [340, 440, 300, 1, 1]])
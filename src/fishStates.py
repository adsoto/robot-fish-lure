''' creates fish objects and creates dictionary of positions [x,y,t]'''
import time


global measurements
measurements = []
#global measurements
fishList = {}
fishObjList = []

FPS = 10

class fishState:

    
    def __init__(self, id, pos_List):
        self.id = id
        self.posList = pos_List # [[x,y,t1], [x,y,t2], ...]


    def update(self, fishCoords):
        global measurements
        i=1
        if measurements == []: # first frame, no fish states exist yet
            measurements = fishCoords
            
            for fish in measurements:
                fishName = 'fish_{}'.format(i)
                fishName = fishState(fish[0], [fish[1:4]])
                fishObjList.append(fishName)

                i +=1
                pos = fishName.get_pos()


        else:
            measurements = fishCoords
            for fish in measurements:
                fishid = fish[0]
                for existingFish in fishObjList:
                    if fishid == existingFish.get_id():
                        existingFish.posList.append(fish[1:4])

                i+=1
        
        return fishObjList

    def get_id(self):
        return self.id
    
    def get_pos(self):
        return self.posList
    
    def returnInfo(self, objList):
        dictionary = {}
        for obj in objList:
            key = obj.get_id()
            value = obj.get_pos()
            dictionary[key] = value
        return dictionary


if __name__ == '__main__':
    fs = fishState(0, [])
    fs.update([[1, 756, 317, 1], [2, 444, 1, 1], [3, 671, 127, 1], [4, 736, 237, 1]])
    fs.update([[1, 760, 315, 2], [2, 440, 5, 2], [3, 675, 125, 2], [4, 735, 235, 2]])
    #fs.update([[6, 814, 441, 33], [5, 785, 380, 33], [1, 700, 227, 33], [3, 607, 144, 33], [7, 837, 127, 33], [11, 271, 5, 33], [8, 809, 268, 33], [4, 567, 219, 33]])

        
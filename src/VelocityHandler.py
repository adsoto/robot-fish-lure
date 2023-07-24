import pandas as pd
import VelocityTracker as vt
from datetime import *
import matplotlib.pyplot as plt
import os

class VelocityHandler:


    def __init__(self, velocitydict,):
        self._velocitydict = velocitydict

    def createdataframe(self, dataframe_name, fish, fishdict):
        poslist = fishdict[fish]
        
        time_list = self.timelist(poslist)
        xpos_list = self.Xposlist(poslist)
        ypos_list = self.Yposlist(poslist)
        xvel_list = self.Xvelocitylist(poslist)
        yvel_list = self.Yvelocitylist(poslist)

        df = pd.DataFrame(time_list, columns=['Time'], index=['frame1','frame2', 'frame3', 'frame4'])
        df['Xpositions'] = xpos_list
        df['Ypositions'] = ypos_list
        df['Xvelocity'] = xvel_list
        df['Yvelocity'] = yvel_list

        return df
    
    def timelist(self, poslist):
        time_list = []
        for frame in range(len(poslist)):
            time = poslist[frame][0]
            time_list.append(time)
        return time_list

    def Xposlist(self, poslist):
        xpos_list = []
        for frame in range(len(poslist)):
            xpos = poslist[frame][1]
            xpos_list.append(xpos)
        return xpos_list
    
    def Yposlist(self, poslist):
        ypos_list = []
        for frame in range(len(poslist)):
            ypos = poslist[frame][2]
            ypos_list.append(ypos)
        return ypos_list

    def Xvelocitylist(self,poslist):
        xvel_list = []
        for frame in range(len(poslist)):
            xvel = poslist[frame][3]
            xvel_list.append(xvel)
        return xvel_list
    
    def Yvelocitylist(self, poslist):
        yvel_list = []
        for frame in range(len(poslist)):
            yvel = poslist[frame][4]
            yvel_list.append(yvel)
        return yvel_list
    
    def megadataframe(self, fishdict):
        mega_dataset = pd.DataFrame()  # initialize megadataframe

        time_list = self.timelist(fishdict[1])

        for i in fishdict:
            poslist = fishdict[i]
            xpos_list = self.Xposlist(poslist)
            ypos_list = self.Yposlist(poslist)
            xvel_list = self.Xvelocitylist(poslist)
            yvel_list = self.Yvelocitylist(poslist)

            df = pd.DataFrame(time_list, columns=['Time' + str(i)], index=['frame1','frame2', 'frame3', 'frame4'])
            df['Xpositions' + str(i)] = xpos_list
            df['Ypositions'+ str(i)] = ypos_list
            df['Xvelocity'+ str(i)] = xvel_list
            df['Yvelocity'+ str(i)] = yvel_list

            mega_dataset = pd.concat([mega_dataset, df],  axis=1)  # adds current fish's dataset to megadataset
        
        return mega_dataset

    

if __name__ == '__main__':
    # initialize list elements
    fishdict =  {
    # t, x, y, vx, vy
                1:  [[1 , 10, 30, 2, 5],  [30 , 100, 300, 3, 5], [55 , 1000, 5000, 5, 7], [77 , 10000, 20000, 8, 10]], 
                2:  [[1 , 20, 50, 3, 8],  [30 , 200, 500, 4, 16], [55, 2000, 7000,2, 4],  [77 , 20000, 40000, 4, 7] ], 
                3:  [[1 , 30, 90, 5, 8],  [30 , 300, 700, 5, 8], [55, 3000, 9000, 6, 6],  [77 , 30000, 50000, 6, 8] ],
                4:  [[1 , 40, 120, 8, 10], [30 , 400, 900, 3, 6], [55 , 4000, 1200,2, 5], [77 , 40000, 70000,4, 18] ], 
                }
    
    # cv = vt.CalcVelocity(fishdict)
    # vel_dict = cv.run()
    vh = VelocityHandler(fishdict)
    now = datetime.now()

    print(now)
    mega_dataset = pd.DataFrame()
    for x in fishdict:
        dataframe = vh.createdataframe('hello', x,fishdict)

        data_folder = 'data/' + now.strftime("%m.%d.%Y/") 
        data_filename = data_folder + "fish"+  str(x) + "data__" + now.strftime("%H.%M") + '.csv'

        if not os.path.exists(data_folder): # creates folder for today's processing
                os.makedirs(data_folder)

        print(dataframe)
        dataframe.to_csv(data_filename, index = True) # writes current fish dataset to its own CSV

    mega = vh.megadataframe(fishdict)
    print(mega)
    megadata_filename = data_folder + "total_data_set"+  now.strftime("%H.%M") + '.csv'
    mega.to_csv(megadata_filename, index = True)




import pandas as pd
import VelocityTracker as vt
from datetime import *
import matplotlib.pyplot as plt
import os

class VelocityHandler:


    def __init__(self, velocityfishdict): # takes in the velocitydictionary
        self._velfishdict = velocityfishdict

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
            time = poslist[frame][2]
            time_list.append(time)
        return time_list

    def Xposlist(self, poslist):
        xpos_list = []
        for frame in range(len(poslist)):
            xpos = poslist[frame][0]
            xpos_list.append(xpos)
        return xpos_list
    
    def Yposlist(self, poslist):
        ypos_list = []
        for frame in range(len(poslist)):
            ypos = poslist[frame][1]
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

    def run(self):

        now = datetime.now()
        print(now)
        fishdict = self._velfishdict
        for x in fishdict:
            dataframe = self.createdataframe('hello', x,fishdict)

            data_folder = 'data/' + now.strftime("%m.%d.%Y/") 
            data_filename = data_folder + "fish"+  str(x) + "data__" + now.strftime("%H.%M") + '.csv'

            if not os.path.exists(data_folder): # creates folder for today's processing
                    os.makedirs(data_folder)

            print(dataframe)
            dataframe.to_csv(data_filename, index = True) # writes current fish dataset to its own CSV

        mega = self.megadataframe(fishdict)
        print(mega)
        megadata_filename = data_folder + "total_data_set"+  now.strftime("%H.%M") + '.csv'
        mega.to_csv(megadata_filename, index = True)
        return megadata_filename

    

if __name__ == '__main__':
    # initialize list elements
    
    fishdict = {
            # x, y, t, vx, vy

                1: [[1, 10, 30, 3.1034, 9.3103, 210.6383, 419.1489], [30, 100, 300, 18.3333, 92.037], [55, 1000, 5000, 210.6383, 419.1489], [77, 10000, 20000, 409.0909, 681.8182]], 
                2: [[1, 20, 50, 6.2069, 15.5172, 421.2766, 840.4255], [30, 200, 500, 36.6667, 128.7037], [55, 2000, 7000, 421.2766, 840.4255], [77, 20000, 40000, 818.1818, 1500.0]], 
                3: [[1, 30, 90, 9.3103, 21.0345, 631.9149, 1048.9362], [30, 300, 700, 55.0, 165.0], [55, 3000, 9000, 631.9149, 1048.9362], [77, 30000, 50000, 1227.2727, 1863.6364]], 
                4: [[1, 40, 120, 12.4138, 26.8966, 842.5532, 1470.2128], [30, 400, 900, 73.3333, 20.0], [55, 4000, 1200, 842.5532, 1470.2128], [77, 40000, 70000, 1636.3636, 3127.2727]]
                }
    
    # cv = vt.CalcVelocity(fishdict)
    # fish_dict = cv.run()

    vh = VelocityHandler(fishdict)

    vh.run()

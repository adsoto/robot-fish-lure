import pandas as pd
import VelocityTracker as vt


class VelocityHandler:

   
    
    def __init__(self, velocitydict):
        self._velocitydict = velocitydict


    if __name__ == '__main__':
        # initialize list elements
        fishdict =  {
        # t, x, y
                  'f1':  [[[1 , 10, 30],  [30 , 100, 300], [55 , 1000, 5000], [77 , 10000, 20000]], ], 
                  'f2':  [[[1 , 20, 50],  [30 , 200, 500], [55, 2000, 7000],  [77 , 20000, 40000]], ], 
                  'f3':  [[[1 , 30, 90],  [30 , 300, 700], [55, 3000, 9000],  [77 , 30000, 50000]], ],
                  'f4':  [[[1 , 40, 120], [30 , 400, 900], [55 , 4000, 1200], [77 , 40000, 70000]], ], 
                 }
        cv = vt.CalcVelocity(fishdict)
        vel_dict = cv.run()
        # Create the pandas DataFrame with column name is provided explicitly

        dict_dataframe = pd.DataFrame(vel_dict)
        
        # print dataframe.
        print(dict_dataframe)
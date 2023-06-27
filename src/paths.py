import numpy as np


# List of potential shapes for the bot to travel.
# Note most of these are in pixels, not meters


#OUT AND BACK
line_points_m = np.array([[0.05, 0.15],
                       [0.4, 0.15],
                       [0.05, 0.15]])
line_times = [0, 4, 8]


# move straight then change angle and move straight
forward_and_change = np.array([[0.15, 0.08],
                              [0.3, 0.08],
                              [0.5, 0.15]])
# straight line across middle of tank
straight_line = np.array([[0.086, 0.125],
                         [0.486, 0.125]])


# arc CCW then arc CW
arc_scurve_points = np.array([[0.115, 0.15/2+0.1],
                                [0.147, 0.066/2+0.1],
                                [0.24, 0.025/2+0.1],
                                [0.365, 0.15/2+0.1],
                                [0.4, 0.237/2+0.1],
                                [0.49, 0.275/2+0.1],
                                [0.58, 0.237/2+0.1],
                                [0.615, 0.15/2+0.1]])




#ARC OUT AND BACK
# arc_points = np.array([[100, 250],
#                        [200, 212],
#                        [300, 190],
#                        [400, 183],
#                        [500, 190],
#                        [600, 212],
#                        [700, 250],
#                        [650, 269],
#                        [600, 288],
#                        [500, 310],
#                        [400, 317],
#                        [300, 310],
#                        [200, 288],
#                        [100, 250]])
# arc_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


#SINGLE TURN
turn_points = np.array([[100, 100],
                       [500, 100],
                       [500, 400],
                       [100, 400]])
turn_times = [0, 1, 1, 1]
turn_angles = [0, np.pi/2, np.pi, np.pi]




rect_points = np.array([[.05, .08],
                       [.45, .08],
                       [.45, .25],
                       [.05, .25]])




forward_and_change = np.array([[.05, .08],
                              [.2, .08],
                              [.4, .15]])


#STANDARD RECTANGLE
# rect_points = np.array([[100, 100],
#                         [700, 100],
#                         [700, 400],
#                         [100, 400],
#                         [100, 100]])
# rect_times = [0, 3, 1.5, 3, 1.5]
rect_angles = [0, np.pi/2, np.pi, -np.pi/2, 0]


#SPECIAL RECTANGLE
rect_points_s = np.array([[100, 100],
                       [700, 100],
                       [700, 200],
                       [700, 400],
                       [600, 400],
                       [100, 400],
                       [100, 300],
                       [100, 100]])
x = .43*2
rect_times_s = [0, 3, x, 1.5, x, 3, x, 1.5]
rect_angles_s = [0, np.pi/2, np.pi/2, np.pi, np.pi, np.pi, np.pi, np.pi]


#LAWNMOWER PATTERN
lawn_points = np.array([[100, 100],
                       [700, 100],
                       [700, 200],
                       [100, 200],
                       [100, 300],
                       [700, 300],
                       [700, 400],
                       [100, 400]])
lawn_times = [0, 6, 7, 13, 14, 20, 21, 27]


#SMALL CIRCLE
circle_points = np.array([[375, 198],
                       [465, 235],
                       [502, 325],
                       [465, 415],
                       [375, 452],
                       [285, 415],
                       [248, 325],
                       [285, 235],
                       [375, 198]])
circle_times = [0, 1, 2, 3, 4, 5, 6, 7, 8]


spiral_points = np.array([[350,66],
                      [480,120],
                      [534,250],
                      [480,380],
                      [350,434],
                      [220,380],
                      [166,250],
                      [220,120],
                      [350,92],
                      [462,138],
                      [508,250],
                      [462,362],
                      [350,408],
                      [238,362],
                      [192,250],
                      [238,138],
                      [350,118],
                      [443,157],
                      [482,250],
                      [443,343],
                      [350,382],
                      [257,343],
                      [218,250],
                      [257,157],
                      [350,145],
                      [425,175],
                      [455,250],
                      [425,325],
                      [350,355],
                      [275,325],
                      [245,250],
                      [275,175],
                      [350,250]])
spiral_times = range(0, len(spiral_points))






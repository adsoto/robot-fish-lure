import numpy as np


# List of potential shapes for the bot to travel.
# Note most of these are in pixels, not meters


#OUT AND BACK in middle of tank
line_points_m = np.array([[0.05, 0.15],
                       [0.4, 0.15],
                       [0.05, 0.15]])
line_times = [0, 4, 10]

trajectory2 = np.array([[0, 0.1, 0.125, 0],
                        [1, 0.15, 0.125, 0],
                        [2, 0.2, 0.125, 0],
                        [3, 0.3, 0.125, 0],
                        [4, 0.4, 0.125, 0],
])

rect_trajectory = np.array([[0, .05, .08, 0],
                       [3, .45, .08, 0],
                       [5, .45, .25, 0],
                       [8, .05, .25, 0 ]])

trajectory3 = np.array([[0, 0.1, 0.1, 0],
                        [3, 0.2, 0.15, 0],
                        [6, 0.3, 0.1, 0],
                        [9, 0.4, 0.15, 0],
                        [12, 0.5, 0.1, 0],
])

trajectory1 = np.array([[ 0.0 , 0.1 , 0.125 , 1.5707963267948966 ],
[ 0.01 , 0.10066666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.02 , 0.10133333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.03 , 0.10200000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.04 , 0.10266666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.05 , 0.10333333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.06 , 0.10400000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.07 , 0.10466666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.08 , 0.10533333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.09 , 0.10600000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.1 , 0.10666666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.11 , 0.10733333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.12 , 0.10800000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.13 , 0.10866666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.14 , 0.10933333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.15 , 0.11 , 0.125 , 1.5707963267948966 ],
[ 0.16 , 0.11066666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.17 , 0.11133333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.18 , 0.112 , 0.125 , 1.5707963267948966 ],
[ 0.19 , 0.11266666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.2 , 0.11333333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.21 , 0.114 , 0.125 , 1.5707963267948966 ],
[ 0.22 , 0.11466666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.23 , 0.11533333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.24 , 0.116 , 0.125 , 1.5707963267948966 ],
[ 0.25 , 0.11666666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.26 , 0.11733333333333335 , 0.125 , 1.5707963267948966 ],
[ 0.27 , 0.11800000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.28 , 0.11866666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.29 , 0.11933333333333335 , 0.125 , 1.5707963267948966 ],
[ 0.3 , 0.12000000000000001 , 0.125 , 1.5707963267948966 ],
[ 0.31 , 0.12066666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.32 , 0.12133333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.33 , 0.122 , 0.125 , 1.5707963267948966 ],
[ 0.34 , 0.12266666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.35000000000000003 , 0.12333333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.36 , 0.124 , 0.125 , 1.5707963267948966 ],
[ 0.37 , 0.12466666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.38 , 0.12533333333333335 , 0.125 , 1.5707963267948966 ],
[ 0.39 , 0.126 , 0.125 , 1.5707963267948966 ],
[ 0.4 , 0.12666666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.41000000000000003 , 0.12733333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.42 , 0.128 , 0.125 , 1.5707963267948966 ],
[ 0.43 , 0.12866666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.44 , 0.12933333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.45 , 0.13 , 0.125 , 1.5707963267948966 ],
[ 0.46 , 0.13066666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.47000000000000003 , 0.13133333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.48 , 0.132 , 0.125 , 1.5707963267948966 ],
[ 0.49 , 0.13266666666666665 , 0.125 , 1.5707963267948966 ],
[ 0.5 , 0.13333333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.51 , 0.134 , 0.125 , 1.5707963267948966 ],
[ 0.52 , 0.13466666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.53 , 0.13533333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.54 , 0.136 , 0.125 , 1.5707963267948966 ],
[ 0.55 , 0.13666666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.56 , 0.13733333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.5700000000000001 , 0.138 , 0.125 , 1.5707963267948966 ],
[ 0.58 , 0.13866666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.59 , 0.13933333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.6 , 0.14 , 0.125 , 1.5707963267948966 ],
[ 0.61 , 0.14066666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.62 , 0.14133333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.63 , 0.14200000000000002 , 0.125 , 1.5707963267948966 ],
[ 0.64 , 0.14266666666666666 , 0.125 , 1.5707963267948966 ],
[ 0.65 , 0.14333333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.66 , 0.14400000000000002 , 0.125 , 1.5707963267948966 ],
[ 0.67 , 0.14466666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.68 , 0.14533333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.6900000000000001 , 0.14600000000000002 , 0.125 , 1.5707963267948966 ],
[ 0.7000000000000001 , 0.14666666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.71 , 0.14733333333333334 , 0.125 , 1.5707963267948966 ],
[ 0.72 , 0.14800000000000002 , 0.125 , 1.5707963267948966 ],
[ 0.73 , 0.14866666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.74 , 0.14933333333333335 , 0.125 , 1.5707963267948966 ],
[ 0.75 , 0.15 , 0.125 , 1.5707963267948966 ],
[ 0.76 , 0.15066666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.77 , 0.15133333333333335 , 0.125 , 1.5707963267948966 ],
[ 0.78 , 0.152 , 0.125 , 1.5707963267948966 ],
[ 0.79 , 0.15266666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.8 , 0.15333333333333332 , 0.125 , 1.5707963267948966 ],
[ 0.81 , 0.154 , 0.125 , 1.5707963267948966 ],
[ 0.8200000000000001 , 0.15466666666666667 , 0.125 , 1.5707963267948966 ],
[ 0.8300000000000001 , 0.15533333333333332 , 0.125 , 1.5707963267948966 ],
[ 0.84 , 0.156 , 0.125 , 1.5707963267948966 ],
[ 0.85 , 0.15666666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.86 , 0.15733333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.87 , 0.158 , 0.125 , 1.5707963267948966 ],
[ 0.88 , 0.15866666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.89 , 0.15933333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.9 , 0.16 , 0.125 , 1.5707963267948966 ],
[ 0.91 , 0.16066666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.92 , 0.16133333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.93 , 0.162 , 0.125 , 1.5707963267948966 ],
[ 0.9400000000000001 , 0.16266666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.9500000000000001 , 0.16333333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.96 , 0.164 , 0.125 , 1.5707963267948966 ],
[ 0.97 , 0.16466666666666668 , 0.125 , 1.5707963267948966 ],
[ 0.98 , 0.16533333333333333 , 0.125 , 1.5707963267948966 ],
[ 0.99 , 0.166 , 0.125 , 1.5707963267948966 ],
[ 1.0 , 0.16666666666666669 , 0.125 , 1.5707963267948966 ],
[ 1.01 , 0.16733333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.02 , 0.16799999999999998 , 0.125 , 1.5707963267948966 ],
[ 1.03 , 0.1686666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.04 , 0.16933333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.05 , 0.16999999999999998 , 0.125 , 1.5707963267948966 ],
[ 1.06 , 0.1706666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.07 , 0.17133333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.08 , 0.172 , 0.125 , 1.5707963267948966 ],
[ 1.09 , 0.1726666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.1 , 0.17333333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.11 , 0.174 , 0.125 , 1.5707963267948966 ],
[ 1.12 , 0.17466666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.1300000000000001 , 0.17533333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.1400000000000001 , 0.176 , 0.125 , 1.5707963267948966 ],
[ 1.1500000000000001 , 0.17666666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.16 , 0.17733333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.17 , 0.178 , 0.125 , 1.5707963267948966 ],
[ 1.18 , 0.17866666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.19 , 0.17933333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.2 , 0.18 , 0.125 , 1.5707963267948966 ],
[ 1.21 , 0.18066666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.22 , 0.18133333333333335 , 0.125 , 1.5707963267948966 ],
[ 1.23 , 0.182 , 0.125 , 1.5707963267948966 ],
[ 1.24 , 0.18266666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.25 , 0.18333333333333335 , 0.125 , 1.5707963267948966 ],
[ 1.26 , 0.184 , 0.125 , 1.5707963267948966 ],
[ 1.27 , 0.18466666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.28 , 0.18533333333333335 , 0.125 , 1.5707963267948966 ],
[ 1.29 , 0.186 , 0.125 , 1.5707963267948966 ],
[ 1.3 , 0.18666666666666668 , 0.125 , 1.5707963267948966 ],
[ 1.31 , 0.18733333333333335 , 0.125 , 1.5707963267948966 ],
[ 1.32 , 0.188 , 0.125 , 1.5707963267948966 ],
[ 1.33 , 0.18866666666666665 , 0.125 , 1.5707963267948966 ],
[ 1.34 , 0.18933333333333335 , 0.125 , 1.5707963267948966 ],
[ 1.35 , 0.19 , 0.125 , 1.5707963267948966 ],
[ 1.36 , 0.19066666666666665 , 0.125 , 1.5707963267948966 ],
[ 1.37 , 0.19133333333333336 , 0.125 , 1.5707963267948966 ],
[ 1.3800000000000001 , 0.192 , 0.125 , 1.5707963267948966 ],
[ 1.3900000000000001 , 0.19266666666666665 , 0.125 , 1.5707963267948966 ],
[ 1.4000000000000001 , 0.19333333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.41 , 0.194 , 0.125 , 1.5707963267948966 ],
[ 1.42 , 0.19466666666666665 , 0.125 , 1.5707963267948966 ],
[ 1.43 , 0.19533333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.44 , 0.196 , 0.125 , 1.5707963267948966 ],
[ 1.45 , 0.19666666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.46 , 0.19733333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.47 , 0.198 , 0.125 , 1.5707963267948966 ],
[ 1.48 , 0.19866666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.49 , 0.19933333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.5 , 0.2 , 0.125 , 1.5707963267948966 ],
[ 1.51 , 0.20066666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.52 , 0.20133333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.53 , 0.202 , 0.125 , 1.5707963267948966 ],
[ 1.54 , 0.20266666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.55 , 0.20333333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.56 , 0.20400000000000001 , 0.125 , 1.5707963267948966 ],
[ 1.57 , 0.20466666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.58 , 0.20533333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.59 , 0.20600000000000002 , 0.125 , 1.5707963267948966 ],
[ 1.6 , 0.20666666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.61 , 0.20733333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.62 , 0.20800000000000002 , 0.125 , 1.5707963267948966 ],
[ 1.6300000000000001 , 0.20866666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.6400000000000001 , 0.20933333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.6500000000000001 , 0.21000000000000002 , 0.125 , 1.5707963267948966 ],
[ 1.6600000000000001 , 0.21066666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.67 , 0.21133333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.68 , 0.21200000000000002 , 0.125 , 1.5707963267948966 ],
[ 1.69 , 0.21266666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.7 , 0.21333333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.71 , 0.214 , 0.125 , 1.5707963267948966 ],
[ 1.72 , 0.21466666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.73 , 0.21533333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.74 , 0.216 , 0.125 , 1.5707963267948966 ],
[ 1.75 , 0.21666666666666667 , 0.125 , 1.5707963267948966 ],
[ 1.76 , 0.21733333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.77 , 0.218 , 0.125 , 1.5707963267948966 ],
[ 1.78 , 0.21866666666666668 , 0.125 , 1.5707963267948966 ],
[ 1.79 , 0.21933333333333332 , 0.125 , 1.5707963267948966 ],
[ 1.8 , 0.22 , 0.125 , 1.5707963267948966 ],
[ 1.81 , 0.22066666666666668 , 0.125 , 1.5707963267948966 ],
[ 1.82 , 0.22133333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.83 , 0.222 , 0.125 , 1.5707963267948966 ],
[ 1.84 , 0.22266666666666668 , 0.125 , 1.5707963267948966 ],
[ 1.85 , 0.22333333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.86 , 0.224 , 0.125 , 1.5707963267948966 ],
[ 1.87 , 0.22466666666666668 , 0.125 , 1.5707963267948966 ],
[ 1.8800000000000001 , 0.22533333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.8900000000000001 , 0.226 , 0.125 , 1.5707963267948966 ],
[ 1.9000000000000001 , 0.22666666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.9100000000000001 , 0.22733333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.92 , 0.228 , 0.125 , 1.5707963267948966 ],
[ 1.93 , 0.22866666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.94 , 0.22933333333333333 , 0.125 , 1.5707963267948966 ],
[ 1.95 , 0.23 , 0.125 , 1.5707963267948966 ],
[ 1.96 , 0.23066666666666666 , 0.125 , 1.5707963267948966 ],
[ 1.97 , 0.23133333333333334 , 0.125 , 1.5707963267948966 ],
[ 1.98 , 0.232 , 0.125 , 1.5707963267948966 ],
[ 1.99 , 0.23266666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.0 , 0.23333333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.0100000000000002 , 0.234 , 0.125 , 1.5707963267948966 ],
[ 2.02 , 0.23466666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.0300000000000002 , 0.23533333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.04 , 0.236 , 0.125 , 1.5707963267948966 ],
[ 2.05 , 0.23666666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.06 , 0.23733333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.07 , 0.238 , 0.125 , 1.5707963267948966 ],
[ 2.08 , 0.23866666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.09 , 0.23933333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.1 , 0.24 , 0.125 , 1.5707963267948966 ],
[ 2.11 , 0.24066666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.12 , 0.24133333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.13 , 0.242 , 0.125 , 1.5707963267948966 ],
[ 2.14 , 0.24266666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.15 , 0.24333333333333335 , 0.125 , 1.5707963267948966 ],
[ 2.16 , 0.244 , 0.125 , 1.5707963267948966 ],
[ 2.17 , 0.24466666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.18 , 0.24533333333333335 , 0.125 , 1.5707963267948966 ],
[ 2.19 , 0.246 , 0.125 , 1.5707963267948966 ],
[ 2.2 , 0.24666666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.21 , 0.24733333333333332 , 0.125 , 1.5707963267948966 ],
[ 2.22 , 0.248 , 0.125 , 1.5707963267948966 ],
[ 2.23 , 0.24866666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.24 , 0.24933333333333332 , 0.125 , 1.5707963267948966 ],
[ 2.25 , 0.25 , 0.125 , 1.5707963267948966 ],
[ 2.2600000000000002 , 0.2506666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.27 , 0.2513333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.2800000000000002 , 0.252 , 0.125 , 1.5707963267948966 ],
[ 2.29 , 0.2526666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.3000000000000003 , 0.2533333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.31 , 0.254 , 0.125 , 1.5707963267948966 ],
[ 2.32 , 0.2546666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.33 , 0.2553333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.34 , 0.256 , 0.125 , 1.5707963267948966 ],
[ 2.35 , 0.25666666666666665 , 0.125 , 1.5707963267948966 ],
[ 2.36 , 0.2573333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.37 , 0.258 , 0.125 , 1.5707963267948966 ],
[ 2.38 , 0.25866666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.39 , 0.2593333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.4 , 0.26 , 0.125 , 1.5707963267948966 ],
[ 2.41 , 0.26066666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.42 , 0.2613333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.43 , 0.262 , 0.125 , 1.5707963267948966 ],
[ 2.44 , 0.26266666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.45 , 0.2633333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.46 , 0.264 , 0.125 , 1.5707963267948966 ],
[ 2.47 , 0.26466666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.48 , 0.2653333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.49 , 0.266 , 0.125 , 1.5707963267948966 ],
[ 2.5 , 0.26666666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.5100000000000002 , 0.2673333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.52 , 0.268 , 0.125 , 1.5707963267948966 ],
[ 2.5300000000000002 , 0.26866666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.54 , 0.2693333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.5500000000000003 , 0.27 , 0.125 , 1.5707963267948966 ],
[ 2.56 , 0.27066666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.57 , 0.2713333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.58 , 0.272 , 0.125 , 1.5707963267948966 ],
[ 2.59 , 0.27266666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.6 , 0.2733333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.61 , 0.274 , 0.125 , 1.5707963267948966 ],
[ 2.62 , 0.27466666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.63 , 0.2753333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.64 , 0.276 , 0.125 , 1.5707963267948966 ],
[ 2.65 , 0.27666666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.66 , 0.2773333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.67 , 0.278 , 0.125 , 1.5707963267948966 ],
[ 2.68 , 0.2786666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.69 , 0.2793333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.7 , 0.28 , 0.125 , 1.5707963267948966 ],
[ 2.71 , 0.2806666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.72 , 0.2813333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.73 , 0.28200000000000003 , 0.125 , 1.5707963267948966 ],
[ 2.74 , 0.2826666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.75 , 0.2833333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.7600000000000002 , 0.28400000000000003 , 0.125 , 1.5707963267948966 ],
[ 2.77 , 0.2846666666666667 , 0.125 , 1.5707963267948966 ],
[ 2.7800000000000002 , 0.2853333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.79 , 0.28600000000000003 , 0.125 , 1.5707963267948966 ],
[ 2.8000000000000003 , 0.2866666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.81 , 0.28733333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.82 , 0.28800000000000003 , 0.125 , 1.5707963267948966 ],
[ 2.83 , 0.2886666666666666 , 0.125 , 1.5707963267948966 ],
[ 2.84 , 0.28933333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.85 , 0.29000000000000004 , 0.125 , 1.5707963267948966 ],
[ 2.86 , 0.29066666666666663 , 0.125 , 1.5707963267948966 ],
[ 2.87 , 0.29133333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.88 , 0.29200000000000004 , 0.125 , 1.5707963267948966 ],
[ 2.89 , 0.29266666666666663 , 0.125 , 1.5707963267948966 ],
[ 2.9 , 0.29333333333333333 , 0.125 , 1.5707963267948966 ],
[ 2.91 , 0.29400000000000004 , 0.125 , 1.5707963267948966 ],
[ 2.92 , 0.29466666666666663 , 0.125 , 1.5707963267948966 ],
[ 2.93 , 0.29533333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.94 , 0.296 , 0.125 , 1.5707963267948966 ],
[ 2.95 , 0.29666666666666663 , 0.125 , 1.5707963267948966 ],
[ 2.96 , 0.29733333333333334 , 0.125 , 1.5707963267948966 ],
[ 2.97 , 0.298 , 0.125 , 1.5707963267948966 ],
[ 2.98 , 0.29866666666666664 , 0.125 , 1.5707963267948966 ],
[ 2.99 , 0.29933333333333334 , 0.125 , 1.5707963267948966 ]])

#much longer, 0.1 seconds apart

along_y = np.array([[0.2, 0.08],
                    [0.2, 0.3]])

diagonal = np.array([[0.15, 0.15],
                     [0.3, 0.3]])

#OUT AND BACK on side of tank
line_points_side = np.array([[0.05, 0.21],
                       [0.4, 0.21],
                       [0.05, 0.21]])
line_points_side_3 = np.array([[0.05, 0.18],
                       [0.48, 0.18],
                       [0.05, 0.18],
                       [0.48, 0.18],
                       [0.05, 0.18],
                       [0.48, 0.18],
                       [0.05, 0.18]])

# move straight then change angle and move straight
forward_and_change = np.array([[0.15, 0.08],
                              [0.3, 0.08],
                              [0.5, 0.15]])
# straight line across middle of tank

straight_line = np.array([[0.15, 0.125],
                         [0.16, 0.125],
                         [0.17, 0.125],
                         [0.18, 0.125],
                         [0.19, 0.125],
                         [0.2, 0.125],
                         [0.21, 0.125],
                         [0.22, 0.125],
                         [0.23, 0.125],
                         [0.24, 0.125],
                         [0.25, 0.125],
                         [0.26, 0.125],
                         [0.27, 0.125],
                         [0.28, 0.125],
                         ])
straight_line_times = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5]

straight_line2 = np.array([
[ 0.15 , 0.125],
[ 0.16 , 0.125],
[ 0.16999999999999998 , 0.125],
[ 0.18 , 0.125],
[ 0.19 , 0.125],
[ 0.2 , 0.125],
[ 0.21 , 0.125],
[ 0.22 , 0.125],
[ 0.22999999999999998 , 0.125],
[ 0.24 , 0.125],
[ 0.25 , 0.125],
[ 0.26 , 0.125],
[ 0.27 , 0.125],
[ 0.28 , 0.125],
[ 0.29000000000000004 , 0.125],
[ 0.3 , 0.125],
[ 0.31 , 0.125],
[ 0.32 , 0.125],
[ 0.32999999999999996 , 0.125],
[ 0.33999999999999997 , 0.125],
[ 0.35 , 0.125],
[ 0.36 , 0.125],
[ 0.37 , 0.125],
[ 0.38 , 0.125],
[ 0.39 , 0.125],
[ 0.4 , 0.125],
[ 0.41000000000000003 , 0.125],
[ 0.42000000000000004 , 0.125],
[ 0.43000000000000005 , 0.125],
[ 0.43999999999999995 , 0.125],
[ 0.44999999999999996 , 0.125],
[ 0.45999999999999996 , 0.125],
[ 0.47 , 0.125],
[ 0.48 , 0.125],
[ 0.49 , 0.125],
[ 0.5 , 0.125],
[ 0.51 , 0.125],
[ 0.52 , 0.125],
[ 0.53 , 0.125],
[ 0.54 , 0.125],
[ 0.55 , 0.125]])

straight_line3 = np.array([
[ 0.05 , 0.125],
[ 0.060000000000000005 , 0.125],
[ 0.07 , 0.125],
[ 0.08 , 0.125],
[ 0.09 , 0.125],
[ 0.1 , 0.125],
[ 0.11 , 0.125],
[ 0.12000000000000001 , 0.125],
[ 0.13 , 0.125],
[ 0.14 , 0.125],
[ 0.15000000000000002 , 0.125],
[ 0.16 , 0.125],
[ 0.16999999999999998 , 0.125],
[ 0.18 , 0.125],
[ 0.19 , 0.125],
[ 0.2 , 0.125],
[ 0.21000000000000002 , 0.125],
[ 0.22000000000000003 , 0.125],
[ 0.22999999999999998 , 0.125],
[ 0.24 , 0.125],
[ 0.25 , 0.125],
[ 0.26 , 0.125],
[ 0.27 , 0.125],
[ 0.28 , 0.125],
[ 0.29 , 0.125],
[ 0.3 , 0.125],
[ 0.31 , 0.125],
[ 0.32 , 0.125],
[ 0.33 , 0.125],
[ 0.33999999999999997 , 0.125],
[ 0.35 , 0.125],
[ 0.36 , 0.125],
[ 0.37 , 0.125],
[ 0.38 , 0.125],
[ 0.39 , 0.125],
[ 0.4 , 0.125],
[ 0.41 , 0.125],
[ 0.42 , 0.125],
[ 0.43 , 0.125],
[ 0.44 , 0.125],
[ 0.45 , 0.125]
])

straight_line_times2 = [
1.0 ,
1.125 ,
1.25 ,
1.375 ,
1.5 ,
1.625 ,
1.75 ,
1.875 ,
2.0 ,
2.125 ,
2.25 ,
2.375 ,
2.5 ,
2.625 ,
2.75 ,
2.875 ,
3.0 ,
3.125 ,
3.25 ,
3.375 ,
3.5 ,
3.625 ,
3.75 ,
3.875 ,
4.0 ,
4.125 ,
4.25 ,
4.375 ,
4.5 ,
4.625 ,
4.75 ,
4.875 ,
5.0 ,
5.125 ,
5.25 ,
5.375 ,
5.5 ,
5.625 ,
5.75 ,
5.875 ,
6.0]

straight_line_times3 =[1.0 ,
1.049800346606159 ,
1.1020807677344115 ,
1.156964771955567 ,
1.2145820186100698 ,
1.2750686241184594 ,
1.3385674835461971 ,
1.4052286081825316 ,
1.4752094799309121 ,
1.548675423348163 ,
1.6257999962113414 ,
1.7067653995349583 ,
1.7917629080071984 ,
1.8809933218620163 ,
1.9746674412546152 ,
2.073006564260992 ,
2.176243009678032 ,
2.2846206658592285 ,
2.398395566882612 ,
2.517836497412041 ,
2.6432256276807977 ,
2.7748591800975837 ,
2.9130481290497254 ,
3.058118935556825 ,
3.2104143185104124 ,
3.3702940643216066 ,
3.538135876889503 ,
3.714336269898286 ,
3.899311503551049 ,
4.093498567953274 ,
4.297356215469162 ,
4.511366044489658 ,
4.7360336371725 ,
4.971889753842118 ,
5.219491586871065 ,
5.4794240770051745 ,
5.752301295242165 ,
6.038767893528282 ,
6.339500627700135 ,
6.655209956269563 ,
6.986641718828549 ]

straight_line_times4 = [
0.0 ,
1.224744871391589 ,
1.7320508075688772 ,
2.121320343559643 ,
2.449489742783178 ,
2.7386127875258306 ,
3.0000000000000004 ,
3.24037034920393 ,
3.4641016151377544 ,
3.6742346141747673 ,
3.872983346207417 ,
4.06201920231798 ,
4.242640687119286 ,
4.415880433163924 ,
4.582575694955841 ,
4.743416490252569 ,
4.898979485566356 ,
5.04975246918104 ,
5.196152422706632 ,
5.338539126015656 ,
5.477225575051661 ,
5.612486080160912 ,
5.744562646538029 ,
5.873670062235366 ,
6.000000000000001 ,
6.123724356957945 ,
6.244997998398398 ,
6.363961030678928 ,
6.48074069840786 ,
6.59545297913646 ,
6.708203932499369 ,
6.819090848492928 ,
6.928203230275509 ,
7.035623639735145 ,
7.14142842854285 ,
7.245688373094719 ,
7.3484692283495345 ,
7.44983221287567 ,
7.54983443527075 ,
7.648529270389178 ,
7.745966692414834]


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

test_points = np.array([[.05, .08],
                [.15, .08],
                [.5, .3]])




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



# rect_trajectory = np.array([[0, 0.1, 0.08, 0],
#                             [3, .1, .25, 0 ],
#                        [5, .5, .25, 0],
#                        [8, .5, .08, 0 ],
#                        [10, 0.1, 0.08, 0]])


rect_trajectory = np.array([[0, .1, .08, 0],
                       [3, .5, .08, 0],
                       [5, .5, .25, 0],
                       [8, .1, .25, 0 ],
                       [10, 0.1, 0.08, 0]])
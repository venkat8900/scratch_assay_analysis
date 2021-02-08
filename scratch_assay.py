from skimage.filters.rank import entropy 
# Adaptive histogram cannot be used as the differnce in pixels is not much.
# entropy measures the degree of randomness. We use the fact that 
# entropy is zero for scratch places. 

from skimage.morphology import disk

from skimage import io
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import threshold_otsu
import glob

time = 0
list_time = []
area_list = []

img_path = "images/scratch_assay/*.*" # change the path accordingly

for file in glob.glob(img_path):
     
    img = io.imread(file)

    # create an entropy filter at image to sperate 2 regions better

    img_entropy = entropy(img, disk(10))
    # plt.imshow(img_entropy)

    # we need to seperate these two regions. 
    # otsu filter works well 
    threshold = threshold_otsu(img_entropy) # find the spot to seperate regions
    print("Threshold value: ", threshold) # prints one single value. 
    # otsu looks and image and gives us the values that is the best for seperating
    # regions

    # now we need to segment regions

    binary_img = img_entropy <= threshold # every image below this pizel value is true
    # plt.imshow(binary_img)
    area_scratch = np.sum(binary_img == 1)
    print(time, area_scratch) 
    list_time.append(time)
    area_list.append(area_scratch)
    time += 1
    
print("Time list: ", list_time)
print("Area List: ", area_list)

plt.plot(list_time, area_list, 'xb-')
plt.legend(['Area', 'Time'])
plt.xlabel('Time')
plt.ylabel('Area')
plt.savefig('time_area.png')
# area is decrasing, i.e. wound is healing

from scipy.stats import linregress # to get stats of plotted graph..ie. rate at which wound is healing

print(linregress(list_time, area_list))
slope, intercept, r_value, p_value, std_err = linregress(list_time, area_list)
print("y = ", slope, "x", "+", intercept)
print("R\N{SUBSCRIPT TWO} = ", r_value**2)
# y =  -2614.030303030303 x + 30595.636363636364
# R₂ =  0.9448801813181574


##################################################################################
##################################################################################
#############                                                      ###############
#############                 INPUT FOR THIS CODE                  ###############
#############                                                      ###############
#############             ANY MEASUREMENT FILE (.csv)              ###############
#############                                                      ###############
#############     Before using this (.csv) file, replace all       ###############
#############     commas (,) with a fullstop (.) and save it.      ###############
#############                                                      ###############
##################################################################################
##################################################################################



# Import required Python libraries
import numpy as np
import csv
import csv_splitter
import matplotlib.pyplot as plt
import matplotlib.colors as cm
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator
from scipy import ndimage
from PIL import Image
import cv2
import os

# Define some easy-to-switch plotting styles which can be tweaked as per requirement
font_size = 14
plt.rcParams["figure.figsize"] = [(0.3*50),(0.2*50)]

label_size = 15
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size

##################################################################################
#############               S E C T I O N    O N E                 ###############
#############                                                      ###############
############# PRE-PROCESS THE (.CSV) FILE TO MAKE IT USABLE FOR    ###############
#############               FURTHER PROCESSING                     ###############
##################################################################################

# Pre-process the (.csv) file by removing spaces/blanks and saving it into one file

# Input (.csv): This is the dynamic rolloff file


dir_name = os.path.dirname(os.path.realpath(__file__))

# Point this as the main directory
src = 'C:/Users/Desktop/PP_Input'

# Rename the measurement file as 'Measurment.csv'
input_file_name = 'Measurement' + '.csv'

input_file = os.path.join(src, input_file_name)
print(" The input measurement file processing right now is : " + input_file)

output_file_name = 'TmpOutput' + '.csv'
output_file = os.path.join(src, output_file_name)
print(" Please find all the frames of measurement here : " + output_file)



with open(input_file,'r') as input, open(output_file, 'w') as output:
    try:
        read = csv.reader(input)
        for r in read:
            non_blank = (line for line in input if line.strip())
            for i in range(15):
                next(read)
            output.writelines(non_blank)
    finally:
        print("Done! TmpOutput is complete!")

# Set the range from which you want to plot the Pressure map.
# Since the first measurement is at 0 ms, it important to either accordingly set the csv_start and csv_end values
# Set the corresponding value for Area

##################################################################################
#############               S E C T I O N    T W O                 ###############
#############                                                      ###############
############# SPLIT THE (.CSV) FILE FRAME-WISE AND SAVE IT IN      ###############
#############                IMAGE FORMAT (.jpg)                   ###############
##################################################################################

csv_start = 411
csv_stop = 525
area = 38.7096
j = 1


os.chdir(src)
os.mkdir('PP')

ppdest = (os.path.join(src, 'PP'))
os.chdir(ppdest)
getval = os.getcwd()

# Split the csv file as per requirement (make necessary changes in csv_splitter)
csv_splitter.split(open(output_file,'r'))
print (" The Pressure files (.csv) can be found here: " + getval)

os.mkdir('PP_Orig')
origdest = (os.path.join(ppdest, 'PP_Orig'))

os.mkdir('PP_Resize')
resdest = (os.path.join(ppdest, 'PP_Resize'))


for i in range(csv_start,csv_stop,1):
    with open('output'+'_'+str(i)+'.csv','r') as file_input:

        # Step 1: Read the (.csv) file. np.genfromtxt is used to read a .csv, the delimiter here is tab
        data_orig = np.genfromtxt(file_input, dtype =int, delimiter = "\t", skip_header = 1)

        # Step 2: Divide the Force values by Area (Force/Area = Pressure)
        data_mod = np.divide(data_orig, area)

        # Step 3: Set the Colormap: 'Jet'. The recommended Colormap though would be 'Viridis'.
        cmap = plt.get_cmap('jet', 11)

        # Step 4: Set all the values over the range as : 'lightgray'
        cmap.set_over('lightgray')

        # Step 5: Set all the values under the range as : 'black'
        cmap.set_under('black')

        # Step 6: Set the limits as 0 to 0.5(Change these values as per requirement)
        norm=cm.BoundaryNorm(np.linspace(0,0.5,11),11)

        # Step 7: pcolor (mapping function)
        plt.pcolor(data_mod, norm = norm, vmin= -0.01, vmax= 0.5, cmap=cmap)

        # Step 8: Plot the colorbar with the ticks mentioned
        cb = plt.colorbar(cmap = cmap, norm = norm, extend='both', ticks=np.linspace(0,0.5,11))

        # Step 9: Change the font and location of label 'PRESS'
        cb.set_label('PRESS', fontsize=20, labelpad=-60, y=1.05, rotation=0)

        # Step 10: Set the font_size as mentioned before
        cb.ax.tick_params(labelsize=font_size)

        # Step 11: Hide tick-labels for X- and Y- axis
        plt.tick_params(axis = 'both', which = 'both', bottom = 'off', top = 'off', right = 'off', left = 'off', labelleft = 'off', labelbottom = 'off')

        # Step 12: Save the plots
        os.chdir(origdest)
        plt.savefig('PP'+'_'+str(j)+'.jpg', cmap = 'jet', bbox_inches = 'tight', dpi = 100)
        os.chdir(ppdest)
        # Increment j to the next number
        j = j + 1

        plt.clf()

##################################################################################
#############               S E C T I O N    T H R E E             ###############
#############                                                      ###############
#############      RESIZE THE (.jpg) IMAGE FILE AND SAVE IT IN     ###############
#############                IMAGE FORMAT (.jpg)                   ###############
##################################################################################

# Set the resize parameters
res_size = (700, 1063)

for i in range(1,114,1):
    os.chdir(origdest)
    img = Image.open('PP'+'_'+ str(i)+'.jpg')
    img = img.resize(res_size, Image.NEAREST)
    os.chdir(resdest)
    img.save('resized_PP'+'_'+ str(i)+'.jpg')

#print (" Success! Program has finished running, please find the original PP files from here: " + origdest)
print (" Success! Program has finished running, please collect the resized PP files from here: " + resdest)

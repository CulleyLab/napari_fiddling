import os.path
import pathlib
from glob import glob
from random import choice
import matplotlib.pyplot as plt
from tifffile import imread
from skimage.transform import rotate
from numpy import flipud, fliplr

# variable to store files that we've already done
visited_files = []

# path names for reading in raw data
raw_path = r"/Users/sianculley/Library/CloudStorage/OneDrive-King'sCollegeLondon/Documents/Pombe database/AV1200/240207/AV1200 fixed/For analysis - DenoiseAI - subset"
raw_path_as_list = raw_path.split(os.sep)
raw_path = pathlib.Path(raw_path)

# path names for saving analysed data
save_path = r"/Users/sianculley/Library/CloudStorage/OneDrive-King'sCollegeLondon/Documents/Pombe database/AV1200/240207/AV1200 fixed/DenoiseAI analysed"
save_path_as_list = save_path.split(os.sep)

found_analysis_file = False

while found_analysis_file == False:

    # read in a file that hasn't been analysed yet
    if len(visited_files)==0:
        file = choice(glob(f'{raw_path}/**/*'))
    else:
        while file in visited_files:
            file = choice(glob(f'{raw_path}/**/*'))
    print(file)

    file_as_list = file.split(os.sep)

    # want to find intermediate folders between raw path and file
    depth_raw = len(raw_path_as_list)
    depth_file = len(file_as_list)

    target_save_path = pathlib.Path(save_path)
    for dir in file_as_list[depth_raw:depth_file]:
        target_save_path = target_save_path.joinpath(pathlib.Path(dir))

    # check if an analysed file already exists at this location
    if target_save_path.exists():
        visited_files.append(file)
    else:
        found_analysis_file = True

# load raw file
raw = imread(file)
plt.imshow(raw)
plt.show()

# apply random rotation
angle = choice([0, 90, 180, 270])
print(angle)
rotated = rotate(raw, angle)
plt.imshow(rotated)
plt.show()

# apply random vertical flip
vertical_flip = choice([0,1])
if vertical_flip == 1:
    print('v flipped!')
    v_flipped = flipud(rotated)
else:
    v_flipped = rotated

# apply random horizontal flip
horizontal_flip = choice([0,1])
if horizontal_flip == 1:
    print('h flipped!')
    h_flipped = fliplr(v_flipped)
else:
    h_flipped = v_flipped

plt.imshow(h_flipped)
plt.show()




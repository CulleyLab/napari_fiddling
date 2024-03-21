import os.path
import pathlib
from glob import glob
from random import choice

path = r"/Users/sianculley/Library/CloudStorage/OneDrive-King'sCollegeLondon/Documents/Pombe database/AV1200/240207/AV1200 fixed/For analysis - DenoiseAI"
path_as_list = path.split(os.sep)
path = pathlib.Path(path)

file = choice(glob(f'{path}/**/*'))
print(file)

path2 = r"/Users/sianculley/Library/CloudStorage/OneDrive-King'sCollegeLondon/Documents/Pombe database/AV1200/240207/AV1200 fixed/DenoiseAI analysed"

file_as_list = file.split(os.sep)

save_string = ''
for i in range(len(file_as_list)-1):
    if file_as_list[i] == path_as_list[i]:
        continue
    else:
        save_string += file_as_list[i]
        save_string += os.sep

print(save_string)
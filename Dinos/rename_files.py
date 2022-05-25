import os

address = "D:\PhotoshopWork\Pictures"

# rename all the files under a directory

for folder in os.listdir(address):
    for file in os.listdir(address + "\\" + folder):
        file_name = address + "\\" + folder + "\\" + file
        os.rename(file_name, address + "\\" + folder + "\\" + file_name.split("_")[-1])


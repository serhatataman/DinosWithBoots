import os

for i in range(2):
    file_path = "./metadata/" + str(i+1)
    os.rename(file_path + ".json", file_path)





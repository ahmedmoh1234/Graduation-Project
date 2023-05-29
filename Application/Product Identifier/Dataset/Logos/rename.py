import os

def renameFiles():
    file_list = os.listdir()
    print(file_list)

    counter = 1
    for file_name in file_list:
        fileExt = file_name.split(".")[-1]
        if fileExt == "py":
            continue
        print(f"Renaming {file_name} to {counter}.{fileExt}")
        os.rename(file_name, str(counter) + "." + fileExt)
        counter += 1

renameFiles()


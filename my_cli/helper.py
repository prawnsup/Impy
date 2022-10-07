from os.path import exists


def converter(file):
    ext = checker(file)
    if ext != '.txt':
        return [file]  # file is equivalent to single file name
    if exists(file):
        path = file
    else:
        print(f"[Error]File {file} not found")
        exit()
    with open(path) as f:
        images_list = [x.rstrip('\n') for x in f]
        for i in images_list:
            checker(i)
        f.close()
        return images_list


def checker(file, type='None'):
    try:
        ext = file[file.rindex('.'):len(file)]
        if len(ext) < 2:
            print(f"[Error] Please specify file extension for the filename: [{file}]")
            exit()
        elif type != 'None':
            if type != ext:
                print(f"[Error] Please make sure file extension for file [{file}] is {type}")
                exit()
            else:
                return file
    except ValueError:
        print(f"[Error] Please specify file extension for filename: [{file}]")
        exit()
    return ext

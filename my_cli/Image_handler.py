import os
from PIL import Image
from PyPDF2 import PdfFileMerger


class ImageHandler:  # class specially made to handle images within a directory
    def __init__(self, cd):
        self.path = cd  # going to hold the current directory we are working in
        self.extensions_dic = {
            'JPEG': ['.jfif', '.jpe', '.jpeg', '.jpg'],
            'PNG': ['.apng', '.png'],
            'PPM': ['.pbm'],
            'PSD': ['.psd'],
            'ICO': ['.ico'],
        }
        self.extensions_dic_c = {  # This dictionary is for file conversions
            'JPEG': ['.jfif', '.jpe', '.jpeg', '.jpg'],
            'PNG': ['.apng', '.png'],
            'PPM': ['.pbm'],
            'PSD': ['.psd'],
            'ICO': ['.ico'],
            'PDF': ['.pdf']
        }
        self.extensions_c = {'.jfif', '.jpe', '.jpeg', '.jpg', '.apng', '.png', '.pbm', '.pgm', '.pnm', '.ppm', '.psd',
                             '.ico', '.pdf'}  # list of extensions for conversion
        self.extensions = {'.jfif', '.jpe', '.jpeg', '.jpg', '.apng', '.png', '.pbm', '.pgm', '.pnm', '.ppm', '.psd',
                           '.ico'}
        self.images = []  # Used to store images that are currently being worked with

    def mapping(self, ex, dic):  # maps the extension to correct format to use for saving file
        if dic is None:
            dic = self.extensions_dic
        for key in dic:
            if ex in dic:
                return key

    # Function that checks to see whether a path is possible based on input .
    # Can accept paths from current directory and new paths.
    def validate(self, path):
        if not os.path.isdir(self.path + path):
            if not os.path.isdir(path):
                print(f"[Error]incorrect path specified please try again: {path}")
                exit()
        else:
            path = self.path + path
        return os.listdir(path), path

    # convert function parameters --> str:path , str:item , str:ext , str:name
    def convert(self, path, item, extension, destination, name='.', ):

        ext_item = item[item.rindex('.'):len(item)]
        if ext_item not in self.extensions:
            print(f"[Error]{item} is not a supported file type to convert from")
            return
        if extension not in self.extensions_c:
            print(f"[Error]{extension} is not a supported extension to convert to ")
            return
        if ext_item == extension:
            print(f"[Error]You are trying to convert to same extension : Item {item} is being converted to {extension}")
            return

        # determine image name based on the parameter.
        if name == ".":
            name = item[0:item.rindex('.')]
        # need to convert RGBA to RGB to convert to pdf/jpg etc  - didn't have a clue till stack overflow
        # https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil

        if ext_item in ['.png',
                        '.apng']:
            file_path_open = path + "/" + item
            file_path_save = destination + "/" + name + extension
            img = Image.open(file_path_open)
            img.load()
            print(f"trying to convert file: {item} to extension: {extension}")
            img1 = Image.new("RGB", img.size, (255, 255, 255))
            img1.paste(img, mask=img.split()[3])
            img1.save(file_path_save[0:file_path_save.rindex('.')] + extension,
                      self.mapping(extension, self.extensions_dic_c), quality=90)
            print(f"converted file {item} to {extension}  , stored at {file_path_save}")
            return
        file_path_open = path + "/" + item
        file_path_save = destination + "/" + name + extension
        img = Image.open(file_path_open)
        img.save(file_path_save, self.mapping(extension , self.extensions_dic), quality=100)
        print(f"converted file {item} to {extension}  , stored at {file_path_save}")

    # PDF function Parameters -->  str:path , str[] images , bool merge , str name]
    def pdf(self, path, pdfs, name, destination):
        if destination != self.path:  # checks if default destination is specified
            x, destination = self.validate(destination)
        if path != "":
            files, path = self.validate(path)
            # Determines path to be used.
        else:
            files = os.listdir(
                self.path)  # if no input is given then default self.path value used- which is os.getcwd().
            path = self.path

        # if no image argument then just searches whole directory
        if pdfs[0] == 'all':
            for img in files:
                try:
                    ext = img[img.rindex('.'):len(img)]
                except ValueError:
                    continue
                if ext == ".pdf":
                    self.images.append(img)  # adds pdfs to list
        else:
            for img in pdfs:
                if not os.path.exists(path + "/" + img):
                    print(f"[Error]Image {img} does not seem to exist in dir {path}.")
                else:
                    self.images.append(img)
        if len(self.images) == 0:
            print("[Error] No images/files found matching specifications")
            return
        # merge sequence
        merger = PdfFileMerger()
        pdfs = [(path + "/" + i) for i in self.images]
        for i in pdfs:
            print(f"Merging ({i}) ")
            try:
                merger.append(i)
            except:
                print(f"[Error] File {i} has a problem. May be corrupted or empty")

        if name == '.':
            merger.write(destination + "/" + "newpdf.pdf")
            print(f"Finished merging to {path}/newfile.pdf")
        else:
            merger.write(destination + "/" + name + ".pdf")
            print(f"Finished merging to {destination}/{name}.pdf")

    def convert_proper(self, path, images, extension, name, destination):
        if destination != "/converted":
            x, destination = self.validate(destination)
        else:
            destination = self.path + destination
            if not os.path.isdir(destination):
                os.makedirs(destination)

        if path != "":
            files, path = self.validate(path)
            # if path is specified then we add that on to current working directory
        else:
            files = os.listdir(
                self.path)  # if no input is given then default self.path value used- which is os.getcwd().
            path = self.path
        if images[0] == 'all':
            for img in files:
                if img[img.rindex('.'):len(img)] in self.extensions_c:
                    self.convert(path, img, extension, destination)
                    self.images.append(img)  # adds name of images to list
        else:
            for img in images:
                if img[img.rindex('.'):len(img)] in self.extensions:
                    if not os.path.exists(path + "/" + img):
                        print(f"[Error]Image [{img}] does not seem to exist.")
                        continue
                    self.convert(path, img, extension, destination, name)
                    self.images.append(
                        img)
        if len(self.images) == 0:
            print("[Error] No images/files found matching specifications")

    def rescale_helper(self, file_path, item, height, width, resize_ratio, extension):
        image = Image.open(file_path)
        if height != 0 and width == 0:
            width = height * image.size[0] / image.size[1]
            print(f"Resized image:{item} height to {int(width)} and height to {int(height)}.Aspect ratio maintained")
        elif width != 0 and height == 0:
            height = width * image.size[1] / image.size[0]
            print(f"Resized image:{item} width to {int(width)} and height to {int(height)}.Aspect ratio maintained")
        elif resize_ratio != 1.0:
            width = image.size[0] / (1 / resize_ratio)
            height = image.size[1] / (1 / resize_ratio)
            print(f"Rescaled image:{item} by a factor of {resize_ratio}")
        else:
            print(f"Resized image:{item} height to {int(width)} and height to {int(height)})")
        image = image.resize((int(width), int(height)), Image.ANTIALIAS)
        image.save(file_path, self.mapping(extension , self.extensions_dic_c), quality=90)
        image.close()

    # rescale function parameters --> str:path , int:resize_ratio ,  str[]:images
    def rescale(self, path, resize_ratio, images, height, width):
        image_b = False
        if path != "":
            files, path = self.validate(path)
        else:
            # if no input is given then default self.path value used- which is os.getcwd().
            files = os.listdir(self.path)
            path = self.path

        # if no image argument then just searches whole directory
        if images[0] == 'all':
            # loop through all images in directory and resizes them
            for item in files:
                extension = item[item.rindex('.'):len(item)]
                if extension in self.extensions:
                    self.rescale_helper(path + "/" + item, item, height, width, resize_ratio, extension)
                    image_b = True
            if image_b is False:
                print(f"[Error]There were no images within directory at path specified {path}:")

        else:
            for img in images:
                try:
                    ext = img[img.rindex('.'):len(img)]
                except ValueError:
                    print(f"[Error] image extension is not specified.The image name is {img}. ")
                    return
                if ext in self.extensions:
                    self.images.append(img)
            if len(self.images) > 0:
                for item in files:
                    if item in images:
                        if ext in self.extensions:
                            self.rescale_helper(path + "/" + item, item, height, width, resize_ratio, ext)
                            image_b = True
                if image_b is False:
                    print(f"[Error]There were no supported images within directory at path specified {path}:")
            else:
                print(f"[Error] None of the images were of the supported extension type")

import click
import os

from .Image_handler import ImageHandler
from .helper import checker
from .helper import converter


@click.group()
def impy():
    pass


@click.command('rescale', short_help="rescales images")
@click.option('--path', '-p', default="", type=click.Path(exists=False),
              help='The area you want this cli to work in, default is current directory')
@click.option('--rescale', '-re', default=1.0,
              help="This is equal to the multiplier you want to rescale your images by.")
@click.argument('image', default='all', type=click.Path(exists=False))
@click.option('--height', '-h', default=0.0, help="New height(pixels) of images specified")
@click.option('--width', '-w', default=0.0, help="New width(pixels) of images specified")
def rescaler(path, rescale, image, height, width):
    if image != 'all':
        images_list = converter(image)
    else:
        if height != 0 or width != 0:
            if rescale != 1.0:
                print(f"[Error] Can't rescale while assigning new width and height.")
                return

        images_list = [image]  # in this case images list = ['all'] or a singular image name ['name']
    im = ImageHandler(os.getcwd())
    im.rescale(path, rescale, images_list, height, width)


@click.command("merge_pdf", short_help="Used to merge pdfs")
@click.option('--path', '-p', default="", type=click.Path(exists=False),
              help='The working directory containing the files, default is current directory')
@click.argument('pdfs', default='all',
                type=click.Path(exists=False))  # image can be input as a single image or file/path of file
@click.option('--add', '-ad', default=[], multiple=True, help="Pdf file you are adding together with specified pdf/s")
@click.option('--name', '-n', default='.', help="Name of merged pdf. Default is new.pdf")
@click.option('--destination', '-d', default=os.getcwd(), type=click.Path(exists=True),
              help="Destination address for merged files.Default is Current directory", required=False)
def merge_pdf(path, pdfs, add, name, destination):
    """merge_pdf -p /heart images.txt.
       merge_pdf -p /heart -n output

       PDFS is the name of original pdf or it's the text file containing names of pdfs to be merged.Each
       pdf has to be within path specified.

       If pdfs argument is not specified then every PDF within the directory will be merged into a file.

        """
    check = False
    if pdfs != 'all':
        images_list = converter(pdfs)
    else:
        images_list = [pdfs]  # in this case images list = ['all']
    if add:
        for i in add:
            images_list.append(checker(i, '.pdf'))

    if len(images_list) == 1 and pdfs != 'all':
        if pdfs != 'all':
            while not check:
                im = click.prompt("Please add a pdf that you want to merge with, type n to exit")
                if im in {"N", "No", "no", "n"} or im == "":
                    print("Exiting Impy")
                    exit()
                else:
                    images_list.append(checker(im, '.pdf'))
                    if not click.confirm("Do you want to add more pdfs?"):
                        check = True

    im = ImageHandler(os.getcwd())
    im.pdf(path, images_list, name, destination)


@click.command("convert", short_help="Used to convert files to a specified extension")
@click.option('--path', '-p', default="", type=click.Path(exists=False),
              help='The area you want to work in, default is current directory')
@click.argument('image', default='all', type=click.Path(exists=False))  # image can be input as a single image or file
@click.option('--name', '-n', default='.',
              help="Name of converted . Default is same name")
@click.option('--extension', '-ex', help="Extension to be converted to", required=True)
@click.option('--destination', '-d', default="/converted", type=click.Path(exists=False),
              help="Destination address for converted files")
def convert(path, image, name, extension, destination):
    """ convert -f -p /heart -ex .jpg images.txt
        convert -p /heart -ex .jpg  -d /jpgs 3.png

       IMAGE is the name of the image .
       If the --file parameter is specified then its a text file containing names of images.
            """
    if image != 'all':
        # check if file containing imagelist exists
        images_list = converter(image)
    else:
        images_list = [image]
    if len(images_list) > 1 and name != '.':
        print(f"[Error] Can't have name parameter when there are multiple outputs")
        return
    im = ImageHandler(os.getcwd())
    im.convert_proper(path, images_list, extension, name, destination)


impy.add_command(rescaler)
impy.add_command(merge_pdf)
impy.add_command(convert)

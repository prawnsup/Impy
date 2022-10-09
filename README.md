# Impy
Image manipulation and PDF merging python Command Line Interface (CLI)

# Installation

Only works for UNIX distributions so far. Install using curl or wget.

Navigate to directory you wish to download to.
```
  curl https://github.com/prawnsup/Impy/raw/master/dist/impy-0.1.4-py3-none-any.whl
  pip install impy-0.1.4-py3-none-any.whl
```

# Usage

Currently no support for chaining multiple commands. So impy [Command] [Command] will not work.

If file names are stored in text file then they must be formatted like shown below:


<img width="228" alt="Screenshot 2022-10-09 at 12 35 41" src="https://user-images.githubusercontent.com/75863764/194754691-b273b78a-9a37-42df-8ba4-619d84ce3b2b.png">
Each file name must be seperated by a newline.

To get general and command specific help. Use:
```
impy --help
impy [COMMAND] --help 
```

Supported commands at the moment:
```
Commands:
  convert    Used to convert files to a specified extension
  merge_pdf  Used to merge pdfs
  rescale    Rescales images
```
# Contributions
Feel free to modify the code in a seperate branch and create pull requests. I am working on creating tests for each command, any help related to that
would be greatly appreciated :) . Make sure to include an updated .whl file in the dist folder. 



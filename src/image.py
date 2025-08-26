from PIL import Image
import os

img_path = r"C:\Users\PMLS\Downloads\test_tools_genomics_workbenchmark\src\image.png"
ico_path = r"C:\Users\PMLS\Downloads\test_tools_genomics_workbenchmark\src\image.ico"
img = Image.open(img_path)
icon_sizes = [(256, 256), (64, 64), (32, 32), (16, 16)]
img.save(ico_path, format='ICO', sizes=icon_sizes)
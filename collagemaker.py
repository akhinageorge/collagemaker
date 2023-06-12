import os
from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageFont
import random
from math import ceil,sqrt
import glob

class CollageMaker:
    ''' The class created to make the collage using images from a file and then rotate the grid'''

    def __init__(self, target_size, rotation_angle,width,height):
        ''' The initialization function includes the:
        1. Rotation angle (angle of rotating the grid)
        2. Target size (the desired size of each image in the collage, defined in pixels)'''

        self.target_size = target_size
        self.rotation_angle = rotation_angle
        self.crop_width=width
        self.crop_height=height

    def resize_and_crop(self, image_path):
        ''' This function is used to crop the image. It calculates the aspect ratio of both the target size
            and the original image. Depending on the aspect ratios, it determines the scale factor for
            resizing the image while maintaining the aspect ratio.'''
        
        image = Image.open(image_path)
        width, height = image.size

        new_width = self.target_size[0]
        new_height = self.target_size[1]
        resized_image = image.resize((new_width, new_height))

        left = (new_width - self.target_size[0]) // 2
        top = (new_height - self.target_size[1]) // 2
        right = left + self.target_size[0]
        bottom = top + self.target_size[1]
        cropped_image = resized_image.crop((left, top, right, bottom))
        return cropped_image

    def create_collage(self, folder_path):
        ''' This function creates the grid for the collage, appends the resized images to it, and rotates 
            the grid altogether. The number of rows and columns in the collage is calculated based on 
            the canvas size and the target size of each image. '''
        
        image_files = [file for file in os.listdir(folder_path) if file.endswith((".jpg", ".jpeg", ".png"))]
        random.shuffle(image_files)

        total_images = len(image_files)
        total_width = self.target_size[0] * ceil(sqrt(total_images))
        total_height = self.target_size[1] * ceil(sqrt(total_images))
        num_columns = total_width // self.target_size[0]
        num_rows = total_height // self.target_size[1]

        padding=10
        padding_color = (0, 0, 0)  
        padding_image = Image.new("RGB", (self.target_size[0] + padding, self.target_size[1] + padding), padding_color)

        grid_width = num_columns * self.target_size[0]
        grid_height = num_rows * self.target_size[1]
        grid_image = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

        for i, file_name in enumerate(image_files):
            image_path = os.path.join(folder_path, file_name)
            resized_image = self.resize_and_crop(image_path)
            x = ((i % num_columns) * (self.target_size[0] + padding))
            y = ((i // num_columns) * (self.target_size[1] + padding))
            grid_image.paste(padding_image, (x, y))
            grid_image.paste(resized_image, (x + padding, y + padding))

        rotated_grid_image = grid_image.rotate(self.rotation_angle, expand=False)

        
        crop_offset_x = (rotated_grid_image.width - self.crop_width) // 2
        crop_offset_y = (rotated_grid_image.height - self.crop_height) // 2
        crop_left = crop_offset_x + 50
        crop_top = crop_offset_y -  50
        crop_right = crop_left + self.crop_width
        crop_bottom = crop_top + self.crop_height
        cropped_image = rotated_grid_image.crop((crop_left, crop_top, crop_right, crop_bottom))

        overlay_image_path = "Collage Maker\Rectangle 4.png"
        overlay_image = Image.open(overlay_image_path)
        cropped_image = cropped_image.convert("RGBA")
        overlay_image = overlay_image.resize(cropped_image.size)
        overlay_image = overlay_image.convert("RGBA")  # Convert overlay image to RGBA mode
        final_image = Image.alpha_composite(cropped_image, overlay_image)
        final_image.show()

target_size = (300, 400)
rotation_angle = -20
width=2500
height=1500
collage_maker = CollageMaker(target_size, rotation_angle, width, height)
file_paths = glob.glob("Collage Maker/Images")
collage_maker.create_collage(file_paths[0],text)  

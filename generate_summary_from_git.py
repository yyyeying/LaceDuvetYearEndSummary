from typing import List
import subprocess
from Coordinates.coordinates import Coordinates
from ImageGenerator.image_generate_git import ImageGeneratorGit

if __name__ == '__main__':
    start_date = [2022, 1, 1]
    end_date = [2022, 3, 31]
    coords = Coordinates(start_date=start_date, end_date=end_date)
    coords.gen_coord_list_from_git()
    img_gen = ImageGeneratorGit(coords=coords)
    img_gen.generate()
    coords.statistics()

import csv
import sys

class Palette(object):
    palette_type = 'dmcfloss'
    palette_list = []

    def __init__(self, palette_type):
        # As of now, the only valid type is 'dmcfloss'
        self.palette_type = palette_type or 'dmcfloss'
        self.palette_list = self._build_palette()

    def _build_palette(self):
        if self.palette_type == 'dmcfloss':
            return self._load_dmc_floss()
        else:
            return

    def _load_dmc_floss(self):
        floss_list = []
        with open('DMCFloss.csv', 'U') as csv_file:
            reader = csv.DictReader(csv_file)
            for row_dict in reader:
                # clean it up into integers
                row_dict['Red'] = int(row_dict['Red'])
                row_dict['Green'] = int(row_dict['Green'])
                row_dict['Blue'] = int(row_dict['Blue'])
                floss_list.append(row_dict)
        return floss_list

    def find_floss(self, red, green, blue):
        """
        Given an RGB value, find the closest DMC floss
        :param red:
        :param green:
        :param blue:
        :return: Floss Number

        TODO: This needs to be cleaned up when other palette options are added
        """

        # todo: make this work

        input_RGB = (red, green, blue)
        min_distance = sys.maxsize
        floss_num = None
        for item in self.palette_list:
            floss_RGB = (item['Red'], item['Green'], item['Blue'])
            dist = self.distance_sqrd(input_RGB, floss_RGB)
            if dist < min_distance:
                min_distance = dist
                floss_num = item['Floss#'].strip()
                rgb_hex = item['RGB code']
        return floss_num, rgb_hex

    def distance_sqrd(self, input_RGB, floss_RGB):
        distance_sqrd = (floss_RGB[0]-input_RGB[0])**2 + (floss_RGB[1]-input_RGB[1])**2 + (floss_RGB[2]-input_RGB[2])**2
        return distance_sqrd

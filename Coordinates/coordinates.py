from typing import List
import os
import yaml
import collections

from Coordinates.coordinate import Coordinate


class Coordinates(object):
    def __init__(self, start_date: List[int], end_date: List[int]):
        self.coord_list: List[Coordinate] = []
        self.colors = {}
        self.brands = {}
        self.dresses = {}
        self.types = {}
        self.start_date = start_date
        self.end_date = end_date

    def date_compare(self, date: List[int]) -> bool:
        if date[0] < self.start_date[0] or date[0] > self.end_date[0]:
            return False
        if date[0] == self.start_date[0]:
            if date[1] < self.start_date[1]:
                return False
            elif date[1] == self.start_date[1]:
                if date[2] < self.start_date[2]:
                    return False
        if date[0] == self.end_date[0]:
            if date[1] > self.end_date[1]:
                return False
            elif date[1] == self.end_date[1]:
                if date[2] > self.end_date[2]:
                    return False
        return True

    def gen_coord_list_from_git(self):
        year_list = list(range(self.start_date[0], self.end_date[0] + 1))
        print(os.popen("git submodule update --remote").read())
        for year in year_list:
            yaml_file = os.path.join(os.getcwd(), "DuvetsCoordinatesToday", str(year), "info.yaml")
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.load(f.read(), Loader=yaml.FullLoader)
            for month_data in data:
                for day_data in month_data['dates']:
                    date = [year, month_data['month'], day_data['date']]
                    # print(day_data)
                    if self.date_compare(date):
                        brand = day_data['coordinates']['brand']
                        name = [day_data['coordinates']["primary_name"]]
                        if "secondary_name" in day_data['coordinates'].keys():
                            name.append(day_data['coordinates']["secondary_name"])
                        # print(name)
                        type_ = day_data['coordinates']['type']
                        color = [day_data['coordinates']['color']] \
                            if "color" in day_data['coordinates'].keys() else None
                        if "color_2" in day_data['coordinates'].keys():
                            color.append(day_data['coordinates']['color_2'])
                        images = []
                        for image in day_data['files']:
                            if "bust" in image or "full_body" in image:
                                images.append(os.path.join(os.getcwd(),
                                                           "DuvetsCoordinatesToday",
                                                           str(year),
                                                           str(date[1]).zfill(2),
                                                           image))
                        # print(images)
                        new_coord = Coordinate(date=date,
                                               brand=brand,
                                               name=name,
                                               type=type_,
                                               color=color,
                                               images=images)
                        self.coord_list.append(new_coord)

    def statistics(self):
        self.brands = collections.Counter([c.brand for c in self.coord_list])
        cs = []
        for c in self.coord_list:
            if c.color is not None:
                for r in c.color:
                    cs.append(r)
        self.colors = collections.Counter(cs)
        self.dresses = collections.Counter([c.name[-1] for c in self.coord_list])
        self.types = collections.Counter([c.type for c in self.coord_list])
        print("Total: {}".format(len(self.coord_list)))
        print(self.brands)
        print(self.colors)
        print(self.dresses)
        print(self.types)


if __name__ == '__main__':
    start_date = [2022, 1, 15]
    end_date = [2022, 3, 23]
    coords = Coordinates(start_date=start_date, end_date=end_date)
    print(coords.date_compare([2022, 3, 25]))

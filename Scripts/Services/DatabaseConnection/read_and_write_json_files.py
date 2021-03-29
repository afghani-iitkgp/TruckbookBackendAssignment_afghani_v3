import os
import json
from collections import defaultdict


from Constants import const
from Scripts.Utility import utils


def intersection_stations_list(file_name):
    try:
        input_file = open(file_name, 'r')
        file_content = input_file.read()
        input_file.close()
        # output_nospace = file_content.replace('\u200b', '').replace('\n', '').replace(' ', '')
        output_nospace = file_content.replace('\u200b', '').replace('\n', '').strip()

        intersections_line_dict = defaultdict(list)
        intersections_lst = []
        for i in output_nospace.split(','):
            if 'intersection' in i:
                intersections_line_dict[file_name.split('/')[-1].split('.')[0]].append(i.split('(')[0].strip())
                intersections_lst.append(i.split('(')[0].strip())

        return intersections_line_dict, intersections_lst

        # print(output_nospace.split(','))

    except Exception as e:
        utils.logger.error("-Error--" + str(e))


def stations_line_wise(file_name):
    try:
        input_file = open(file_name, 'r')
        file_content = input_file.read()
        input_file.close()
        # output_nospace = file_content.replace('\u200b', '').replace('\n', '').replace(' ', '')
        output_nospace = file_content.replace('\u200b', '').replace('\n', '').strip()

        stations_line_wise = defaultdict(list)
        for i in output_nospace.split(','):
            stations_line_wise[file_name.split('/')[-1].split('.')[0]].append(i.strip())

        return stations_line_wise

    except Exception as e:
        utils.logger.error("-Error--" + str(e))


def fetch_all_intersections(root_dir):
    # traverse root directory, and list directories as dirs and files as files

    for root, dirs, files in os.walk(root_dir):
        try:
            path = root.split(os.sep)
            # print((len(path) - 1) * '---', os.path.basename(root))
            intersections_list_of_dicts = []
            total_intersections_lst = []
            for file in files:
                # print(os.path.join(root_dir, file))
                file_path = os.path.join(root_dir, file)

                # print(stations_line_wise(file_path))
                intersections_linewise_dict, intersections_stations_lst = intersection_stations_list(file_path)
                intersections_list_of_dicts.append(intersections_linewise_dict)
                total_intersections_lst.extend(intersections_stations_lst)


            return intersections_list_of_dicts, list(set(total_intersections_lst))

        except Exception as e:
            utils.logger.error("-Error--" + str(e))


def fetch_all_stations_linewise(root_dir):
    # traverse root directory, and list directories as dirs and files as files

    for root, dirs, files in os.walk(root_dir):
        try:
            path = root.split(os.sep)
            # print((len(path) - 1) * '---', os.path.basename(root))
            lst_stations = []
            for file in files:

                # print(os.path.join(root_dir, file))
                file_path = os.path.join(root_dir, file)

                # print(stations_line_wise(file_path))
                lst_stations.append(stations_line_wise(file_path))

            return lst_stations

        except Exception as e:
            utils.logger.error("-Error--" + str(e))

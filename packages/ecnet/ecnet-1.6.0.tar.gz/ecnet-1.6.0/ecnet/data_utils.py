#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ecnet/data_utils.py
# v.1.6.0
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains the "DataFrame" class, and functions for processing/importing/
# outputting data. High-level usage is handled by the "Server" class in
# server.py.
#

# Stdlib imports
from csv import reader, writer, QUOTE_ALL
from random import sample

# 3rd party imports
from numpy import asarray


class DataPoint:

    def __init__(self):
        '''
        DataPoint object: houses row in CSV database, containing ID, set
        assignment, strings, groups, targets and inputs
        '''

        self.id = None
        self.assignment = None
        self.strings = []
        self.groups = []
        self.targets = []
        self.inputs = []


class PackagedData:

    def __init__(self):
        '''
        PackagedData object: contains lists of input and target data for data
        set assignments
        '''

        self.learn_x = []
        self.learn_y = []
        self.valid_x = []
        self.valid_y = []
        self.test_x = []
        self.test_y = []


class DataFrame:

    def __init__(self, filename):
        '''
        DataFrame object: handles data importing, set splitting, shuffling,
        packaging

        Args:
            filename (str): path to ECNet-formatted CSV database
        '''

        if '.csv' not in filename:
            filename += '.csv'
        try:
            with open(filename, newline='') as file:
                data_raw = list(reader(file))
        except FileNotFoundError:
            raise Exception('CSV database not found: {}'.format(filename))

        self.data_points = []
        for point in range(2, len([sublist[0] for sublist in data_raw])):
            new_point = DataPoint()
            new_point.id = [sublist[0] for sublist in data_raw][point]
            for header in range(len(data_raw[0])):
                if 'STRING' in data_raw[0][header]:
                    new_point.strings.append(data_raw[point][header])
                elif 'GROUP' in data_raw[0][header]:
                    new_point.groups.append(data_raw[point][header])
                elif 'TARGET' in data_raw[0][header]:
                    new_point.targets.append(data_raw[point][header])
                elif 'INPUT' in data_raw[0][header]:
                    new_point.inputs.append(data_raw[point][header])
                elif 'ASSIGNMENT' in data_raw[0][header]:
                    new_point.assignment = data_raw[point][header]
                elif 'DATAID' in data_raw[0][header]:
                    new_point.id = data_raw[point][header]
            self.data_points.append(new_point)

        self.string_names = []
        self.group_names = []
        self.target_names = []
        self.input_names = []
        for header in range(len(data_raw[0])):
            if 'STRING' in data_raw[0][header]:
                self.string_names.append(data_raw[1][header])
            if 'GROUP' in data_raw[0][header]:
                self.group_names.append(data_raw[1][header])
            if 'TARGET' in data_raw[0][header]:
                self.target_names.append(data_raw[1][header])
            if 'INPUT' in data_raw[0][header]:
                self.input_names.append(data_raw[1][header])
        self.num_strings = len(self.string_names)
        self.num_groups = len(self.group_names)
        self.num_targets = len(self.target_names)
        self.num_inputs = len(self.input_names)

    def __len__(self):
        '''
        DataFrame length == number of DataPoints
        '''

        return len(self.data_points)

    def create_sets(self, random=False, split=[0.65, 0.25, 0.1]):
        '''
        Creates learning, validation and test sets

        Args:
            random (bool): if True, use random assignments for learn, validate,
                           test sets
            split (list): [learn%, valid%, test%] if random == True
        '''

        self.learn_set = []
        self.valid_set = []
        self.test_set = []

        if random:
            rand_index = sample(range(len(self)), len(self))
            split_locs = [
                int(len(rand_index) * split[0]),
                int(len(rand_index) * (split[0] + split[1])),
            ]
            learn_index = rand_index[0: split_locs[0]]
            valid_index = rand_index[split_locs[0]: split_locs[1]]
            test_index = rand_index[split_locs[1]:]
            for idx in learn_index:
                self.data_points[idx].assignment = 'L'
                self.learn_set.append(self.data_points[idx])
            for idx in valid_index:
                self.data_points[idx].assignment = 'V'
                self.valid_set.append(self.data_points[idx])
            for idx in test_index:
                self.data_points[idx].assignment = 'T'
                self.test_set.append(self.data_points[idx])

        else:
            for point in self.data_points:
                if point.assignment == 'L':
                    self.learn_set.append(point)
                elif point.assignment == 'V':
                    self.valid_set.append(point)
                elif point.assignment == 'T':
                    self.test_set.append(point)

    def create_sorted_sets(self, sort_string, split=[0.65, 0.25, 0.1]):
        '''
        Creates random learn, validate and test sets, ensuring data points with
        the supplied sort string are split proportionally between the sets

        Args:
            sort_string (str): database STRING value used to sort data points
            split (list): [learn%, valid%, test%] for set assignments
        '''
        try:
            string_idx = self.string_names.index(sort_string)
        except ValueError:
            raise Exception('{} not found in STRING names'.format(sort_string))
        self.data_points.sort(key=lambda x: x.strings[string_idx])

        string_vals = []
        string_groups = []

        for point in self.data_points:
            if point.strings[string_idx] not in string_vals:
                string_vals.append(point.strings[string_idx])
                string_groups.append([point])
            else:
                string_groups[-1].append(point)

        self.learn_set = []
        self.valid_set = []
        self.test_set = []

        for group in string_groups:
            split_locs = [
                int(len(group) * split[0]),
                int(len(group) * (split[0] + split[1])),
            ]
            for point in group[0: split_locs[0]]:
                point.assignment = 'L'
                self.learn_set.append(point)
            for point in group[split_locs[0]: split_locs[1]]:
                point.assignment = 'V'
                self.valid_set.append(point)
            for point in group[split_locs[1]:]:
                point.assignment = 'T'
                self.test_set.append(point)

    def shuffle(self, *args, split=[0.65, 0.25, 0.1]):
        '''
        Shuffles (new random assignments) learn, validate, test sets

        Args:
            *args (str): 'l', 'v', and/or 't', specifies whether to shuffle
                         learn, validate and/or test sets
            split (list): [learn%, valid%, test%] used for new assignments
        '''

        if 'l' and 'v' and 't' in args:
            self.create_sets(random=True, split=split)

        elif 'l' and 'v' in args:
            lv_set = []
            for point in self.learn_set:
                lv_set.append(point)
            for point in self.valid_set:
                lv_set.append(point)
            rand_index = sample(
                range(len(self.learn_set) + len(self.valid_set)),
                (len(self.learn_set) + len(self.valid_set))
            )
            learn_index = rand_index[
                0: int(len(rand_index) * (split[0] / (1 - split[2]))) + 1
            ]
            valid_index = rand_index[
                int(len(rand_index) * (split[0] / (1 - split[2]))) + 1:
            ]

            self.learn_set = []
            self.valid_set = []

            for idx in learn_index:
                self.learn_set.append(lv_set[idx])
            for idx in valid_index:
                self.valid_set.append(lv_set[idx])

        else:
            raise Exception('Shuffle arguments must be *l, v, t* or *l, v')

    def package_sets(self):
        '''
        Packages learn, validate and test sets for model hand-off

        Returns:
            PackagedData: object containing learn, validate and test inputs
                          and targets
        '''

        pd = PackagedData()
        for point in self.learn_set:
            pd.learn_x.append(asarray(point.inputs).astype('float32'))
            pd.learn_y.append(asarray(point.targets).astype('float32'))
        for point in self.valid_set:
            pd.valid_x.append(asarray(point.inputs).astype('float32'))
            pd.valid_y.append(asarray(point.targets).astype('float32'))
        for point in self.test_set:
            pd.test_x.append(asarray(point.inputs).astype('float32'))
            pd.test_y.append(asarray(point.targets).astype('float32'))

        pd.learn_x = asarray(pd.learn_x)
        pd.learn_y = asarray(pd.learn_y)
        pd.valid_x = asarray(pd.valid_x)
        pd.valid_y = asarray(pd.valid_y)
        pd.test_x = asarray(pd.test_x)
        pd.test_y = asarray(pd.test_y)
        return pd


def save_results(results, DataFrame, filename):
    '''
    Saves results obtained from ecnet.Server.use_model()

    Args:
        results (list): list of lists, where sublists are predicted data for
                        each data point
        DataFrame (DataFrame): data_utils.DataFrame object used for results
                               file formatting
        filename (str): path to save location for results
    '''

    if '.csv' not in filename:
        filename += '.csv'

    rows = []

    type_row = []
    type_row.append('DATAID')
    type_row.append('ASSIGNMENT')
    for string in range(DataFrame.num_strings):
        type_row.append('STRING')
    for group in range(DataFrame.num_groups):
        type_row.append('GROUP')
    for target in range(DataFrame.num_targets):
        type_row.append('TARGET')
    for result in results:
        type_row.append('RESULT')
    rows.append(type_row)

    title_row = []
    title_row.append('DATAID')
    title_row.append('ASSIGNMENT')
    for string in DataFrame.string_names:
        title_row.append(string)
    for group in DataFrame.group_names:
        title_row.append(group)
    for target in DataFrame.target_names:
        title_row.append(target)
    for result in range(len(results)):
        title_row.append(result)
    rows.append(title_row)

    if len(results[0]) == len(DataFrame.learn_set):
        dset = 'learn'
    elif len(results[0]) == len(DataFrame.valid_set):
        dset = 'valid'
    elif len(results[0]) == len(DataFrame.test_set):
        dset = 'test'
    elif len(results[0]) == (
        len(DataFrame.learn_set) + len(DataFrame.valid_set)
    ):
        dset = 'train'
    else:
        dset = None

    if dset == 'train':
        output_points = []
        for point in DataFrame.learn_set:
            output_points.append(point)
        for point in DataFrame.valid_set:
            output_points.append(point)
    elif dset == 'learn':
        output_points = DataFrame.learn_set
    elif dset == 'valid':
        output_points = DataFrame.valid_set
    elif dset == 'test':
        output_points = DataFrame.test_set
    else:
        output_points = []
        for point in DataFrame.learn_set:
            output_points.append(point)
        for point in DataFrame.valid_set:
            output_points.append(point)
        for point in DataFrame.test_set:
            output_points.append(point)

    for idx, point in enumerate(output_points):
        data_row = []
        data_row.append(point.id)
        data_row.append(point.assignment)
        for string in point.strings:
            data_row.append(string)
        for group in point.groups:
            data_row.append(group)
        for target in point.targets:
            data_row.append(target)
        for result in results:
            if DataFrame.num_targets == 1:
                data_row.append(result[idx][0])
            else:
                data_row.append(result[idx])
        rows.append(data_row)

    with open(filename, 'w') as file:
        wr = writer(file, quoting=QUOTE_ALL, lineterminator='\n')
        for row in rows:
            wr.writerow(row)

# -*- coding: utf-8 -*-
"""
Created on Feb. 14th 2018
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from builtins import open, bytes, str

__author__ = "yuhao"

import json


class ThreePoints(object):
    """
    inline, crossline and z coordinates of three points in survey
    """
    def __init__(self, json_file=None):
        self.json_file = None
        self.dict_survey = None
        self.startInline = None
        self.endInline = None
        self.stepInline = None
        self.startCrline = None
        self.endCrline = None
        self.stepCrline = None
        self.startDepth = None
        self.endDepth = None
        self.stepDepth = None
        self.zType = None
        self.inline_A = None
        self.crline_A = None
        self.east_A = None
        self.north_A = None
        self.inline_B = None
        self.crline_B = None
        self.east_B = None
        self.north_B = None
        self.inline_C = None
        self.crline_C = None
        self.east_C = None
        self.north_C = None
        if json_file is not None:
            if isinstance(json_file, (bytes, str)):
                self.json_file = json_file
                self._read_json()
            elif isinstance(json_file, dict):
                self.dict_survey = json_file
            self._parse_survey_setting()
        else:
            raise Exception("json_file is None")

    def _read_json(self):
        try:
            with open(self.json_file, 'r') as fl:
                self.dict_survey = json.load(fl)
        except ValueError as e:
            print(e.message)

    def _parse_survey_setting(self):
        try:
            self._parse_survey_setting_v1()
        except Not_threepoints_v1_Exception:
            try:
                self._parse_survey_setting_v2()
            except Not_threepoints_v2_Exception:
                print("cannot parse file")
                raise Invalid_threepoints_Exception

    def _parse_survey_setting_v1(self):
        # with open(json_file, 'r') as file:
        #     dict_survey = json.load(file)
        try:
            coordinate = self.dict_survey["Coordinate"]
            self.inline_A, self.crline_A, self.east_A, self.north_A = \
                coordinate[0]
            self.inline_B, self.crline_B, self.east_B, self.north_B = \
                coordinate[1]
            self.inline_C, self.crline_C, self.east_C, self.north_C = \
                coordinate[2]
            inline_range = self.dict_survey["inline"]
            self.startInline, self.endInline, self.stepInline = inline_range
            crline_range = self.dict_survey["crline"]
            self.startCrline, self.endCrline, self.stepCrline = crline_range
            z_range = self.dict_survey["depth"]
            self.startDepth, self.endDepth, self.stepDepth = z_range
        except KeyError:
            raise Not_threepoints_v1_Exception
            # print(e.message)


    def _parse_survey_setting_v2(self):
        # with open(json_file, 'r') as file:
        #     dict_survey = json.load(file)
        try:
            self.startInline, self.endInline, self.stepInline = \
                self.dict_survey["inline_range"]
            self.startCrline, self.endCrline, self.stepCrline = \
                self.dict_survey["crline_range"]
            self.startDepth, self.endDepth, self.stepDepth, self.zType = \
                self.dict_survey["z_range"]
            # self.zType = self.dict_survey["z_range"][2]
            self.inline_A, self.crline_A, self.east_A, self.north_A = \
                self.dict_survey["point_A"]
            self.inline_B, self.crline_B, self.east_B, self.north_B = \
                self.dict_survey["point_B"]
            self.inline_C, self.crline_C, self.east_C, self.north_C = \
                self.dict_survey["point_C"]
        except KeyError:
            # print(e.message)
            raise Not_threepoints_v2_Exception

class Not_threepoints_v1_Exception(Exception):
    def __init__(self, message=None):
        self.message = message
        self.message = "Not three points V1 file"
        super(Not_threepoints_v1_Exception, self).__init__(self.message)


class Not_threepoints_v2_Exception(Exception):
    def __init__(self, message=None):
        self.message = message
        self.message = "Not three points V2 file"
        super(Not_threepoints_v2_Exception, self).__init__(self.message)


class Invalid_threepoints_Exception(Exception):
    def __init__(self, message=None):
        self.message = message
        self.message = "Not valid three points file"
        super(Invalid_threepoints_Exception, self).__init__(self.message)

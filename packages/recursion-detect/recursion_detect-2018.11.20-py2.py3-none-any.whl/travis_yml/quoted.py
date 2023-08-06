#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString


def single(value):
    return SingleQuotedScalarString(value)


def double(value):
    return DoubleQuotedScalarString(value)

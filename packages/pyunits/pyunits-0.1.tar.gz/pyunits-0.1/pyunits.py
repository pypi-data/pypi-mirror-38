#!/usr/bin/env python
# coding: utf8

'''
Byte change to special Unit
'''

from enum import Enum
import re

class Values():
    values = {'B': 1}

    @staticmethod
    def getValues():
        if len(Values.values) <= 1:
            kbunits = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB' ]
            kibunits = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
            for index, unit in enumerate(kibunits):
                Values.values[unit] = 1 << (index + 1) * 10
            for index, unit in enumerate(kbunits):
                Values.values[unit] = 10 ** ((index + 1) * 3)
        return Values.values

    @staticmethod
    def get(key):
        return Values.getValues().get(key)


class Units(Enum):

    def __new__(self, name):
        obj = object.__new__(self)
        obj._value_ = Values.get(name)
        return obj

    B = ('B')
    K = ('K')
    KB = ('KB')
    KiB = ('KiB')
    M = ('M')
    MB = ('MB')
    MiB = ('MiB')
    G = ('G')
    GB = ('GB')
    GiB = ('GiB')
    T = ('T')
    TB = ('TB')
    TiB = ('TiB')
    P = ('P')
    PB = ('PB')
    PiB = ('PiB')
    E = ('E')
    EB = ('EB')
    EiB = ('EiB')
    Z = ('Z')
    ZB = ('ZB')
    ZiB = ('ZiB')
    Y = ('Y')
    YB = ('YB')
    YiB = ('YiB')


class ByteUnitConversionUtil():
    __defaultformat = "%.5f"

    @staticmethod
    def convert(value, unit=Units.B, format=__defaultformat):
        ret, value = ByteUnitConversionUtil.isNumber(value)
        if ret:
            if (unit == Units.B):
                return str(value).split(".", 2)[0] + unit.name
            else:
                return (format % (value / unit.value)) + unit.name
        else:
            num, units = ByteUnitConversionUtil.splitNumUnit(value)
            if num:
                value = num * Values.get(units)
                if (unit == Units.B):
                    return str(value).split(".", 2)[0] + unit.name
                else:
                    return (format % (value / unit.value)) + unit.name
            else:
                print(units)

    @staticmethod
    def isNumber(value):
        '''
        jduge input is Number
        :param value: input param
        :return: True/False, value
        '''
        # int and float, such as 1 and 1.23
        if isinstance(value, int) or isinstance(value, float):
            return True, float(value)
        # such as "1234"
        elif value.isdigit():
            return True, float(value)
        # such as "123.4"
        elif value.replace(".", "").isdigit():
            return True, float(value)
        # such as "123KB", "123.4KB", "abc"
        else:
            return False, value

    @staticmethod
    def splitNumUnit(value):
        '''
        split input param to number and unit
        :param value: input param
        :return: number, unit
        '''

        # process with single "B"
        if value.rstrip("B").isdigit():
            return float(value.rstrip("B")), "B"
        elif value.rstrip("B").replace(".", "").isdigit():
            return float(value.rstrip("B")), "B"

        #
        re_str = "[KMGTPEZY]i?B?"
        re_com = re.compile(re_str)
        re_ret = re.search(re_com, value)

        # whether input is legal
        if not re_ret:
            return None, "Illegal String"
        value_unit = re_ret.group()
        value_num = value.strip(value_unit)
        return float(value_num), value_unit[0].upper() + "B"


if __name__ == "__main__":
    print(ByteUnitConversionUtil.convert("1000000000", Units.GB))
    print(ByteUnitConversionUtil.convert("1000000000.1234", Units.GiB))
    print(ByteUnitConversionUtil.convert("1000000000B", Units.GiB))
    print(ByteUnitConversionUtil.convert("1000000000.1234B", Units.GiB))
    print(ByteUnitConversionUtil.convert("1000000000KB", Units.GiB))
    print(ByteUnitConversionUtil.convert("1000000000KiB", Units.GiB))
    print(ByteUnitConversionUtil.convert("1000000000.1234KB", Units.GiB))
    print(ByteUnitConversionUtil.convert("1003.1234TiB", Units.GiB, "%.5f"))
    print(ByteUnitConversionUtil.convert("1003.1234T", Units.GiB, "%.5f"))
    print(ByteUnitConversionUtil.convert(1000000000, Units.GB, "%.5f"))
    print(ByteUnitConversionUtil.convert(1000000000.234, Units.GiB, "%.5f"))

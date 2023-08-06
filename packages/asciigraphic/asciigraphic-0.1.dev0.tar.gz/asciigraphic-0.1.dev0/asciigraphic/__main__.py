#!/usr/bin/env python

######################################################################
# @author      : nevernew (nevernew@orca)
# @file        : __main__
# @created     : Пятница ноя 16, 2018 22:01:56 MSK
#
# @description : 
######################################################################


import asciichartpy

def main():
    list = [12,12,22,12,8,4,14]
    print(asciichartpy.plot(list))

if __name__ == "__main__":
    main()


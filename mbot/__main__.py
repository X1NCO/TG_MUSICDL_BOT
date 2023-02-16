# Copyright (C) 2023 DX_MODS
#Licensed under the  AGPL-3.0 License;
#you may not use this file except in compliance with the License.
#Author ZIYAN
from mbot import Mbot
from os import sys,mkdir,path

if __name__ == "__main__":
    if not path.exists("cache"):
        mkdir("cache")
    Mbot().run()

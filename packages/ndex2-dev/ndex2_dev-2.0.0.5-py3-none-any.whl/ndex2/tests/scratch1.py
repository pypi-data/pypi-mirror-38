
__author__ = 'aarongary'

import unittest

import json
import pandas as pd
import csv
import networkx as nx
import ndex2
import ndex2.client as nc
import os
from ndex2.nice_cx_network import NiceCXNetwork
from ndex2.client import DecimalEncoder
from ndex2cx.nice_cx_builder import NiceCXBuilder
import numpy as np

upload_server = 'dev.ndexbio.org'
upload_username = 'scratch'
upload_password = 'scratch'

path_this = os.path.dirname(os.path.abspath(__file__))

class TestScratch1(unittest.TestCase):
    @unittest.skip("Temporary skipping")
    def test_scratch1(self):
        print('Testing: SIMPLE3.txt with DictReader')
        path_to_network = os.path.join(path_this, 'SIMPLE3.txt')

        return_json = {}
        with open(path_to_network, 'r') as tsvfile:
            reader = csv.DictReader(filter(lambda row: row[0] != '#', tsvfile), dialect='excel-tab', fieldnames=['a', 'b', 'c'])
            counter = 0
            for row in reader:
                return_json[counter] = [row.get('a'), row.get('b'), row.get('c')]
                counter += 1

        pd1 = pd.DataFrame.from_dict(return_json, orient='index')

        print(pd1.head(20))

        print(len(return_json))

    #@unittest.skip("Temporary skipping")
    def test_scratch2(self):
        path_to_big_file = '/Users/aarongary/Projects/hiview_cx/hiview_cached_networks/cytoscape_js_files/ce01e381-6e96-11e8-9d1c-0660b7976219.cx'

        nice_cx = ndex2.create_nice_cx_from_file(path_to_big_file)

        nice_cx.print_summary()



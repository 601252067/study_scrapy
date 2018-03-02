# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

class Com289Pipeline(object):


    def process_item(self, item, spider):
        base_dir = os.getcwd()
        file_name = base_dir + '/偷拍自拍.txt'


        with open(file_name, 'a') as f:
            f.write(str(item['link']) + '\n')
        return item




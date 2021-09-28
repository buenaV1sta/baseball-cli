# -*- coding: utf-8 -*-
import os
from baseball.utils import NpbConst
from scrapy.exporters import JsonItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class NpbPipeline:
    file = None

    def open_spider(self, spider):
        os.makedirs(NpbConst.NPB_CLI_HOME, exist_ok=True)
        self.file = open(NpbConst.OUTPUT_JSON_FILE_PATH, 'wb')
        self.exporter = JsonItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

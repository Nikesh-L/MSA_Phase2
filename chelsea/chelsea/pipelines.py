# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class ChelseaPipeline:
#     def process_item(self, item, spider):
#         return item
from scrapy.exporters import CsvItemExporter
from scrapy import signals

def item_type(item):
    return type(item).__name__.replace('Item','').lower()

class MultiCSVItemPipeline(object):
    SaveTypes = ['post','comment']

    def open_spider(self, spider):
        self.files = dict([ (name, open(name+'.csv','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = type(item).__name__
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
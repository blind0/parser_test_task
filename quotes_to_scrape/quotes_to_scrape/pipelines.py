# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class QuotesToJsonPipeline:
    def open_spider(self, spider):
        self.file = open("output.json","w")
        self.data = {}
        self.data['authors']={}

    def close_spider(self, spider):
        json.dump(self.data, self.file, ensure_ascii=True, indent=4)    
        self.file.close()

    def process_item(self, item, spider):
        if item['author'] not in self.data['authors']:
            self.data['authors'][item['author']] = {
                "quotes":[]
            } 
        
        self.data['authors'][item['author']]['quotes'].append(
            {
                "quote":item['text'],
                'tags':item['tags']
            }
        )

        return item
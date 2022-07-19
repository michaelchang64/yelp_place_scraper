import os
import json

from itemadapter import ItemAdapter
from datetime import datetime

class WriteJsonPipeline:

    def open_spider(self, spider):
        self.dirname = '_output'
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
        now = datetime.now()
        now_str = now.strftime("%Y_%m_%d")
        self.filename = '{}/{}.jsonl'.format(self.dirname, now_str)
        self.file = open(self.filename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
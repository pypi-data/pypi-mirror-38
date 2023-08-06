from pdb import set_trace
from ia import Audio, Item
import datetime

ten_minutes_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

for i in Item.recent(collection="tednelsonjunkmail"):
    print i.identifier, i.metadata['title']

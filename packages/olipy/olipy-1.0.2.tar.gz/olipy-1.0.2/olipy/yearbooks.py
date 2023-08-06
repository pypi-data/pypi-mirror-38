from pdb import set_trace
import json
import random
by_year = json.load(open("yearbooks_by_year.json"))
def choose():
    year = int(random.gauss(1980, 20))
    for_year = by_year.get(str(year))
    if not for_year:
        return None
    return random.choice(for_year)

choice = None
while not choice:
    choice = choose()

from ia import Text
item = Text(choice)
pages = item.pages or 200
page = random.randint(0, pages-1)
print item.image_url(page)

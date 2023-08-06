from datetime import datetime, timedelta

from mochart import melon, mnet, naver, gaon, oricon


def print_first_five(ranks):
    ranks = list(ranks)
    for rank in ranks[:5]:
        print(rank)


provider = melon

# print(" - - - - - NOW")
# ranks = provider.peek()
# print_first_five(ranks)

print(" - - - - - NOW")
ranks = provider.realtime()
# print_first_five(ranks)
from pprint import pprint
pprint(ranks)

import json
with open("melon_realtime.json", "w", encoding="utf8") as f:
    f.write(json.dumps(ranks, ensure_ascii=False))

# print(" - - - - - 2 hours ago")
# four_hours_ago = datetime.now() - timedelta(hours=2)
# ranks = provider.trend(four_hours_ago)
# print_first_five(ranks)

# print(" - - - - - 4 hours ago")
# four_hours_ago = datetime.now() - timedelta(hours=4)
# ranks = provider.realtime(four_hours_ago)
# print_first_five(ranks)

# print(" - - - - - today")
# ranks = provider.day(datetime.now())
# print_first_five(ranks)


# print(" - - - - - weekly today")
# week_ago = datetime.now()
# ranks = provider.week()
# print_first_five(ranks)

# print(" - - - - - 1 week ago")
# week_ago = datetime.now() - timedelta(days=7)
# ranks = provider.week(week_ago)
# print_first_five(ranks)

# print(" - - - - - 2 week ago")
# two_weeks_ago = datetime.now() - timedelta(days=14)
# ranks = provider.week(two_weeks_ago)
# print_first_five(ranks)

# print(" - - - - - 1 month ago")
# month_ago = datetime.now() - timedelta(days=31)
# ranks = provider.month(month_ago)
# print_first_five(ranks)

# print(" - - - - - 5 month ago")
# month_ago = datetime.now() - timedelta(days=30*5)
# ranks = provider.month(month_ago)
# print_first_five(ranks)

# print(" - - - - - 1 year ago")
# year_ago = datetime.now() - timedelta(days=365)
# ranks = provider.year(year_ago)
# print_first_five(ranks)

# print(" - - - - - 5 year ago")
# year_ago = datetime.now() - timedelta(days=365*5)
# ranks = provider.year(year_ago)
# print_first_five(ranks)

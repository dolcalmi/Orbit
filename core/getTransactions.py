from re import findall
from core.utils import pageLimit
from core.requester import requester

def getTransactions(address, processed, database, limit):
    addresses = []
    increment = 0
    database[address] = {}
    pages = pageLimit(limit)
    for i in range(pages):
        if pages > 1 and increment != 0:
            trail = '?offset=%i' % increment
        # print ('address %s\n' % address)
        response = requester(address)
        # print ('data after %s\n\n\n' % response)
        matches = findall(r'"address": ".*?"', response)
        # print ('matches %s\n\n\n' % matches)
        for match in matches:
            found = match.split('"')[3]
            if found not in database[address]:
                database[address][found] = 0
            database[address][found] += 1
            addresses.append(found)
        increment += 50
        processed.add(address)
    return addresses

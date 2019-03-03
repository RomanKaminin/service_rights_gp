import datetime


class Entry:
    def __init__(self, db, **kwargs):
        self.collection = db['apps']

    async def save(self, data, **kw):
        result = await self.collection.insert(
            {'id': data['id'],
             'app_data': data['app_data'],
             'time': datetime.datetime.utcnow()
             }
        )
        return result

    async def get_messages(self, entry_id):
        entry = self.collection.find().sort([('id', entry_id)])
        return await entry.to_list(length=None)


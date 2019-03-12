from pymongo import MongoClient
#'database_pipeline'

class MongoDB():
    def __init__(self,dbname):
        self.client = MongoClient()
        self.db = self.client[dbname]

    def get_collection_name(self):
        #Return all collection names
        return self.db.list_collection_names()

    def find(self, collection, _id=False, last=False):
        #by default the function doesn't select the _id field
        #retourne une list de dictionaire last=False
        #retourne un dictionaire si last=True
        if _id == False:
            cursor = self.db[collection].find({}, {'_id': False})
        else:
            cursor = self.db[collection].find()

        if last == True:
            cursor = cursor.sort([("Time", -1)]).limit(1)
            return cursor[0]

        return self.cursor_to_dict(cursor)

    def find_all(self, _id=False, last=False):
        d = dict()
        for coll in self.get_collection_name():
            d[coll] = self.find(coll, _id, last)
        return d

    def cursor_to_dict(self, cursor):
        l = list()
        for i in cursor:
            l.append(i)
        return l

    def get_keys(self, collection):
        #Return all field name of a collection
        map = Code("function() { for (var key in this) { emit(key, null); } }")
        reduce = Code("function(key, stuff) { return null; }")
        result = self.db[collection].map_reduce(map, reduce, "myresults")
        return result.distinct('_id')

#docs = list(self.db[collec_pipe_name].find().sort([('Time', -1)]))

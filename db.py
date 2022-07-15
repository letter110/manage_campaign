import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://test:HHmm123456@cluster0.sheu0ff.mongodb.net/?retryWrites=true&w=majority")
db = client['mydb']
campaigns = db['campaigns']
running_campaigns = db['running_campaigns']

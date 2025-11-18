from pymongo import MongoClient

# connection to mongodb instance
client = MongoClient("mongodb://localhost:27017")

# creating or choosing the database
db = client["book_library"]

# choosing the collection

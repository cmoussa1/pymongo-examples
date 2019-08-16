import pymongo

# mongod --dmongod --dbpath /Users/moussa1/data/db/
# the above command will start the MongoDB daemon
# that points to a database directory to write to 

# to create a DB in MongoDB, we create a MongoClient object,
# specify a connection URL with an IP address and the name of 
# the database we want to create. Mongo DB will create the 
# DB if it does not exist, and make a connection to it.
myclient = pymongo.MongoClient("mongodb://localhost:27017/")


# the following line will make a database called "baseball."
# the database will not officially be "created" until it gets
# content
mydb = myclient["baseball"]
print("== LIST OF DATABASES ==")
print("(the 'baseball' database will not appear until we put a collection in it)")
print(myclient.list_database_names(), "\n")


# we then create a collection, using the database object and
# specifying the name of the collection we want to create.
# the following line will create a collection called "giants"
mycol = mydb["giants"]
print("== LIST OF COLLECTIONS ==")
print("(should be empty because there are no records in it yet)")
print(mydb.list_collection_names(),"\n\n")


# to insert a document in MongoDB into a collection, we use the 
# insert_one() method. the first parameter of this method is a 
# dictionary containing the name(s) and value(s) of each field
# in the document we want to insert
print("== CREATING A RECORD ==")
mydict = {
	"number" : 28,
	"name" : "Buster Posey",
	"position" : "catcher"
}
# insert_one() returns an InsertOneResult object, which has a 
# property, inserted_id, that holds the id of the inserted 
# document
record = mycol.insert_one(mydict)
print("Buster Posey ID:", record.inserted_id,"\n\n")


# let's check the databases and collections now...
print("== LIST OF DATABASES (UPDATED) ==")
print(myclient.list_database_names(),"\n")
print("== LIST OF COLLECTIONS (UPDATED) ==")
print(mydb.list_collection_names(),"\n\n")


# we can insert multiple documents into a collection using the
# insert_many() method, a list containing dictionaries with the 
# data we want to insert, with an optional id that we can specify
print("== CREATING MANY RECORDS ==")
print("(will return a list of object ID's)\n")
giants_players = [
	{"number" : 9, "name" : "Brandon Belt", "position" : "first baseman"},
	{"number" : 14, "name" : "Scooter Gennett", "position" : "second baseman"},
	{"number" : 10, "name" : "Evan Longoria", "position" : "third baseman"},
	{"number" : 35, "name" : "Brandon Crawford", "position" : "shortstop"},
	{"number" : 5, "name" : "Mike Yastrzemski", "position" : "outfielder"},
	{"number" : 1, "name" : "Kevin Pillar", "position" : "outfielder"},
	{"number" : 53, "name" : "Austin Slater", "position" : "outfielder"},
	{"number" : 40, "name" : "Madison Bumgarner", "position" : "pitcher"}
]
record = mycol.insert_many(giants_players)
print(record.inserted_ids,"\n\n")

print("*" * 19)
print("NEW LIST OF PLAYERS")
print("*" * 19)
for player in mycol.find():
	print(player)
print("\n\n")


# to update a record, we can use the update_one() method, where
# the first parameter is a query object defining which document
# to update
print("== UPDATING A RECORD ==")
print("(changing Austin Slater's spot to Steven Duggar's)\n")
myquery = {"number" : 53, "name" : "Austin Slater", "position" : "outfielder"}
newvalues = { "$set": {"number" : 6, "name" : "Steven Duggar", "position" : "outfielder"} }
mycol.update_one(myquery, newvalues)
print("*" * 23)
print("UPDATED LIST OF PLAYERS")
print("*" * 23)
for player in mycol.find():
	print(player)
print("\n\n")


# to select data from a collection in MongoDB, we can use the 
# find_one() method, which returns the first occurence in the 
# selection.
record = mycol.find_one()
print("== FINDING OBJECT ID OF FIRST RECORD ==")
print(record,"\n\n\n")


# the second parameter of the find() method is an object describing
# which fields to include in the result
print("== QUERYING A COLLECTION ==")
print("(finding all outfielders in the collection)\n")
myquery = {"position" : "outfielder"}
mydoc = mycol.find(myquery)
for x in mydoc:
	print(x)
print("\n\n")


# we can use sort() to sort the result in ascending or descending order.
# it takes one parameter for "fieldname" and one parameter for 
# "direction"
print("== SORTING A COLLECTION ==")
print("(will go in descending order by name)\n")
print("*" * 22)
print("SORTED LIST OF PLAYERS")
print("*" * 22)
mydoc = mycol.find().sort("name", -1)
for x in mydoc:
	print(x)
print("\n\n")


# to delete a document, we can use the delete_one() method, where 
# the first parameter is a query object defining which document
# to delete
print("== DELETING A RECORD ==")
print("(will delete Buster Posey from collection)\n")
myquery = {"name" : "Buster Posey"}
mycol.delete_one(myquery)
print("*" * 23)
print("UPDATED LIST OF PLAYERS")
print("*" * 23)
for player in mycol.find():
	print(player)
print("\n\n")


# we can pass in an empty query object to the delete_many() method to delete
# all documents in a collection
print("== DELETING ALL RECORDS IN A COLLECTION ==")
x = mycol.delete_many({})
print(x.deleted_count, "document(s) deleted.")
print("\n")
# we can delete a collection by using the drop() method
print("== DROPPING A COLLECTION ==")
print("(the 'giants' collection should not appear under here)")
mycol.drop()
print(mydb.list_collection_names()) # should be empty this time around
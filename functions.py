import os
import ast
import pickle
from pymongo import MongoClient
cluster="mongodb://192.168.29.178/?directConnection=true"
client=MongoClient(cluster)
db=client.Users
profs=db.names
lists=db.listings
resources=["wood", "steel", "plants", "metal", "plastic"]
materials={"steel":["type1","type2","type3"], "plants":["cotton","wool","silk","bamboo","tomato","onion"],"metal":["iron", "tungsten","copper"], "wood":["wood"],"plastic":["plastic"]}
def signUp(user, passwd):
    j=profs.find_one({f"{user}": {'$exists': True}})
    if j==None:
        c={"_id":f"{user}",f"{user}":passwd,
           "wood":50,
           "steel":{"type1":0, "type2":0, "type3":0},
           "plants":{"cotton":0, "wool":0, "silk":0, "bamboo":0, "tomato":0, "onion":0},
           "metal":{"iron":0, "tungsten":0, "copper":0},
           "plastic":0,
           "money":10000,
           "group":"None"}
        profs.insert_one(c)
        return "Done!"
    else:
        return "User exists!"

def listListings(typeOfMaterial,material):
    material.lower()
    allLists=lists.find_one({"_id":"lists"})
    finalList=allLists[material][typeOfMaterial]
    print(finalList)
    return finalList

def showInv(user):
    if profs.find_one({user: {'$exists': True}})!=None:
        l=profs.find_one({"_id":user},{"_id":0, user:0})
        return l
def passChange(user,oldPasswd,newPasswd):
    r=profs.find_one({user: {'$exists': True}})
    if r!=None:
        if profs.find_one({user:oldPasswd}):
            profs.update_one({user:oldPasswd},{"$set":{user: newPasswd}})
            return "password changed"
        else:
            return "wrong current password"
    else:
        return "no user"

def login(user, passwd):
    f=profs.find_one({user: {'$exists': True}})
    if f==None:
        return "User not found!"
    else:
        if profs.distinct(user)==[passwd]:
            print(profs.distinct(user))
            print(type(profs.distinct(user)))
            return "correct!"
        else:
            print(profs.distinct(user))
            print(type(profs.distinct(user)))
            return "incorrect!"

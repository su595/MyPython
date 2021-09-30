
from os import name, path
import yaml


class Bike():

    def __init__(self, name, macAddress, isClamied, claimedBy, inWifi, size, needsRepair):
        self.macAddress = macAddress
        self.name = name
        self.isClamed = isClamied
        self.claimedBy = claimedBy
        self.inWifi = inWifi
        self.size = size
        self.needsRepair = needsRepair

        


class BikeManager():

    def __init__(self) -> None:
        self.ymlPath = input("path pls ")
        self.bikeList = self.parseBikeList(self.ymlPath) # a list of all bikes
        
    
    def parseBikeList(self, path):
        bikeDict = yaml.safe_load(open(path, "r"))
        
        tempList = []

        for bike in bikeDict:
            tempList.append(Bike( bike["name"], bike["macAddress"], bike["isClaimed"], bike["claimedBy"], bike["inWifi"], bike["size"], bike["needsRepair"]  ))
        
        return tempList

    def updateYmlList(self, path):
        bikeDict = {}
        for i in range(len(self.bikeList)):
            bike = self.bikeList[i]

            bikeDict[str(i)] = {}
            bikeDict[str(i)]["name"] = bike.name
            bikeDict[str(i)]["macAddress"] = bike.macAddress
            bikeDict[str(i)]["isClaimed"] = bike.isClaimed
            bikeDict[str(i)]["claimedBy"] = bike.claimedBy
            bikeDict[str(i)]["inWifi"] = bike.inWifi
            bikeDict[str(i)]["size"] = bike.Size

        print(bikeDict)

        yaml.dump(bikeDict, open(path, "w"))    

    def checkIfBikesInWifi(self, macAddresses): # updates the .inWifi variable of every bike
        for bike in self.bikeList:
            if bike.macAdress in macAddresses:
                bike.inWifi = True
            else:
                bike.inWifi = False

    def getMacAddressesOnNetwork(self): # returns a list of mac addresses on the network
        
        return # a list of mac addresses

    def claimBike(self):
        pass

    def filterBikes(self, name=None, size=None): # returns a list of bikes with the selected properties
        filteredBikes = []
        for bike in self.bikeList:
            # if the bike needs repair, discard it
            if bike.needsRepair:
                break

            # if no specific name/size was given or if the name/size matches the bike, append to filtered list
            if name is None or name == bike.name:
                filteredBikes.append(bike)
                break # this prevents one bike from being appended twice
            
            if size is None or size == bike.size:
                filteredBikes.append(bike)
                break
        
        return filteredBikes
            




from networktables import NetworkTables
from enum import Enum

alliances = Enum("alliances", "Blue Red Unknown")

class DriverStation(object):
	def __init__(self):
		NetworkTables.initialize()
		self.fms = NetworkTables.getTable("FMSInfo")
	
	def getAlliance(self):
		fms_alliance_red = self.fms.getBoolean("IsRedAlliance", True)
		
		if fms_alliance_red:
			return alliances.Red
		else:
			return alliances.Blue
	
	def getStation(self):
		return int(self.fms.getEntry("StationNumber", 1))
	
	def getMatchType(self):
		return int(self.fms.getEntry("MatchType", 0))
	
	def getFMSControlData(self):
		return self.fms.getEntry("FMSControlData")
	
	def getReplayNumber(self):
		return int(self.fms.getEntry("ReplayNumber"))
		
	def getMatchNumber(self):
		return int(self.fms.getEntry("MatchNumber"))
	
	def getEventName(self):
		return str(self.fms.getEntry("EventName"))
	
	def getGSM(self):
		return str(self.fms.getEntry("GameSpecificMessage")).upper()
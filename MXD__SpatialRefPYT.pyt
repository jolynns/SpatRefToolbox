#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jolynn
#
# Created:     03/12/2016
# Copyright:   (c) jolynn 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.overwriteOutput = True


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

	# First Param chooses what is to be done
	param0 = arcpy.Parameter(
        	displayName="Choose Function",
        	name="myFunction",
        	datatype="GPString",
        	parameterType="Required",
        	direction="Input")
	param0.filter.type = "VAlueList"
	param0.filter.list = ["SetDataFrame", "SetLayers"]

	# Second Param chooses a file or directory to work on
	param1 = arcpy.Parameter(
        	displayName="Input MXD or Directory",
        	name="myFiles",
        	datatype=["DEMapDocument", "DEFolder"],
        	parameterType="Required",
        	direction="Input")

	# Third Param chooses the spacial reference to convert to
	param2 = arcpy.Parameter(
        	displayName="Spatial Reference",
        	name="mySpatialRef",
        	datatype="GPSpatialReference",
        	parameterType="Required",
        	direction="Input")

        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, params, messages):
        """The source code of the tool."""
##        return

    import sys

# define the variables colledec as user input from the toolbox
##    myMXD = "C:\\Users\\jolynn\\Documents\\GIS\\GEOG_485\\Lesson2\\Test.mxd"
##    myDir = "C:\\Users\\jolynn\\Documents\\GIS\\GEOG_485\\Lesson2\\"
##    myTask = "SetLayers"
##    targetSR = "32149"
    myTask = params[0].valueAsText
    myMXD = params[1].valueAsText
    rawSR = arcpy.Describe(params[2])
    targetSR = desc.spatialReference.factoryCode

# test to see if spatial reference matches
    def testSR(targetSRF, targetSR):
        try:
            desc = arcpy.Describe(targetSRF)
            spatialRef = desc.spatialReference.factoryCode
            if str(spatialRef) == str(targetSR):
                return True
            else:
                return False
        except:
            arcpy.AddError("Unable to get Spatial Reference: skipping")
            arcpy.AddMessage(arcpy.GetMessages())

# add the _projected to a file name
    def renameFile(fullName):
        try:
            import os.path
            fName, extension = os.path.splitext(fullName)
            return fName + "_projected" + extension
        except:
            arcpy.AddError("Unable to rename file %s" % fullName)
            arcpy.AddMessage(arcpy.GetMessages())

# Conver the Spatial ref of a feature class and give it a new name
    def convertSR(featureClass, outputFC, targetSR):
        try:
            arcpy.Project_management(featureClass, outputFC, targetSR)
        except:
            arcpy.AddError("Unable to convert Spatial Reference for %s" % featureClass)
            arcpy.AddMessage(arcpy.GetMessages())
        else:
            pass

# Open the MXD file and updates spatial ref of the first dataframe
    def setDataFrameSR(MXD, spatialRef):
        try:
            workingMXD = arcpy.mapping.MapDocument(MXD)
            dataFrame = arcpy.mapping.ListDataFrames(workingMXD)[0]
            sr = arcpy.SpatialReference(int(spatialRef))
            dataFrame.spatialReference = sr
            workingMXD.save()
            del workingMXD
        except:
            arcpy.AddError("Unable to set dataframe spatial reference from %s" % MXD)
            arcpy.AddMessage(arcpy.GetMessages())

# Get the list of MX files to work on, it may be a list of one.
    mxd_list = []
    desc = arcpy.Describe(myMXD)
    fileType = desc.dataType
    if fileType == "MapDocument":
        mxd_list.append(myMXD)
    elif fileType == "Folder":
        listMXD = arcpy.ListFiles("*.mxd")
        for mxdFile in listMXD:
            mxd = arcpy.mapping.MapDocument(mxdFile)
            mxd_list.append(mxd.filePath)

#set the spatial reference for each layer and update the MXD with the new feature class
    if myTask == "SetLayers":
        for currentMXD in mxd_list:
            # define our current working MXD file
            workingMXD = arcpy.mapping.MapDocument(currentMXD)

            # Start working on each layer of the MXD file
            for layer in arcpy.mapping.ListLayers(workingMXD):
                # Get variables to use later for each layer
                wsPath = layer.workspacePath
                featureClass = layer.dataSource
                outputFC = renameFile(featureClass)
                layerName = layer.name
                outputLN = renameFile(layerName)

                # Test to see if the feature class has the target spatial reference
                if testSR(featureClass, targetSR):
                    pass
                else:
                    # Conver the Spatial reference
                    convertSR(featureClass, outputFC, targetSR)
                    # update the layer source to new feature class
                    layer.replaceDataSource(str(wsPath), 'SHAPEFILE_WORKSPACE', outputLN)

            # save changes to the MXD file
            workingMXD.save()
# set the spatial reference for the dataframe
    elif myTask == "SetDataFrame":
        for currentMXD in mxd_list:
            setDataFrameSR(currentMXD, targetSR)






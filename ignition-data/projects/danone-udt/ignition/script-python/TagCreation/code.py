def GetDeviceName(file_string):
    file_list = CSV.parse_csv_into_list(file_string)
    system.perspective.print(file_list[0]["Ignition Device Name"])
    return file_list[0]["Ignition Device Name"]

def CreateTag(device_name, file_string):
    file_list = CSV.parse_csv_into_list(file_string)
    
    [system.perspective.print(row) for row in file_list]
    
    tag_path = "[default]"
    
    # parameters
    tagName = device_name
    tagProgramName = file_list[0]["Device Tag Path"]
    tagUDTName = "OEE"
    
    try:
        int(file_list[0]["Device Tag Path"])
        typeId = "AllenBradley Logix"
    except:
        typeId = "Modbus"

    tagType = "UdtInstance"
    
    tag = {
    	"name" : "Test",
        "typeId" : typeId,
    	"tagType" : tagType,
		"parameters" : {
    		"DeviceName" : tagName,
    		"ProgramName" : tagProgramName,
    		"UDTName" : tagUDTName
    	}
    }
    
    collisionPolicy = "o"
    
    result = system.tag.configure(tag_path, [tag], collisionPolicy)
    
    system.perspective.print(result)
    return
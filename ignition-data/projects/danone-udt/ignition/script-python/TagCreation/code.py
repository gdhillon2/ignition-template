"""
This script creates tags from two csv files. One file containing the equipment
to device mappings and the other containing the necessary information
"""
SITE = "NORAM"
AREA = "BOU"

tag_path = "%s/%s" % (SITE, AREA)

logger = system.util.getLogger("tag creation")

def get_mappings(file_string):
    file_list = CSV.parse_csv_into_list(file_string)
    return file_list

def create_tags(mappings, tag_file):
    tag_list = CSV.parse_csv_into_list(tag_file)
    tag_list_size = len(tag_list)

    line = "Line"
    equip = "Equipment Name"
    path = "Device Tag Path"
    name = "Ignition Device Name"

    # MODBUS params
    state = "State"
    infeed = "InfeedCount"
    outfeed = "OutfeedCount"

    # creates NORAM directory with a BOU directory inside of it
    folder_structure = {
        "tagType" : "Folder",
        "name" : SITE,
        "tags" : [
                    {
                        "name" : AREA,
                        "tagType" : "Folder",
                        "tags" : [{}]
                    }
        ]
    }

    system.tag.configure(basePath = "", tags = folder_structure, collisionPolicy = "a")
    # for each row in mappings,
    for row in mappings:
        logger.debug("%s" % row)
        line_folder = {
            "tagType" : "Folder",
            "name" : row[line],
            "tags" : []
        }

        equip_folder = {
            "tagType" : "Folder",
            "name" : row[equip],
            "tags" : []
        }
        line_folder["tags"].append(equip_folder)

        system.tag.configure(basePath = tag_path, tags = line_folder, collisionPolicy = "m")

        logger.debug("current row " + row[line] + " " + row[equip])
        t_ptr = 0
        # initialize DeviceName from row in mappings
        device_name = row[name]
        # find the correct row in tag_list that corresponds to the line
        while t_ptr < tag_list_size and row[line] != tag_list[t_ptr][line]:
            t_ptr += 1
        # keep going down rows until correct Equipment Name is found
        while t_ptr < tag_list_size and row[equip] != tag_list[t_ptr][equip]:
            t_ptr += 1
        # if there's a number in the tag path it is MODBUS
        try:
            int(tag_list[t_ptr][path])
            # initialize InfeedAddress, OutfeedAddress, StateAddress parameters
            infeed_address = ""
            outfeed_address = ""
            state_address = ""
            # keep going down rows as long as Equipment Name stays the same as mapping row
            while t_ptr < tag_list_size and row[equip] == tag_list[t_ptr][equip]:
                # if "" column is State, assign Device Tag Path to state param,
                # InfeedCount, OutfeedCount, etc.
                if tag_list[t_ptr][""] == state:
                    state_address = tag_list[t_ptr][path]
                elif tag_list[t_ptr][""] == infeed:
                    infeed_address = tag_list[t_ptr][path]
                elif tag_list[t_ptr][""] == outfeed:
                    outfeed_address = tag_list[t_ptr][path]
                t_ptr += 1
            logger.debug("device name " + device_name)
            logger.debug("state " + state_address)
            logger.debug("infeed " + infeed_address)
            logger.debug("outfeed " + outfeed_address)

            # create the tag
            plc_path = "%s/%s/%s" % (tag_path, row[line], row[equip])
            typeId = "Modbus"
            tagType = "UdtInstance"

            tag = {
                "name" : "PLC Data",
                "typeId" : typeId,
                "tagType" : tagType,
                "parameters" : {
                    "DeviceName" : device_name,
                    "InfeedAddress" : infeed_address,
                    "OutfeedAddress" : outfeed_address,
                    "StateAddress" : state_address
                }
            }

            system.tag.configure(plc_path, [tag], "o")
        # if there's not a string in the tag path it is AB
        except ValueError:
            # initialize ProgramName from DanPT_ + Equipment Name
            program_name = tag_list[t_ptr][path].split(".")[0]
            logger.debug("device name " + device_name)
            logger.debug("program name " + program_name)
            # create the tag
            plc_path = "%s/%s/%s" % (tag_path, row[line], row[equip])
            typeId = "AllenBradley Logix"
            tagType = "UdtInstance"

            tag = {
                "name" : "PLC Data",
                "typeId" : typeId,
                "tagType" : tagType,
                "parameters" : {
                    "DeviceName" : device_name,
                    "ProgramName" : program_name,
                }
            }

            system.tag.configure(plc_path, [tag], "o")
    return

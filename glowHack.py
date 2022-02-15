import pymem

#Game offsets
################################################
dwForceJump = (0x52789F8)
dwLocalPlayer = (0xDB35EC)
m_fFlags = (0x104)
dwEntityList = (0x4DCEB7C)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x5316E98)
m_iGlowIndex = (0x10488)
################################################
pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle,'client.dll').lpBaseOfDll

def execGlow():
    glow_manager = pm.read_int(client+dwGlowObjectManager)
    for i in range(1,32):
        entity = pm.read_int(client + dwEntityList + i*0x10)
        #Glow
        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)

            if entity_team_id == 2:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

            if entity_team_id == 3:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
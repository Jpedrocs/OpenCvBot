import pymem
import keyboard
import PySimpleGUI as sg
import csgo

sg.theme('Dark Blue 2')

layout = [[sg.Text('Choose the team you want to glow:')],
          [sg.Checkbox('CT', default = False, key = '-CT-')],
          [sg.Checkbox('TR', default = False, key = '-TR-')],
          [sg.Text('Press End to stop or restart the program to select another option')],
          [sg.Button('Start')],
          [sg.Exit()]]

window = sg.Window('GlowHack', layout)

#Game offsets
dwEntityList = csgo.dwEntityList
m_iTeamNum = csgo.m_iTeamNum
dwGlowObjectManager = csgo.dwGlowObjectManager
m_iGlowIndex = csgo.m_iGlowIndex

pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle,'client.dll').lpBaseOfDll

def execGlow(ct_on,tr_on):
    enabled = True
    while enabled:
        glow_manager = pm.read_int(client+dwGlowObjectManager)
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i*0x10)
            #Glow
            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if tr_on:
                    if entity_team_id == 2:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
                if ct_on:
                    if entity_team_id == 3:
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                        pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                        pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)
        if keyboard.is_pressed('End'):
            enabled = False


while True:
    event, values = window.read()

    if values['-CT-'] or values['-TR-']:
        if values['-CT-'] and values['-TR-']:
            execGlow(True,True)
        elif values['-CT-']:
            execGlow(True,False)
        else:
            execGlow(False,True)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
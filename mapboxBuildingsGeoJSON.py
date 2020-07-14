import PySimpleGUI as sg 

from convert2geo import logToGeojson

sg.theme('SystemDefault')

layout = [[sg.In('Select Log File'), sg.FileBrowse()],
          [sg.In('Select Save Location'), sg.FileSaveAs()],
          [sg.OK(), sg.Cancel()]]

window = sg.Window('Convert Mapbox Log to GeoJSON', layout)

event, values = window.Read()

window.Close()

fileOpen = values[0]
fileSave = values[1]

if event == 'OK':
    logToGeojson(fileOpen, fileSave)
    sg.Popup('Conversion Complete!')

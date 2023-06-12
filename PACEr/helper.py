# Lehmann Janneck 22.05.2023

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import json

def oldPace(laenge, bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min):
    try:
        # Convert times to seconds
        bz = int(bz_min) * 60 + int(bz_sec)
        hz = int(hz_min) * 60 + int(hz_sec)
        ez = int(ez_min) * 60 + int(ez_sec)
        
        return_dict = {}
        
        # Check if the length is at least 1km (1000m)
        if laenge >= 1000:
            # Calculate the time for 1km at each effort level
            bz_pace_1km = bz / laenge * 1000
            hz_pace_1km = hz / laenge * 1000
            ez_pace_1km = ez / laenge * 1000

            # Calculate the time at each effort level for each km
            for km in range(1, int(laenge/1000)+1):
                # Calculate the time for this km at each effort level
                bz_time = km * bz_pace_1km
                hz_time = km * hz_pace_1km
                ez_time = km * ez_pace_1km

                # Convert the time at each effort level to minutes and seconds
                bz_min_km = int(bz_time / 60)
                bz_sec_km = int(bz_time % 60)
                hz_min_km = int(hz_time / 60)
                hz_sec_km = int(hz_time % 60)
                ez_min_km = int(ez_time / 60)
                ez_sec_km = int(ez_time % 60)

                # Add the km (1000) data to the return dictionary
                return_dict[km*1000] = {
                    "bz_min": bz_min_km,
                    "bz_sec": bz_sec_km,
                    "hz_min": hz_min_km,
                    "hz_sec": hz_sec_km,
                    "ez_min": ez_min_km,
                    "ez_sec": ez_sec_km
                }
        # if less 1km (1000m) = finishing time |  so add the km data to the return dictionary
        return_dict[laenge] = {"bz_min": bz_min, "bz_sec": bz_sec, "hz_min": hz_min, "hz_sec": hz_sec, "ez_min": ez_min, "ez_sec": ez_sec
                }
        return return_dict
    
    except Exception as e:
        print('Error: ' + str(e))
        return 'Error: ' + str(e)


def pace(laenge, time_min, time_sec):
    try:
        # Convert time to seconds
        time = int(time_min) * 60 + int(time_sec)
        
        return_dict = {}
        
        # Check if the length is at least 1km (1000m)
        if laenge >= 1000:
            # Calculate the time for 1km
            pace_1km = time / laenge * 1000

            # Calculate the time for each km
            for km in range(1, int(laenge/1000)+1):
                # Calculate the time for this km
                time_km = km * pace_1km

                # Convert the time to minutes and seconds
                min_km = int(time_km / 60)
                sec_km = int(time_km % 60)

                # Add the km (1000) data to the return dictionary
                return_dict[km*1000] = {
                    "min": min_km,
                    "sec": sec_km
                }
        # if less 1km (1000m) = finishing time |  so add the km data to the return dictionary
        return_dict[laenge] = {"min": time_min, "sec": time_sec}
        return return_dict
    
    except Exception as e:
        return 'Error: ' + str(e)



def calculatePace(laenge, kmh, art):
    # Bergriffsklärung: HZ = Höchstzeit, BZ = Bestzeit, EZ = Erlaubte Zeit
    # convert laenge from m to km
    laenge = laenge / 1000
    # calculate the pace for EZ with formula: laenge in km * 60 / kmh = EZ in min
    #print(laenge, kmh, art)
    ez = (laenge * 60 / kmh)
    # convert min to sec for precise calculation
    ez = int(ez * 60)
    
    # now there is a different calculation for each art
    if art == "wegstrecke":
        hz = ez + (ez * 0.2)
        bz = ez - 120
    elif art == "hindernisstrecke":
        hz = 2 * ez
        bz = ez - 180
    elif art == "schrittstrecke":
        hz = 2 * ez
        bz = None
    else:
        raise ValueError("Error: Art not defined")

    # Convert times from seconds to minutes and seconds
    ez_min = int(ez / 60)
    ez_sec = int(ez % 60)
    hz_min = int(hz / 60)
    hz_sec = int(hz % 60)
    if bz is not None:
        bz_min = int(bz / 60)
        bz_sec = int(bz % 60)
    else:
        bz_min = None
        bz_sec = None

    return bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min

    
    

    
def getDirPath():
    # get the folder the file is in
    dirPath = os.path.dirname(os.path.realpath(__file__))
    dirPath = dirPath.replace("\\", "/") # replace backslashes with forward slashes
    return dirPath

# example call
result = oldPace(4900, 37, 14, 37, 16, 45, 19)
print(result)
# # output the results
# for km, data in result.items():
#     print(f"Kilometer {km}:")
#     print(f"\tBestzeit: {data['bz_min']}:{data['bz_sec']}")
#     print(f"\tErlaubte Zeit: {data['ez_min']}:{data['ez_sec']}")
#     print(f"\tHöchstzeit: {data['hz_min']}:{data['hz_sec']}")




def generate_pdf_from_json(json_data, output_path):
    data = json.loads(json_data)

    # PDF erstellen
    c = canvas.Canvas(output_path, pagesize=A4)

    # PDF-Inhalt erstellen
    table_header = ['Länge', 'BZ', 'EZ', 'HZ']
    table_data = [table_header]

    for key, value in data.items():
        row = [str(key) + ' m']
        if 'bz_min' in value and 'bz_sec' in value:
            row.append(f"{value['bz_min']}:{'{:02}'.format(value['bz_sec'])}")
        row.append(f"{value['ez_min']}:{'{:02}'.format(value['ez_sec'])}")
        row.append(f"{value['hz_min']}:{'{:02}'.format(value['hz_sec'])}")

        table_data.append(row)

    # Tabelle im PDF zeichnen
    x_offset = 50
    y_offset = 700
    cell_width = (A4[0] - 2 * x_offset) / len(table_header)
    cell_height = 40

    background_colors = [colors.white, colors.green, colors.orange, colors.red]

    for index, row in enumerate(table_data):
        for i, cell in enumerate(row):
            if index == 0:  # Header
                c.setFont("Helvetica-Bold", 14)
                c.setFillColor(colors.black)
            else:  # Daten
                c.setFont("Helvetica-Bold", 22)  # Größere Schriftart
                c.setFillColor(colors.black)
                c.setFillColor(background_colors[i])
                c.rect(x_offset + (i * cell_width), y_offset - cell_height, cell_width, cell_height, fill=True, stroke=True)
                c.setFillColor(colors.black if i == 0 else colors.white)

            c.drawString(x_offset + (i * cell_width) + 10, y_offset - cell_height + 10, cell)
        y_offset -= 2 * cell_height  # Lassen Sie eine Zeile frei zwischen den Reihen

    c.save()
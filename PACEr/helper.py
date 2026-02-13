import datetime
from models import db, UsageStatistic


def oldPace(laenge, bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min):
    try:
        bz = int(bz_min) * 60 + int(bz_sec)
        hz = int(hz_min) * 60 + int(hz_sec)
        ez = int(ez_min) * 60 + int(ez_sec)

        return_dict = {}

        if laenge >= 1000:
            bz_pace_1km = bz / laenge * 1000
            hz_pace_1km = hz / laenge * 1000
            ez_pace_1km = ez / laenge * 1000

            for km in range(1, int(laenge / 1000) + 1):
                bz_time = km * bz_pace_1km
                hz_time = km * hz_pace_1km
                ez_time = km * ez_pace_1km

                return_dict[km * 1000] = {
                    "bz_min": int(bz_time / 60),
                    "bz_sec": int(bz_time % 60),
                    "hz_min": int(hz_time / 60),
                    "hz_sec": int(hz_time % 60),
                    "ez_min": int(ez_time / 60),
                    "ez_sec": int(ez_time % 60),
                }

        return_dict[laenge] = {
            "bz_min": bz_min, "bz_sec": bz_sec,
            "hz_min": hz_min, "hz_sec": hz_sec,
            "ez_min": ez_min, "ez_sec": ez_sec,
        }
        return return_dict

    except Exception as e:
        print('Error: ' + str(e))
        return 'Error: ' + str(e)


def pace(laenge, time_min, time_sec):
    try:
        time = int(time_min) * 60 + int(time_sec)

        return_dict = {}

        if laenge >= 1000:
            pace_1km = time / laenge * 1000

            for km in range(1, int(laenge / 1000) + 1):
                time_km = km * pace_1km
                return_dict[km * 1000] = {
                    "min": int(time_km / 60),
                    "sec": int(time_km % 60),
                }

        return_dict[laenge] = {"min": time_min, "sec": time_sec}
        return return_dict

    except Exception as e:
        return 'Error: ' + str(e)


def calculatePace(laenge, kmh, art):
    # HZ = Höchstzeit, BZ = Bestzeit, EZ = Erlaubte Zeit
    laenge_km = laenge / 1000
    ez = (laenge_km * 60 / kmh)
    ez = int(ez * 60)

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


def writeStatistics():
    today = datetime.date.today()
    stat = UsageStatistic.query.filter_by(date=today).first()
    if stat:
        stat.count += 1
    else:
        stat = UsageStatistic(date=today, count=1)
        db.session.add(stat)
    db.session.commit()

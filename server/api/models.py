import csv



class Beat:

    def __init__(self, name, address):
        self._name = name
        self._address = address

    def toDict(self):
        return  {
            'task': 'server.api.tasks.send_health_check',
            'schedule': 10.0,
            "args": (self._address,)
            
            }
        


   

class FileParser:

    def __init__(self, filename):
        self._filename = filename

    def getBeatSchedule(self):
        with open(self._filename, mode="r") as hosts:
            beat_schedule = {}
            csvreader = csv.reader(hosts)
            for row in csvreader:
                beat = Beat(row[0].strip(" "), row[1].strip(" ")) 
                beat_schedule[beat._name] = beat.toDict()
            return beat_schedule
                
    def getHostFromFile(self, address):
        with open(self._filename, mode="r") as hosts:
            csvreader = csv.reader(hosts)
            for row in csvreader:
                beat = Beat(row[0].strip(" "), row[1].strip(" ")) 
                if beat._address == address:
                    return beat
            return None

               
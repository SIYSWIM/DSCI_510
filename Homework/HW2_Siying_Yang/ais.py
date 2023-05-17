from __future__ import annotations
from math import sin, cos, sqrt, atan2, radians
from typing import Optional, Tuple
import re
import sys

## Q4
class GeoCoordinates:
    def __init__(self, lat: Optional[float] = None, long: Optional[float] = None, dms: Optional[str] = None):
        self.lat = lat
        self.long = long
        self.dms = dms
        ## convert
        if self.dms:
            self.convert_from_dms()
        elif self.lat and self.long:
            self.convert_from_latlong()


    def convert_from_dms(self) -> str:
        if self.dms:
            convert_type = self.dms.split(' ')
            la = convert_type[0]
            lo = convert_type[1]
            # convert latitudes
            if '″' in la:
                pattern = re.findall(r'^(?P<degree>[^°]+)\S(?P<minute>[^′]+)\S(?P<second>[^″]+)\S(?P<direction>[^\s]+)', la)
                for x, y, z, i in pattern:
                    degree = int(x)
                    minute = int(y)
                    second = float(z)
                    direction = i
                    lat = degree + (minute/60) + (second/3600)
                    if direction == 'S':
                        lat = -lat
                    else:
                        lat = lat
            else:
                pattern = re.findall(r'^(?P<degree>[^°]+)\S(?P<minute>[^′]+)\S(?P<direction>[^\s]+)',la)
                for x, y, i in pattern:
                    degree = int(x)
                    minute = int(y)
                    direction = i
                    lat = degree + (minute/60)
                    if direction == 'S':
                        lat = -lat
                    else:
                        lat = lat
            # convert longitudes
            if '″' in lo:
                pattern = re.findall(r'^(?P<degree>[^°]+)\S(?P<minute>[^′]+)\S(?P<second>[^″]+)\S(?P<direction>[^\s]+)', lo)
                for x, y, z, i in pattern:
                    degree = int(x)
                    minute = int(y)
                    second = float(z)
                    direction = i
                    long = degree + (minute/60) + (second/3600)
                    if direction == 'W':
                        long = -long
                    else:
                        long = long
            else:
                pattern = re.findall(r'^(?P<degree>[^°]+)\S(?P<minute>[^′]+)\S(?P<direction>[^\s]+)',lo)
                for x, y, i in pattern:
                    degree = int(x)
                    minute = int(y)
                    direction = i
                    long = degree + (minute/60)
                    if direction == 'W':
                        long = -long
                    else:
                        long = long
        self.lat = lat
        self.long = long
    
    def convert_from_latlong(self) -> str:
        if self.lat and self.long:
            # la
            if self.lat >= 0:
                la_degree = int(self.lat)
                la_min = (self.lat - la_degree)*60
                la_sec = (la_min - int(la_min))*60
                la = f'{la_degree}°{int(la_min)}′{int(la_sec)}″N'
            else:
                la_degree = int(abs(self.lat))
                la_min = (abs(self.lat) - la_degree)*60
                la_sec = (la_min - int(la_min))*60
                la = f'{la_degree}°{int(la_min)}′{int(la_sec)}″S'
            # lo
            if self.long >= 0:
                lo_degree = int(self.long)
                lo_min = (self.long - lo_degree)*60
                lo_sec = (lo_min - int(lo_min))*60
                lo = f'{lo_degree}°{int(lo_min)}′{int(lo_sec)}″E'
            else:
                lo_degree = int(abs(self.long))
                lo_min = (abs(self.long) - lo_degree)*60
                lo_sec = (lo_min - int(lo_min))*60
                lo = f'{lo_degree}°{int(lo_min)}′{int(lo_sec)}″W'
        self.dms = f'{la} {lo}'

    def __str__(self) -> str:
        output = f'{self.dms} (lat:{self.lat}, long:{self.long})'
        return output
   
    def distance(self, other: GeoCoordinates) -> float:
        earth_radius = 6373.0  # in kilometers
        lat1 = radians(self.lat)
        lon1 = radians(self.long)
        lat2 = radians(other.lat)
        lon2 = radians(other.long)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = earth_radius * c
        return distance  # in kilometers

## Q5
class Airport:
    def __init__(self, code: str, airport_name: str, airport_location: str):
        self.code = code
        self.name = airport_name
        self.location = airport_location

    def __str__(self) -> str:
        output = f'{self.code}\t{self.name}\t({self.location})'
        return output


class GeoAirport(Airport):
    def __init__(self,  code: str, airport_name: str, airport_location: str, geo_corrdinates: str, nearby: list[tuple] = []):
        super().__init__(code, airport_name, airport_location)
        self.geo = geo_corrdinates
        # within a 100km range (distance: float, nearby_airport: GeoAirport)
        self.nearby = nearby
        
    def __str__(self):
        if self.geo:
            return f'{self.code}\t{self.name}\t({self.location}; {self.geo})'
        else:
            return f'{self.code}\t{self.name}\t({self.location})'
    
    def nearby_airports(self):
        nearby_str = ''
        for near in self.nearby:
            dist = near[0]
            code = near[1].code
            name = near[1].name
            nearby_str += f"   Nearby:\t{dist:>2}km\t{code}\t{name}\n"
        return nearby_str


## main program
def main():
    # Airport instance
    airport_instance_dict = {}
    with open('airports.tsv', 'r') as f:
        for line in f:
            if line.strip():
                object = line.split('\t')
                code = object[0]
                airport_name = object[1]
                airport_location = object[2]
                airport_instance_dict[code] = Airport(code, airport_name, airport_location)

    # Geoairport instance
    airport_coordinate = {}
    with open('airport-coordinates.tsv', 'r') as d:
        for x in d:
            if x.strip():
                object = x.split('\t')
                airport_coordinate[object[0]] = object[1].strip()
    
    airports_GeoAirport = {}

    # Build GeoAirport instances for all airports
    for c, coord in airport_coordinate.items():
        code = airport_instance_dict[c].code
        name = airport_instance_dict[c].name
        airport_location = airport_instance_dict[c].location
        # airports_GeoAirport = {code: GeoAirport(code, name, location, coord, nearby)}
        airports_GeoAirport[c] = GeoAirport(code, name, airport_location, geo_corrdinates = coord, nearby =[]) 
    
    # Update nearby_airports for all airports (GeoAirport instance)  
    for x, y in airport_coordinate.items():
        for a, b in airport_coordinate.items():
            # Skip comparing two identical airport
            if x == a:
                continue
            if y and b:  # Some coordinates are missing
                distance_km = round(GeoCoordinates(dms = y).distance(GeoCoordinates(dms = b)))
                if distance_km <= 100:
                    # Append nearby airport to nearby_airport list of the current instance
                    airports_GeoAirport[x].nearby.append((distance_km, airports_GeoAirport[a]))

        airports_GeoAirport[x].nearby.sort(key = lambda x: x[0])

    # example 1, 2
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in airports_GeoAirport:
            print(airports_GeoAirport[arg])
            print(airports_GeoAirport[arg].nearby_airports())
        elif arg in airport_instance_dict:
            print(airport_instance_dict[arg])
    # example 3
        else:
            # print out airport with coordinates
            airport_sample3 = []
            for airport in airports_GeoAirport:
                if arg in airports_GeoAirport[airport].name:
                    airport_sample3.append(airports_GeoAirport[airport].code)
                    print(airports_GeoAirport[airport])
            for airport in airport_instance_dict:
                if arg in airport_instance_dict[airport].name:
                    if airport_instance_dict[airport].code not in airport_sample3:
                        airport_sample3.append(airport_instance_dict[airport].code)
                        print(airport_instance_dict[airport])
    elif len(sys.argv) == 3:
        # example 4
        arg1, arg2 = float(sys.argv[1]), float(sys.argv[2])
        airports = []  # [(distance, GeoAirport)]
        for c in airports_GeoAirport:
            current_airport = airports_GeoAirport[c]
            if current_airport.geo:
                dist = round(GeoCoordinates(dms=current_airport.geo).distance(GeoCoordinates(lat=arg1, long=arg2)))
                airports.append((dist, current_airport))
        airports.sort(key = lambda x: x[0])
        print(f'{airports[0][0]}km\t{airports[0][1]}')

    elif len(sys.argv) == 4:
        # example 5
        arg1, arg2 = sys.argv[1], sys.argv[2]
        nums = int(sys.argv[3])
        lat, long, dms = None, None, None
        try:
            lat = float(arg1)
            long = float(arg2)
        except:
            dms = f'{arg1} {arg2}'
        airports = []  # [(distance, GeoAirport)]
        for c in airports_GeoAirport:
            current_airport = airports_GeoAirport[c]
            if current_airport.geo:
                dist = round(GeoCoordinates(dms=current_airport.geo).distance(GeoCoordinates(lat=lat, long=long, dms=dms)))
                airports.append((dist, current_airport))
        airports.sort(key = lambda x: x[0]) 
        for i in range(nums):
            print(f"{airports[i][0]}km\t{airports[i][1]}")  

if __name__ == '__main__':
    main()
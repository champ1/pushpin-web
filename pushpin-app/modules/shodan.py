from modules import module
# unique to module
from datetime import datetime
from django.conf import settings

class Shodan(module.Module):

    def __init__(self):
        return

    def run(self, locname, lat, lon, rad):
        self.output("Collecting data from Shodan...")
        pins = []
        point = str(lat) + "," + str(lon)
        query = 'geo:%s,%d' % (point, rad)
        # setting limit to 1 to limit 1 API request per location
        limit = 1
        # TODO: shodan sometimes times out and throws an error
        results = self.search_shodan_api(query, limit)
        for host in results:
            os = host['os'] if 'os' in host else ''
            hostname = host['hostnames'][0] if len(host['hostnames']) > 0 else 'None'
            protocol = '%s:%d' % (host['ip_str'], host['port'])
            source = 'Shodan'
            screen_name = protocol
            profile_name = protocol
            profile_url = 'http://%s' % (protocol)
            media_url = 'http://www.shodanhq.com/search?q=net:' + str(host['ip_str'])
            thumb_url = settings.STATIC_URL + 'images/shodan.png'
            message = 'Hostname: %s | City: %s, %s | OS: %s' % (hostname, host['location']['city'], host['location']['country_name'], os)
            latitude = host['location']['latitude']
            longitude = host['location']['longitude']
            time = datetime.strptime(host['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
            pins.append(self.createPin(source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude, longitude, time))
        self.addPins(locname, pins)
        #self.summarize(new, len(results))

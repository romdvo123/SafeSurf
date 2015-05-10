import pygeoip, os
#from uuid import getnode as get_mac

class FireWall:
    def __init__(self,blacklists_path,geolocation_path):
        #porn
        self.blacklist_porn_path = os.path.join(
            blacklists_path,"porn")
        self.porn_urls = os.path.join(
            self.blacklist_porn_path,"urls")
        self.porn_domains = os.path.join(
            self.blacklist_porn_path,"domains")
        self.porn_expressions = os.path.join(
            self.blacklist_porn_path,"expressions")

        #ecommerce
        self.blacklist_ecommerce_path = os.path.join(
            blacklists_path,"ecommerce")
        self.ecommerce_urls = os.path.join(
            self.blacklist_ecommerce_path,"urls")
        self.ecommerce_domains = os.path.join(
            self.blacklist_ecommerce_path,"domains")

        #countries
        self.blacklist_countries_path = os.path.join(
            blacklists_path,"countries")
        self.countries_banned = os.path.join(
            self.blacklist_countries_path,"banned")
        
        print "Loaded blacklists"

        #geolocation
        self.geolocation = pygeoip.GeoIP(geolocation_path)
        
        print "Loaded geolocation"

    def location_query(self,ip,user):
        directory
        data = self.geolocation.record_by_name(ip)
        country = data['country_name']
        with open(self.countries_banned,'r') as banned:
            banned_list = banned.read().split("\n")
            if country in banned_list:
                print "DETECTED: BANNED COUNTRY - %s"%str(country)
                return (1,str(country))
        return (0,str(country))

    def blacklist_url_query(self,url):
        with open(self.porn_urls,'r') as urls:
            urls_list = urls.read().split("\n")
            if url in urls_list:
                print "DETECTED: PORN SITE URL"
                return 1
        with open(self.ecommerce_urls,'r') as urls:
            urls_list = urls.read().split("\n")
            if url in urls_list:
                print "DETECTED: ECOMMERCE SITE URL"
                return 1
        return 0
                
    def blacklist_domain_query(self,domain):       
        with open(self.porn_domains,'r') as domains:
            domains_list = domains.read().split("\n")
            if domain in domains_list:
                print "DETECTED: PORN SITE DOMAIN"
                return 1
        with open(self.ecommerce_domains,'r') as domains:
            domains_list = domains.read().split("\n")
            if domain in domains_list:
                print "DETECTED: ECOMMERCE SITE DOMAIN"
                return 1
        return 0
    
    def blacklist_expressions_query(self,host):
        with open(self.porn_expressions,'r') as expressions:
            expressions_list = expressions.read().split("\n")
            for expression in expressions_list:
                if expression in host:
                    print "DETECTED: PORN EXPRESSION"
                    return 1
        return 0

    def private_blacklists(self,user):
        #get ip , go to his directory. every query first checks if the private file
        #exists, if yes it reads from it. first checks if its in the allowed part,
        #then checks if its

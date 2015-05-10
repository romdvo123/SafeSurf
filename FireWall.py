import pygeoip, os
#from uuid import getnode as get_mac

class FireWall:
    def __init__(self,blacklists_path,geolocation_path):
        self.base_path = os.path.join(os.path.split(blacklists_path)[0],
                                      'accounts')
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
        data = self.geolocation.record_by_name(ip)
        country = data['country_name']
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','countries','banned')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    allowed = False
                    banned = False
                    private_list = private.read().split('\n')
                    for _country in private_list:
                        if _country != '':
                            country_split = _country.split(';')
                            if len(country_split) > 1:
                                if country_split[1] == country:
                                    allowed = True
                                    break
                            else:
                                if _country == country:
                                    banned = True
                                    break
                if allowed:
                    return (0,str(country))
                elif banned:
                    print "DETECTED: BANNED COUNTRY - %s"%str(country)
                    return (1,str(country))
        with open(self.countries_banned,'r') as banned:
            banned_list = banned.read().split("\n")
            if country in banned_list:
                print "DETECTED: BANNED COUNTRY - %s"%str(country)
                return (1,str(country))
        return (0,str(country))

    def blacklist_url_query(self,url,user):
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','porn','urls')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    allowed = False
                    banned = False
                    private_list = private.read().split('\n')
                    for _url in private_list:
                        if _url != '':
                            url_split = _url.split(';')
                            if len(url_split) > 1:
                                if url_split[1] in url:
                                    allowed = True
                                    break
                            else:
                                if _url in url:
                                    banned = True
                                    break
                if allowed:
                    return 0
                elif banned:
                    print "DETECTED: PORN SITE URL"
                    return 1
        with open(self.porn_urls,'r') as urls:
            urls_list = urls.read().split("\n")
            if url in urls_list:
                print "DETECTED: PORN SITE URL"
                return 1
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','ecommerce','urls')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    allowed = False
                    banned = False
                    private_list = private.read().split('\n')
                    for _url in private_list:
                        if _url != '':
                            url_split = _url.split(';')
                            if len(url_split) > 1:
                                if url_split[1] in url:
                                    allowed = True
                                    break
                            else:
                                if _url in url:
                                    banned = True
                                    break
                if allowed:
                    return 0
                elif banned:
                    print "DETECTED: ECOMMERCE SITE URL"
                    return 1
        with open(self.ecommerce_urls,'r') as urls:
            urls_list = urls.read().split("\n")
            if url in urls_list:
                print "DETECTED: ECOMMERCE SITE URL"
                return 1
        return 0
                
    def blacklist_domain_query(self,domain,user):
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','porn','domains')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    allowed = False
                    banned = False
                    private_list = private.read().split('\n')
                    for _domain in private_list:
                        if _domain != '':
                            domain_split = _domain.split(';')
                            if len(domain_split) > 1:
                                if domain_split[1] in domain:
                                    allowed = True
                                    break
                            else:
                                if _domain in domain:
                                    banned = True
                                    break
                if allowed:
                    return 0
                elif banned:
                    print "DETECTED: PORN SITE DOMAIN"
                    return 1
        with open(self.porn_domains,'r') as domains:
            domains_list = domains.read().split("\n")
            if domain in domains_list:
                print "DETECTED: PORN SITE DOMAIN"
                return 1
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','ecommerce','domains')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    allowed = False
                    banned = False
                    private_list = private.read().split('\n')
                    for _domain in private_list:
                        if _domain != '':
                            domain_split = _domain.split(';')
                            if len(domain_split) > 1:
                                if domain_split[1] in domain:
                                    allowed = True
                                    break
                            else:
                                if _domain in domain:
                                    banned = True
                                    break
                if allowed:
                    return 0
                elif banned:
                    print "DETECTED: ECOMMERCE SITE DOMAIN"
                    return 1
        with open(self.ecommerce_domains,'r') as domains:
            domains_list = domains.read().split("\n")
            if domain in domains_list:
                print "DETECTED: ECOMMERCE SITE DOMAIN"
                return 1
        return 0
    
    def blacklist_expressions_query(self,host,user):
        allowed_expressions = []
        if user != None:
            directory = os.path.join(self.base_path,user,'blacklists','porn','expressions')
            if os.path.exists(directory):
                with open(directory,'r') as private:
                    banned = False
                    private_list = private.read().split('\n')
                    for _expression in private_list:
                        if _expression != '':
                            expression_split = _expression.split(';')
                            if len(expression_split) > 1:
                                if expression_split[1] in host:
                                    allowed_expressions.append(expression_split[1])
                            else:
                                if _expression in host:
                                    banned = True
                                    break
                if banned:
                    print "DETECTED: PORN EXPRESSION"
                    return 1
        
        if len(allowed_expressions)>0:
            with open(self.porn_expressions,'r') as expressions:
                expressions_list = expressions.read().split("\n")
                for expression in expressions_list:
                    if expression in host:
                        if expression in allowed_expressions:
                            allowed_expressions.remove(expression)
                        else:
                            print "DETECTED: PORN EXPRESSION"
                            return 1
            return 0
        else:
            with open(self.porn_expressions,'r') as expressions:
                expressions_list = expressions.read().split("\n")
                for expression in expressions_list:
                    if expression in host:
                        print "DETECTED: PORN EXPRESSION"
                        return 1
            return 0

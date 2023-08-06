from .base import Friendlyscore


class Cloud(Friendlyscore):

    def user_social_network_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/show/social-network-data"
                        .format(self.by, self.id))

    def user_data_points(self):
        self.getToken()
        return self.get("users/{0}/{1}/show/data-points"
                        .format(self.by, self.id))

    def user_heat_map_coordinates(self):
        self.getToken()
        return self.get("users/{0}/{1}/show/heat-map-coordinates"
                        .format(self.by, self.id))

    def fraud_alerts(self):
        self.getToken()
        return self.get("fraudalerts/{0}/{1}/show"
                        .format(self.by, self.id))

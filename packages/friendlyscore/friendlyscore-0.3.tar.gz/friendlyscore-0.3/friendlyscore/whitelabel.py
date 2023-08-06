from .base import Friendlyscore


class WhiteLabel(Friendlyscore):

    def __init__(self, url, cid, sec):
        self.by = None
        self.id = None
        self.client_id = cid
        self.client_secret = sec
        self.base_url = url.rstrip('/') + '/'
        self.request_token_url = self.base_url + 'oauth/v2/token'

    def get_score(self, partner_user_id=None):
        if partner_user_id is None and self.by == 'partner-id':
            partner_user_id = self.id

        # TODO
        # raise ArgumentError, 'Either argument partner_user_id must be passed or by_partner_id() method must be called before get_score' if partner_user_id.nil?
        return self.get('get_score', {'partner_user_id': partner_user_id})

    def user_facebook_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/facebook-data"
                        .format(self.by, self.id))

    def user_linkedin_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/linkedin-data"
                        .format(self.by, self.id))

    def user_twitter_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/twitter-data"
                        .format(self.by, self.id))

    def user_google_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/google-data"
                        .format(self.by, self.id))

    def user_paypal_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/paypal-data"
                        .format(self.by, self.id))

    def user_instagram_data(self):
        self.getToken()
        return self.get("users/{0}/{1}/instagram-data"
                        .format(self.by, self.id))

# the real code lives here, mostly authenticating to microsoft
# no creepers allowed!

import os, requests, json
from pathlib import Path
from tokens import OAuthToken, UserToken, XSTSToken
from exceptions import AuthenticationException, MinecraftApiException, NoOauthTokenException

class IsAnyoneInTheMine:

    OAUTH_URL = "https://login.live.com/oauth20_token.srf"
    USER_URL = "https://user.auth.xboxlive.com/user/authenticate"
    XSTS_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"
    MINECRAFT_URI = "https://pocket.realms.minecraft.net/"
    SCOPES = ["Xboxlive.signin", "Xboxlive.offline_access"]

    def __init__(self, client_id=None, client_secret=None, token_file=None):
        self.client_id = client_id or os.getenv("CLIENT_ID")
        self.client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.token_file_path = token_file or os.getenv("TOKEN_FILE")
        try:
            self.oauth_token = self.load_oauth_token_from_file(self.token_file_path)
        except NoOauthTokenException:
            # TODO if this happens, we need to do the "auth" loop again
            raise NoOauthTokenException("Could not find the original oauthtoken, check your token file")
        self.user_token = None
        self.xsts_token = None

    def is_anyone_in_the_mine(self):
        self.check_and_refresh_auth()
        active_player_data = self._get_active_minecraft_realms_players()
        return True if "servers" in active_player_data and len(active_player_data["servers"]) > 0 else False

    def check_and_refresh_auth(self):
        if not self.oauth_token or not self.oauth_token.is_valid():
            self.oauth_token = self._get_oauth_token()
        if not self.user_token or not self.oauth_token.is_valid():
            self.user_token = self._get_user_token()
        if not self.xsts_token or not self.xsts_token.is_valid():
            self.xsts_token = self._get_xsts_token()
    
    def load_oauth_token_from_file(self, filepath):
        token_file = Path(filepath)
        if token_file.exists():
            with open(token_file, 'r') as f:
                return OAuthToken(**json.load(f))
        return None

    def write_oauth_token_to_file(self, filepath, token):
        token_file = Path(filepath)
        with open(token_file, 'w') as f:
            f.write(token.json())

    def _get_oauth_token_from_auth_code(self, auth_code, redirect_uri, url=OAUTH_URL, scopes=SCOPES):
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "scope": " ".join(scopes),
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data)
        return OAuthToken(**json.loads(response.text))

    def _get_oauth_token(self, url=OAUTH_URL, scopes=SCOPES):
        data = {
            "grant_type": "refresh_token",
            "scope": " ".join(scopes),
            "refresh_token": self.oauth_token.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data)
        if not response.ok:
            raise AuthenticationException("Problem authenticating. ERROR {0}".format(response.status_code))
        return OAuthToken(**json.loads(response.text))

    def _get_user_token(self, url=USER_URL):
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": "d={0}".format(self.oauth_token.access_token),
            }
        }
        response = requests.post(url, json=data)
        if not response.ok:
            raise AuthenticationException("Problem authenticating. ERROR {0}".format(response.status_code))
        return UserToken(**json.loads(response.text))

    def _get_xsts_token(self, url=XSTS_URL, relying_party=MINECRAFT_URI):
        data = {
            "RelyingParty": relying_party,
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [self.user_token.Token],
                "SandboxId": "RETAIL",
            },
        }
        response = requests.post(url, json=data)
        if not response.ok:
            raise AuthenticationException("Problem authenticating. ERROR {0}".format(response.status_code))
        return XSTSToken(**json.loads(response.text))

    def _get_active_minecraft_realms_players(self, minecraft_uri=MINECRAFT_URI):
        url = "{0}activities/live/players".format(minecraft_uri)
        headers = {
            "User-Agent" : "MCPE/UWP",
            "Host" : "pocket.realms.minecraft.net",
            "Client-Version" : "1.17.10",
            "Authorization" : self.xsts_token.get_auth_header(),
        }
        response = requests.get(url, headers=headers)
        if not response.ok:
            raise MinecraftApiException("Problem accessing the minecraft API. ERROR {0}".format(response.status_code))
        return json.loads(response.text)

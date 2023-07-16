# models for all the tokens

from dataclasses import dataclass
from typing import Optional

class Token:

    def is_valid(self):
        return False
    
@dataclass
class OAuthToken(Token):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    user_id: str
    issued: Optional[str] = None

    def is_valid(self):
        # TODO DO THIS
        return False 

@dataclass
class XSTSToken(Token):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaims: dict

    def get_auth_header(self):
        return "XBL3.0 x={0};{1}".format(self.DisplayClaims['xui'][0]['uhs'], self.Token)

    def is_valid(self):
        return False

@dataclass
class UserToken(Token):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaims: dict

    def is_valid(self):
        return False
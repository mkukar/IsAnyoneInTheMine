# models for all the tokens

from dataclasses import dataclass, field, asdict
import json
from typing import Optional
from datetime import datetime, timedelta, timezone
from abc import ABC, abstractmethod

def now_datetime():
    return datetime.now(timezone.utc)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

class Token(ABC):

    @abstractmethod
    def is_valid(self):
        return False
    
    def json(self):
        return json.dumps(asdict(self), default=str)
    

@dataclass
class OAuthToken(Token):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    user_id: str
    issued: Optional[datetime] = field(default_factory=now_iso)

    def __post_init__(self):
        if isinstance(self.issued, str):
            self.issued = datetime.fromisoformat(self.issued)

    def is_valid(self):
        return (self.issued + timedelta(seconds=self.expires_in)) > now_datetime()


@dataclass
class UserToken(Token):
    IssueInstant: datetime
    NotAfter: datetime
    Token: str
    DisplayClaims: dict

    def __post_init__(self):
        if isinstance(self.IssueInstant, str):
            self.IssueInstant = datetime.strptime(self.IssueInstant.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            self.IssueInstant = self.IssueInstant.replace(tzinfo=timezone.utc)
        if isinstance(self.NotAfter, str):
            self.NotAfter = datetime.strptime(self.NotAfter.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            self.NotAfter = self.NotAfter.replace(tzinfo=timezone.utc)

    def is_valid(self):
        return self.NotAfter > now_datetime()
    

@dataclass
class XSTSToken(UserToken):
    def get_auth_header(self):
        return "XBL3.0 x={0};{1}".format(self.DisplayClaims['xui'][0]['uhs'], self.Token)

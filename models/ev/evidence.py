from pydantic import BaseModel


class EvidenceBase(BaseModel):
    license: str
    projectId: str
    personaId: str
    fullname: str
    initiated: int = None   # first init timestamp
    started: int = None     # start timestamp
    finished: int = None    # finish timestamp
    touched: int = None     # last timestamp
    # minutes * 60 * 000
    maxTime: int = 0        # Max net time consumed
    netTime: int = 0        # Net time consumed
    remains: int = 0        # Time reamining
    items: int              # number of test items
    done: int = 0       # Last number touched

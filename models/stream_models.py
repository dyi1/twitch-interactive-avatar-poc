from pydantic import BaseModel

class StreamBaseModel(BaseModel):
    stream_id: str
    success: bool


class SDPOfferModel(BaseModel):
    sdp: str
    type: str
from pydantic import BaseModel

class StreamBaseModel(BaseModel):
    stream_id: str
    success: bool


class HeygenSessionModel(BaseModel):
    session_id: str
    access_token: str
    url: str


class LivekitData(BaseModel):
    room_name: str
    stream_id: str


class GlobalStreamData(BaseModel):
    heygen_session: HeygenSessionModel
    livekit_data: LivekitData
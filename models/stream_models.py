from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class StreamBaseModel(BaseModel):
    stream_id: str
    success: bool


class HeygenSessionModel(BaseModel):
    session_id: str
    access_token: str
    url: str
    realtime_endpoint: str


class LivekitData(BaseModel):
    room_name: str
    stream_id: str

class ChatMessage(BaseModel):
    text: str
    task_type: str = "chat"
    twitch_username: Optional[str] = None

class AvatarStatus(str, Enum):
    IDLE = "idle"
    TALKING = "talking"

class GlobalStreamData(BaseModel):
    listener_enabled: bool = False
    tw_chat_listener_enabled: bool = False
    avatar_status: AvatarStatus = AvatarStatus.IDLE
    heygen_session: HeygenSessionModel
    livekit_data: LivekitData
    chat_queue: List[ChatMessage] = []
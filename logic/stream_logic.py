import os
from logic.twitch_client import TwitchClient
from models.stream_models import StreamBaseModel
from logic.heygen_client import HeygenClient
from logic.livekit_room import LivekitRoom
from livekit import api


async def start_stream():
    heygen_client = HeygenClient()
    session_info = heygen_client.create_session()
    heygen_client.start_stream(session_info.session_id)

    room = LivekitRoom()
    await room.connect(session_info.url, session_info.access_token)

    live_kit_api_key = os.getenv("LIVEKIT_API_KEY")
    live_kit_api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    # Create the LiveKitAPI client
    lk_api = api.LiveKitAPI(
        session_info.url,
        live_kit_api_key,
        live_kit_api_secret
    )
    
    # Get the egress client
    egress_client = lk_api.egress
    twitch_client = TwitchClient()
    
    start_request = api.RoomCompositeEgressRequest(
        room_name=room.room.name,
        stream_outputs=[
            api.StreamOutput(
                protocol=api.StreamProtocol.RTMP,
                urls=[twitch_client.get_stream_url()]
            )
        ]
    )
    try:
        egress_info = await egress_client.start_room_composite_egress(
            start_request
        )
        
        print(f"Egress started with ID: {egress_info.egress_id}")
        print(f"Status: {egress_info.status}")
        
        return StreamBaseModel(stream_id=egress_info.egress_id, success=True)
        
    except Exception as e:
        print(f"Failed to start egress: {e}")
        raise
    finally:
        # Important: Close the API client to avoid the "Unclosed client session" warning
        await lk_api.aclose()
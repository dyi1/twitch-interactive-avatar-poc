import json
import os
import random
import threading
from logic.twitch_client import TwitchClient
from models.stream_models import AvatarStatus, ChatMessage, LivekitData, StreamBaseModel
from logic.heygen_client import HeygenClient
from logic.livekit_room import LivekitRoom
from livekit import api
import websocket

from models.stream_models import GlobalStreamData
TOPICS = [
    "Tell me a story about HeyGen", 
    "Let me know about the latest and greatest in AI",
    "What is the weather in Tokyo?",
]
global_stream_data: GlobalStreamData = None

def get_global_stream_data() -> GlobalStreamData:
    global global_stream_data
    return global_stream_data

def set_global_stream_data(data: GlobalStreamData) -> None:
    global global_stream_data
    global_stream_data = data

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

        live_kit_data = LivekitData(
            room_name=room.room.name,
            stream_id=egress_info.egress_id
        )

        global_stream_data = GlobalStreamData(
            heygen_session=session_info,
            livekit_data=live_kit_data
        )
        set_global_stream_data(global_stream_data)
        return StreamBaseModel(stream_id=egress_info.egress_id, success=True)
        
    except Exception as e:
        print(f"Failed to start egress: {e}")
        raise
    finally:
        # Important: Close the API client to avoid the "Unclosed client session" warning
        await lk_api.aclose()


async def send_text_to_stream(text: str, task_type: str = "chat"):
    global_stream_data = get_global_stream_data()
    if global_stream_data is None:
        print("No stream data running")
        return
    
    global_stream_data.chat_queue.append(
        ChatMessage(
            text=text,
            task_type=task_type,
        )
    )

    return True

async def background_stream_task():
    global_stream_data = get_global_stream_data()
    if global_stream_data is None:
        print("No stream data running")
        return
    
    print(global_stream_data.chat_queue)
    print(global_stream_data.avatar_status)
    if global_stream_data.avatar_status == AvatarStatus.IDLE:
        if len(global_stream_data.chat_queue) > 0:

            chat_message = global_stream_data.chat_queue.pop(0)
            text = chat_message.text
            task_type = chat_message.task_type
        else:
            text = random.choice(TOPICS)
            task_type = "chat"

        heygen_client = HeygenClient()
        session_id = global_stream_data.heygen_session.session_id
        heygen_client.send_text(session_id, text, task_type)
        global_stream_data.avatar_status = AvatarStatus.TALKING
        

async def avatar_status_listener():
    global_stream_data = get_global_stream_data()
    if global_stream_data is None:
        print("No stream data running")
        return
    
    if global_stream_data.listener_enabled:
        print("Listener already enabled")
        return

    def on_message(ws, message):
        print("Received:", message)
        json_data = json.loads(message)
        if json_data.get("state") == 0:
            global_stream_data.avatar_status = AvatarStatus.IDLE

    def on_error(ws, error):
        print("Error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("Connection closed:", close_status_code, close_msg)

    def on_open(ws):
        print("Connection opened")

    def start_listener():
        ws = websocket.WebSocketApp(
            global_stream_data.heygen_session.realtime_endpoint,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        ws.run_forever()
    
    thread = threading.Thread(target=start_listener)
    thread.daemon = False  # Keep the process alive
    thread.start()

    global_stream_data.listener_enabled = True
    
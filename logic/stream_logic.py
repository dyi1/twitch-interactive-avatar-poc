from logic.twitch_client import TwitchClient
from models.stream_models import SDPOfferModel, StreamBaseModel
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRecorder

# pcs = set()

async def start_stream():
    twitch_client = TwitchClient()
    twitch_client.stream_to_twitch()
    # print(url)
    # offer = SDPOfferModel(sdp=twitch_client.get_stream_url(), type="offer")
    # pc = RTCPeerConnection()
    # pcs.add(pc)

    # recorder = MediaRecorder(twitch_client.get_stream_url(), format="flv")

    # @pc.on("track")
    # async def on_track(track):
    #     print(f"🎥 Track received: {track.kind}")
    #     await recorder.addTrack(track)

    #     @track.on("ended")
    #     async def on_ended():
    #         print(f"🛑 Track ended: {track.kind}")
    #         await recorder.stop()

    # await pc.setRemoteDescription(RTCSessionDescription(sdp=offer.sdp, type=offer.type))
    # await recorder.start()

    # answer = await pc.createAnswer()
    # await pc.setLocalDescription(answer)

    # return {
    #     "sdp": pc.localDescription.sdp,
    #     "type": pc.localDescription.type
    # }

    return StreamBaseModel(stream_id="1234567890", success=True)
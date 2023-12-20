from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, LikeEvent

import time
import tinytuya

userName = input("Username: ")
view_only = True if input("View only? (y/n) ") == "y" else False



rainbow = {
    "red": [255, 0, 0],
    "orange": [255, 127, 0],
    "yellow": [255, 200, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "indigo": [46, 43, 95],
    "violet": [139, 0, 255],
}

baloonColors = {
    "silver": [192, 192, 192],
    "light blue": [5, 242, 215],
    "pink": [245, 5, 221],
    "gold": [237, 222, 9],
}

gunColors = {"violet": [139, 0, 255], "green": [0, 255, 0], "gold": [237, 222, 9]}

light = tinytuya.BulbDevice(
    dev_id="",
    address="",
    local_key="",
    version=3.3,
)


def baloon_gift():
    for x in range(0, 2):
        for color in baloonColors:
            [r, g, b] = baloonColors[color]
            light.set_colour(
                r, g, b, nowait=True
            )  # nowait = Go fast don't wait for response
            time.sleep(0.25)


def galaxy():
    for x in range(0, 10):
        for color in rainbow:
            [r, g, b] = rainbow[color]
            light.set_colour(
                r, g, b, nowait=True
            )  # nowait = Go fast don't wait for response
            time.sleep(0.25)


def money_gun():
    for x in range(0, 2):
        for color in gunColors:
            [r, g, b] = gunColors[color]
            light.set_colour(
                r, g, b, nowait=True
            )  # nowait = Go fast don't wait for response
            time.sleep(0.25)


client: TikTokLiveClient = TikTokLiveClient(unique_id=userName)





@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


@client.on("gift")
async def on_gift(event: GiftEvent):
    light.turn_on()
    if(not view_only):
        match event.gift.info.name:
            case "Rose":
                light.set_colour(245, 5, 221, nowait=True)
            case "Rosa":
                light.set_colour(255, 0, 0, nowait=True)
            case "Tiny Diny":
                light.set_colour(0, 255, 0, nowait=True)
            case "Balloons":
                baloon_gift()
            case "Galaxy":
                galaxy()
            case "TikTok":
                light.set_colour(255, 255, 255)
            case "Money Gun":
                money_gun()

    if event.gift.streakable and not event.gift.streaking:
        print(
            f'{event.user.unique_id} sent {event.gift.count}x "{event.gift.info.name}"'
        )

    elif not event.gift.streakable:
        print(f'{event.user.unique_id} sent "{event.gift.info.name}"')

if(not view_only):
    @client.on("like")
    async def on_like(event: LikeEvent):
        if light.status()["dps"]["1"]:
            light.turn_off()
        else:
            light.turn_on()


async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} -> {event.comment}")


client.add_listener("comment", on_comment)

if __name__ == "__main__":
    client.run()



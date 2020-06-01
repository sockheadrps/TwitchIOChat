from twitchio.ext import commands
from twitchio.client import Client
import asyncio
import requests
import time
import os
import playsound
from gtts import gTTS


irc_token = 'xxxx'
client_id = 'xxxx'
nick = 'sockheadrps'
initial_channels = ['sockheadrps']
prefix = '!'


discord_link = r'https://discord.gg/zar9q45'
time_com_used = time.time()
time_discord_used = time.time()
time_def_mess_used = time.time()

default_mess_interval = 5


def playSound():
    print("We're simulating a play sound, woohoo!")

def makeRequest(dict, path):
    host = "http://localhost:8000/"
    url = host + path
    r = requests.post(url, json=dict)
    print(r.status_code, r.reason)

def tts_speak(text):
    for line in text:
        txt = text[:int(maxChars)]
        tts = gTTS(text=txt, lang="en", slow=False)
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove("voice.mp3")
        break

dirr = r'C:\Users\rpski\Beaux44\BaxterAndFriends\Sounds'
def listDir(dirr):
    commandList = []
    fileNames = os.listdir(dirr)
    for fileName in fileNames:
        fileName = fileName[:-4]
        commandList.append(fileName)
    return commandList
play_sound_commands = listDir(dirr)
print(play_sound_commands)

class client(Client):
    def __init__(self):
        super().__init__(irc_token=irc_token, client_id=client_id,
                         nick=nick, prefix=prefix,
                         initial_channels=initial_channels)


    async def get_chatters(self, channel: str):
        await client.get_followers(channel)


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=prefix,
                         initial_channels=initial_channels)


    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')



    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)



    # Commands use a decorator...
    @commands.command(name='play')
    async def play_command(self, ctx):
        global play_sound_commands, sounds_to_play, time_com_used, dir
        # print(dir(ctx))
        com = ctx.content[6:]
        if com in play_sound_commands and time.time() - time_com_used < 10:
            print("command found!")
            await ctx.send(f'Hello {ctx.author.name}, commands on cooldown!')
        if com in play_sound_commands and time.time() - time_com_used > 10:
            time_com_used = time.time()
            playsound.playsound(dir + "\\" + com.lower() + '.mp3')
            await ctx.send(f'{ctx.author.name}, command playing {ctx.content}')
        elif com not in play_sound_commands:
            print('invalid command received')
            print(play_sound_commands)
            await ctx.send(f'Hello {ctx.author.name}, command was not found!')


    @commands.command(name='discord')
    async def discord_command(self, ctx):
        global time_discord_used, discord_link
        if time.time() - time_discord_used < 60:
            print("Discord Cooldown")
        if time.time() - time_discord_used > 60:
            time_discord_used = time.time()
            await ctx.send(f'{ctx.author.name}, join us on discord {discord_link}')

async def main():
    get_the_followers = loop.create_task(asyncio.run(twitch_client.get_followers('sockheadrps')))
    print(get_the_followers)
    await asyncio.wait(get_the_followers)

#
# if __name__ == "__main__":
#     print('main')
#     try:
#         twitch_client = Client()
#         loop = asyncio.get_event_loop()
#         loop.set_debug(1)
#         fllwers = loop.run_until_complete(main())
#         print(fllwers)
#         # asyncio.run(twitch_client.get_followers('sockheadrps'))
#     except Exception as e:
#         print(e)


bot = Bot()
bot.run()
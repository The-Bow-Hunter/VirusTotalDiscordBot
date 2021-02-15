import json
from asyncio import sleep
from base64 import urlsafe_b64encode
from pprint import pformat

import discord
from virustotal_python import Virustotal, virustotal

print("starting up url tester unit")
try:
    with open("Config.json", "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("Config.json", "w") as f:
        json.dump({'Discord_Bot_Token': 'YOURTOKEN', 'VirusTotalToken': 'YOURTOKEN',
                   'YourDiscordId': '0', 'Prefix': '&'}, f)
    raise Exception("Missing Config.json. I added it, please fill it out yourself! (Intended at first excecution)")

print("url tester unit loaded with key " + CONFIG['VirusTotalToken'])
vtotal = Virustotal(API_KEY=CONFIG['VirusTotalToken'], API_VERSION="v3")


async def get_url_embed(url: str, ctx):
    print(url)
    embed = discord.Embed(title="VirusTotalBot URL Check",
                          description="Information about " + url,
                          color=discord.Colour.red())
    embed.set_author(name=str(ctx.author))
    try:
        # See https://github.com/dbrennand/virustotal-python
        print("check1")
        resp = vtotal.request("urls", data={"url": url}, method="POST")
        print("check2")
        await sleep(12)  # This is supoptimal but seems to be necessary in order of ensuring that the url gets testet
        print("check3")
        url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
        analysis_resp = vtotal.request(f"urls/{url_id}")
        last_analysis_stats = ""
        for i in analysis_resp.data['attributes']['last_analysis_stats'].keys():
            last_analysis_stats = last_analysis_stats + "\n" + i + ": " + str(
                analysis_resp.data['attributes']['last_analysis_stats'][i])

        embed.add_field(name="Last Analysis stats", value=last_analysis_stats, inline=True)
        embed.add_field(name="reputation score", value=str(analysis_resp.data['attributes']["reputation"]), inline=True)
        votes = ""
        for i in analysis_resp.data['attributes']['total_votes'].keys():
            votes = votes + "\n" + i + ": " + str(analysis_resp.data['attributes']['total_votes'][i])
        embed.add_field(name="votes", value=votes, inline=True)
        embed.add_field(name="Times submitted", value=str(analysis_resp.data['attributes']['times_submitted']))
        embed.add_field(name="trackers", value=pformat(analysis_resp.data['attributes']['trackers']))

    except virustotal.VirustotalError:
        print("An Error occured trying to handle " + url)
        embed = discord.Embed(title="VirusTotalBot Url Check",
                              description="Information about " + url,
                              color=discord.Colour.red())
        embed.add_field(name="Results", value="Something went wrong, most commonly is that it is not an working domain")

    finally:
        return embed
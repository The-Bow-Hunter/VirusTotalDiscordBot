from asyncio import sleep

from discord.ext import commands

from Cogs import settings
from Utils.file_tester import get_file_embed


class FileListener(commands.Cog, name="Server File Listener"):
    def __init__(self, b):
        self.b = b
        print("File Listener sucessfully added to bot!")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.id == self.b.user.id:
            pass
        elif (not settings.bottest) and ctx.author.bot:
            pass
        elif str(ctx.channel.type) != "private" and len(ctx.attachments) > 0:
            attachments: list = ctx.attachments.copy()
            for i in attachments:
                ignored = False
                for a in settings.ignorfiles:
                    if i.content_type.startswith(a):
                        ignored = True
                if ignored:
                    attachments.remove(i)
            if len(attachments) > 0:
                await ctx.reply("🛑‼⚠️⚠️⚠️️WARNING⚠️⚠️⚠️‼️🛑\n Do never trust any files! Even if you think you know "
                                "the file is safe it might still harm your pc! "
                                "I will run a short test over it but cant ensure anything.\n"
                                "This test can take some time if i do not know the file")
                for i in ctx.attachments:
                    msgn = await ctx.reply("Stand by...")
                    await msgn.edit(content=None, embed=await get_file_embed(i, ctx))
                    await sleep(30)

import discord

import Cogs.settings as settings

helpembed = discord.Embed(title="VirusTotalBot",
                          description="This Bot checks suspicous links and files in all "
                                      "hannels he is in and flags them",
                          color=settings.helpembedcolour)
helpembed.set_author(name="Tom Mucke")
helpembed.add_field(name="About",
                    value="This is an self hosted bot whichs code is provided on Github (see github command). "
                          "Please note that it uses Virus Total to scan your files/urls so do not "
                          "send any personal critical files in a channel it can read!", inline=True)
helpembed.set_footer(text="Virus Total Bot by TM#5784. This is a public available bot on Github")

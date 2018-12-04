import time
import discord
import asyncio
import random

from cogs.utils.db import give_points
from cogs.utils.util import get_random_embed_color

class SantaEvent(object):

    GUILD_ID = 390134592507609088   # 244998983112458240
    ROLE_ID = 476719309901791232    # 518971059756859393
    EMOJI = '🎁'
    COOLDOWN = 25
    CHANCE = 100
    WAIT_FOR = 7
    SANTA_GIF = "https://media1.giphy.com/media/3oriNS6RGNct2MZWJq/giphy.gif"

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.role = None
        self.time = time.time()
        self.bot.loop.create_task(self.fetch_objects())

    async def fetch_objects(self):
        await self.bot.wait_until_ready()
        self.guild = self.bot.get_guild(self.GUILD_ID)
        self.role = discord.utils.get(self.guild.roles, id=self.ROLE_ID)

    async def __local_check(self, ctx):
        return ctx.guild.id == self.GUILD_ID

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.attachments != []:
            return
        if message.guild.id != self.GUILD_ID:
            return
        if time.time() - self.time <= self.COOLDOWN:
            return

        if random.randint(1, 100) <= self.CHANCE:
            await message.add_reaction(self.EMOJI)
            await asyncio.sleep(self.WAIT_FOR)
            """for r in message.reactions:
                if r.emoji == self.EMOJI:
                    reaction = r
                else:
                    reaction = None"""
            reaction = message.reactions[0]
            members = []
            role_members = []
            async for m in reaction.users():
                if m.id == self.bot.user.id:
                    pass
                elif self.role not in m.roles:
                    role_members.append(m)
                else:
                    members.append(m)
            
            await message.clear_reactions()

            points_common = random.choice(range(50, 61))
            points_uncommon = random.choice(range(61, 101))
            points_rare = random.choice(range(101, 200))
            points_leg = random.choice(range(200, 301))

            try:
                winner = random.choice(role_members)
                await winner.add_roles(self.role, reason="Gift from TAD's Santa Lil Neko")
                winner_points = random.choice([points_common]*40+[points_uncommon]*30+[points_rare]*20+[points_leg]*10)
                await give_points(str(message.guild.id), str(winner.id), winner_points)
                role_members.remove(winner)
                embed = discord.Embed(title=f"{self.EMOJI} Gifts for you!", colour=get_random_embed_color())
                embed.set_footer(text=f"Congrats {winner.name}!", icon_url=winner.avatar_url)
                embed.set_author(name="Santa Neko", icon_url=self.SANTA_GIF) 
                description = f"🤶    __**{winner.name}    🏆 {self.role.mention} and +{winner_points} cosmos points.__**\n\n"
            except:
                pass
            members += role_members
            if not members:
                return
            for m in members:
                m_points = random.choice([points_common]*80+[points_uncommon]*15+[points_rare]*3+[points_leg]*2)
                await give_points(str(message.guild.id), str(m.id), m_points)
                description += f"🤶    {m.name}    +{m_points} cosmos points.\n"
            embed.description = description
            await message.channel.send(embed=embed)
            self.time = time.time()


def setup(bot):
    bot.add_cog(SantaEvent(bot))

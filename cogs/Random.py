from discord.ext import commands


class RandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == "Carl-bot":
            if "father" in message.content.lower():
                await message.channel.send('Fuck you Im father now')
            elif "mhm" in message.content.lower():
                await message.channel.send('mhm fuck you too')
            elif "shush" in message.content.lower():
                await message.channel.send('shut up')
            elif "we do not say that." in message.content.lower():
                await message.channel.send('we do say that here')
            elif "need me" in message.content.lower():
                await message.channel.send('No Im father they need me here')
            elif "cool" in message.content.lower():
                await message.channel.send(f'{message.content.lower()} I might agree with this one')
            else:
                await message.channel.send(f'{message.content.lower()}\n~ not father')

async def setup(bot):
    await bot.add_cog(RandomCog(bot))
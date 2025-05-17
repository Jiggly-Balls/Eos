import os
import logging
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from .._checks import is_master_guild, is_admin


logger = logging.getLogger(__name__)


def embed_info(message):
    """
    Embedding for things you cant do.
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


class AdminEmergencey(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @is_master_guild()
    @is_admin()
    @commands.hybrid_command()
    async def lockdown(self, interaction: discord.Interaction):
        await interaction.response.defer()
        logger.warning(f"{interaction.guild.name} is going into lockdown mode!")
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(interaction.guild.default_role, send_messages=False)
            await channel.send(f"***{channel.name} is now in lockdown.***")
        await interaction.followup.send(f"{interaction.guild.name} is now in lockdown. When ready, use **unlock**")

    @is_master_guild()
    @is_admin()
    @commands.hybrid_command()
    async def unlock(self, interaction: discord.Interaction):
        await interaction.response.defer()
        logger.warning(f"{interaction.guild.name} is coming out of lockdown mode!")
        for channel in interaction.guild.text_channels:
            await channel.set_permissions(interaction.guild.default_role, send_messages=None)
            await channel.send(f"***{channel.name} has been unlocked.***")
        await interaction.followup.send(f"{interaction.guild.name} is now unlocked.")

    @lockdown.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to lock down the server. The staff has been notified."))

    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.channel.send(embed=embed_info(
                f"{ctx.author.mention}, you dont have permission to unlock the server. The staff has been notified."))


async def setup(bot) -> None:
    """
    required.
    """
    await bot.add_cog(AdminEmergencey(bot))

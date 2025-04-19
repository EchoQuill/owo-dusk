import pkg_resources
import sys

print(f"Python version: {sys.version}")
print("\nInstalled packages:")
for pkg in pkg_resources.working_set:
    if "discord" in pkg.key:
        print(f"{pkg.key}=={pkg.version}")

try:
    import discord
    print(f"\nDiscord.py version: {discord.__version__}")
    
    from discord.ext import commands
    
    # Test creating Bot with intents
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    print("Successfully created Bot instance")
    
except Exception as e:
    print(f"Error: {e}") 
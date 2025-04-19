import traceback
import sys
import os

try:
    # Coba import dan tampilkan versi
    print("Importing discord...")
    import discord
    from discord.ext import commands
    print(f"Discord version: {discord.__version__}")
    
    # Memeriksa keberadaan intents
    print("Checking for Intents...")
    if hasattr(discord, 'Intents'):
        print("Intents exists in discord module")
        intents = discord.Intents.default()
        print(f"Default intents: {intents}")
        
        # Coba buat bot
        print("Creating bot...")
        bot = commands.Bot(command_prefix="!", intents=intents)
        print("Bot created successfully")
    else:
        print("No Intents found in discord module")
except Exception as e:
    print(f"Error: {e}")
    print("\nTraceback:")
    traceback.print_exc()
    
# Cek versi pip
print("\nRunning pip list...")
os.system(f"{sys.executable} -m pip list | findstr discord") 
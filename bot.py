import discord
from discord import app_commands
from discord.ext import commands
import json
import os
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

# Initialize intents and bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# File path to store character data
CHARACTER_FILE = "characters.json"

# Function to load characters from the file
def load_characters():
    if not os.path.exists(CHARACTER_FILE):
        return []
    with open(CHARACTER_FILE, "r") as f:
        return json.load(f)

# Function to save characters to the file
def save_characters(data):
    with open(CHARACTER_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Event handler to sync commands when bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync the updated commands with Discord
    print(f"Logged in as {bot.user}")

# List of possible gems (for autocomplete and choices)
GEM_CHOICES = [
    "yellow", "green", "blue", "purple", "black", "red", "heal", "protect", "reinforce", "trap"
]

# /add command: Adds a character with its gems
@bot.tree.command(name="add")
@app_commands.describe(name="Character name", gems="Comma-separated list of gems")
async def add(interaction: discord.Interaction, name: str, gems: str):
    # Load existing characters
    characters = load_characters()

    # Process and clean up the gems input
    gem_list = [g.strip().lower() for g in gems.split(",")]

    # Create new character data
    new_char = {
        "name": name,
        "gems": gem_list
    }

    # Append to the characters list and save to the file
    characters.append(new_char)
    save_characters(characters)

    # Send confirmation message
    await interaction.response.send_message(f"✅ Added **{name}** with gems `{', '.join(gem_list)}`")

# /find command: Finds characters based on gems
@bot.tree.command(name="find")
@app_commands.describe(gems="Comma-separated list of gems")
async def find(interaction: discord.Interaction, gems: str = ""):
    # Process and clean up the gems query input
    gems_query = [g.strip().lower() for g in gems.split(",") if g] if gems else []

    # Load all characters
    characters = load_characters()
    results = []

    # Search for characters that match the gem criteria
    for char in characters:
        if all(g in char["gems"] for g in gems_query):
            results.append(f"**{char['name']}** – Gems: {', '.join(char['gems'])}")

    # Send the results or a no match message
    if results:
        await interaction.response.send_message("\n".join(results))
    else:
        await interaction.response.send_message("No characters found matching that criteria.")

# Autocomplete for the 'gems' parameter
@add.autocomplete("gems")
async def gems_autocomplete(interaction: discord.Interaction, current: str):
    # Return suggestions that match the current input (autocomplete behavior)
    return [
        app_commands.Choice(name=g, value=g) for g in GEM_CHOICES if g.startswith(current.lower())
    ]






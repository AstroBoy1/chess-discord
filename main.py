import requests
import chess
import chess.svg
import chess.pgn
from io import StringIO, BytesIO
import cairosvg
import discord
from discord.ext import commands, tasks  # Import tasks for background tasks
import os
from dotenv import load_dotenv
from discord.utils import get  # Import get utility from discord

#load_dotenv()

# Discord bot setup
TOKEN = os.getenv('TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.members = True  # Allows bot to track member joins
intents.dm_messages = True  # Allows bot to receive DMs
intents.message_content = True  # Allows bot to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    post_daily_puzzle.start()  # Start the background task when the bot is ready

@tasks.loop(hours=24)  # Run this task every 24 hours
async def post_daily_puzzle():
    for guild in bot.guilds:  # Iterate over all guilds the bot is connected to
        puzzles_channel = get(guild.channels, name="puzzles")  # Find the 'puzzles' channel in the guild

        if puzzles_channel:
            await fetch_and_post_puzzle(puzzles_channel)
        else:
            print(f"No 'puzzles' channel found in guild {guild.name}. Skipping.")

@post_daily_puzzle.before_loop
async def before_post_daily_puzzle():
    await bot.wait_until_ready()  # Wait until the bot is ready before starting the task

@bot.command(name="daily_puzzle")
async def daily_puzzle(ctx):
    puzzles_channel = get(ctx.guild.channels, name="puzzles")  # Find the 'puzzles' channel in the current guild

    if puzzles_channel:
        await fetch_and_post_puzzle(puzzles_channel)
    else:
        await ctx.send("No 'puzzles' channel found in this server. Please create one.")

async def fetch_and_post_puzzle(channel):
    """
    Fetches the daily puzzle from Lichess and posts it to the specified channel.

    Args:
        channel (discord.TextChannel): The channel where the puzzle will be posted.
    """
    try:
        # Step 1: Get the daily puzzle
        response = requests.get("https://lichess.org/api/puzzle/daily")
        data = response.json()

        # Step 2: Extract the puzzle information
        pgn = data['game']['pgn']
        moves = data['puzzle']['solution']

        # Step 3: Parse the PGN and display the board position
        pgn_io = StringIO(pgn)
        game = chess.pgn.read_game(pgn_io)
        board = game.board()

        # Apply the moves from the PGN to reach the puzzle position
        for move in game.mainline_moves():
            board.push(move)

        # Determine whose turn it is
        turn = "White" if board.turn else "Black"

        # Generate the board as an SVG
        svg_data = chess.svg.board(board=board, flipped=not board.turn)

        # Convert the SVG to PNG
        png_data = BytesIO()
        cairosvg.svg2png(bytestring=svg_data, write_to=png_data)
        png_data.seek(0)

        # Send the PNG image and PGN to the channel
        await channel.send(file=discord.File(png_data, "daily_puzzle.png"))
        await channel.send(f"It is {turn}'s move for today's puzzle!")
    except Exception as e:
        print(f"Failed to fetch or post the puzzle: {e}")
        if isinstance(channel, discord.TextChannel):
            await channel.send(f"An error occurred while fetching the puzzle: {e}")

# Run the bot
bot.run(TOKEN)

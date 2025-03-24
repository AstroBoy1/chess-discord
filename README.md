# Chess Discord Bot

A Discord bot that posts daily chess puzzles from [Lichess](https://lichess.org) in a dedicated channel. The bot can also respond to user commands to fetch puzzles on demand.

---

## Features
- Automatically posts daily chess puzzles in a `#puzzles` channel.
- Displays the chessboard and PGN for the puzzle.
- Indicates whose turn it is (White or Black).
- Supports multiple servers with a dedicated `puzzles` channel in each.
- Allows users to fetch the puzzle manually using a command.

---
## Hosting
Just upload the files to a server!

## Local Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/discord_chess.git
   cd discord_chess
   ```

2. **Create a Conda Environment**:
   ```bash
   conda create -n myenv python=3.10
   conda activate myenv
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```


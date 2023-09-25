import discord
import random
from ayarlar import ayarlar

TOKEN = ayarlar["TOKEN2"]  # Discord Developer Portal'dan alınan bot tokenı
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Oyuncuların tahtalarını depolamak için sözlük
player_boards = {}

# Oyuncuların gemilerini saklamak için sözlük
player_ships = {}

# Oyun durumlarını saklamak için sözlük
game_states = {}

# Amiral Battı oyunu için tahta oluştur
def create_board():
    board = []
    for _ in range(5):
        board.append(["O"] * 5)
    return board

# Rastgele gemi yerleştir
def place_ship(board):
    ship_row = random.randint(0, 4)
    ship_col = random.randint(0, 4)
    board[ship_row][ship_col] = "S"
    return (ship_row, ship_col)

# Tahtayı görüntüle
def print_board(board):
    return "\n".join([" ".join(row) for row in board])

# Oyunu başlat
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + 'start'):
        player = message.author
        if player in game_states and game_states[player] == "playing":
            await message.channel.send("Zaten bir oyun oynanıyor.")
        else:
            board = create_board()
            player_boards[player] = board
            ship_location = place_ship(board)
            player_ships[player] = ship_location
            game_states[player] = "playing"
            await message.channel.send(f'Amiral Battı oyunu başladı! İlk hamlenizi yapın.\n{print_board(board)}')

    elif message.content.startswith(PREFIX + 'shoot'):
        player = message.author
        if player in game_states and game_states[player] == "playing":
            try:
                parts = message.content.split()
                if len(parts) != 3:
                    await message.channel.send("Geçersiz bir hamle girdiniz. Örnek: `!shoot 3 4`")
                else:
                    row = int(parts[1])
                    col = int(parts[2])
                    if row < 0 or row >= 5 or col < 0 or col >= 5:
                        await message.channel.send("Geçersiz bir hedef girdiniz. Satır ve sütun 0 ile 4 arasında olmalıdır.")
                    else:
                        board = player_boards[player]
                        if board[row][col] == "X":
                            await message.channel.send("Bu hedefi zaten vurdunuz.")
                        elif board[row][col] == "S":
                            await message.channel.send("Tebrikler, gemiyi vurdunuz!")
                            game_states[player] = "finished"
                        else:
                            board[row][col] = "X"
                            await message.channel.send(f'Hamlenizi yaptınız!\n{print_board(board)}')
            except ValueError:
                await message.channel.send("Geçersiz bir hamle girdiniz. Örnek: `!shoot 3 4`")
        else:
            await message.channel.send("Oyun başlamadı. `!start` komutuyla başlatın.")

client.run(ayarlar["TOKEN2"])

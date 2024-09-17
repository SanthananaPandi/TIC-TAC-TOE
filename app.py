from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

Board = ["_","_","_","_","_","_","_","_","_"]
CurrentPlayer = "X"
winner = None
gamerunning = True

# Function to print the game board (for testing)
def printBoard(Board):
    print(Board[0] + " | " + Board[1] + " | " + Board[2])
    print("---------")
    print(Board[3] + " | " + Board[4] + " | " + Board[5])
    print("---------")
    print(Board[6] + " | " + Board[7] + " | " + Board[8])

# Function to check for a horizontal win
def checkHorizontle(Board):
    global winner
    if Board[0] == Board[1] == Board[2] and Board[1] != "_":
        winner = Board[0]
        return True
    elif Board[3] == Board[4] == Board[5] and Board[3] != "_":
        winner = Board[3]
        return True
    elif Board[6] == Board[7] == Board[8] and Board[6] != "_":
        winner = Board[6]
        return True
    return False

# Function to check for a vertical win
def checkRow(Board):
    global winner
    if Board[0] == Board[3] == Board[6] and Board[0] != "_":
        winner = Board[0]
        return True
    elif Board[1] == Board[4] == Board[7] and Board[1] != "_":
        winner = Board[1]
        return True
    elif Board[2] == Board[5] == Board[8] and Board[2] != "_":
        winner = Board[2]
        return True
    return False

# Function to check for a diagonal win
def checkdiagonal(Board):
    global winner
    if Board[0] == Board[4] == Board[8] and Board[0] != "_":
        winner = Board[0]
        return True
    elif Board[2] == Board[4] == Board[6] and Board[2] != "_":
        winner = Board[2]
        return True
    return False

# Function to check for a tie
def checkTie(Board):
    global gamerunning
    if "_" not in Board:
        gamerunning = False
        return True
    return False

# Check if there is a winner
def checkwin():
    if checkdiagonal(Board) or checkHorizontle(Board) or checkRow(Board):
        return True
    return False

# Switch player
def switchplayer():
    global CurrentPlayer
    if CurrentPlayer == "X":
        CurrentPlayer = "O"
    else:
        CurrentPlayer = "X"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global Board, CurrentPlayer, winner, gamerunning

    data = request.get_json()
    move_index = data['index']

    # Update board if valid move
    if Board[move_index] == "_" and gamerunning:
        Board[move_index] = CurrentPlayer
        if checkwin():
            gamerunning = False
            return jsonify({'status': 'win', 'winner': winner})
        if checkTie(Board):
            return jsonify({'status': 'tie'})
        switchplayer()
        return jsonify({'status': 'continue', 'board': Board, 'currentPlayer': CurrentPlayer})
    else:
        return jsonify({'status': 'invalid'})

@app.route('/restart', methods=['POST'])
def restart():
    global Board, CurrentPlayer, winner, gamerunning
    Board = ["_","_","_","_","_","_","_","_","_"]
    CurrentPlayer = "X"
    winner = None
    gamerunning = True
    return jsonify({'status': 'reset', 'board': Board, 'currentPlayer': CurrentPlayer})

if __name__ == '__main__':
    app.run(debug=True)

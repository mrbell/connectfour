from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from src.board import Board
from src.player import RandomPlayer
from src.basic_ai import AIPlayer
import numpy as np
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

PLAYER_TYPES = {
    'human': None,  # Human moves via web UI
    'random': RandomPlayer,
    'ai': AIPlayer
}

AI_DEPTH = 4

# Helper to serialize the board state for the frontend
def board_to_dict(board):
    return {
        'state': board.state.tolist(),
        'curr_player': board.curr_player,
        'nrow': board.NROW,
        'ncol': board.NCOL
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    p1 = request.form.get('p1')
    p2 = request.form.get('p2')
    board = Board()
    session['board'] = board.state.tolist()
    session['curr_player'] = board.curr_player
    session['p1_type'] = p1
    session['p2_type'] = p2
    session['ai_depth'] = AI_DEPTH
    return redirect(url_for('game'))

@app.route('/game')
def game():
    board = Board()
    board.state = np.array(session['board'])
    board.curr_player = session['curr_player']
    # Pass player types to the template
    p1_type = session.get('p1_type', 'human')
    p2_type = session.get('p2_type', 'human')
    return render_template('game.html', board=board_to_dict(board), p1_type=p1_type, p2_type=p2_type)

@app.route('/move', methods=['POST'])
def move():
    col = int(request.json['col'])
    board = Board()
    board.state = np.array(session['board'])
    board.curr_player = session['curr_player']
    curr_player = board.curr_player
    ptype = session['p1_type'] if curr_player == Board.P1 else session['p2_type']
    if ptype == 'human':
        if not board.is_legal_move(col):
            return jsonify({'error': 'Illegal move'}), 400
        board.make_move(col)
    else:
        # AI or random
        if ptype == 'ai':
            player = AIPlayer(curr_player, session['ai_depth'])
        else:
            player = RandomPlayer(curr_player)
        move = player.get_move(board)
        board.make_move(move)
    session['board'] = board.state.tolist()
    session['curr_player'] = board.curr_player
    winner = board.check_for_victory()
    return jsonify({'board': board_to_dict(board), 'winner': winner})

@app.route('/ai_move', methods=['POST'])
def ai_move():
    board = Board()
    board.state = np.array(session['board'])
    board.curr_player = session['curr_player']
    curr_player = board.curr_player
    ptype = session['p1_type'] if curr_player == Board.P1 else session['p2_type']
    if ptype == 'ai':
        player = AIPlayer(curr_player, session['ai_depth'])
    else:
        player = RandomPlayer(curr_player)
    move = player.get_move(board)
    board.make_move(move)
    session['board'] = board.state.tolist()
    session['curr_player'] = board.curr_player
    winner = board.check_for_victory()
    return jsonify({'board': board_to_dict(board), 'winner': winner})

if __name__ == '__main__':
    app.run(debug=True)

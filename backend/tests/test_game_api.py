# backend/tests/test_game_api.py

import pytest
# from flask_testing import TestCase
from app import build_app, db  # Adjust the import according to your project structure

import pytest
from app import build_app, db


@pytest.fixture(scope='module')
def test_client():
    app = build_app(testing=True)
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


def register_and_login_user(test_client, username, password):
    test_client.post('/auth/register', json={'username': username, 'password': password})
    response = test_client.post('/auth/login', json={'username': username, 'password': password})
    assert response.status_code == 200
    assert response.json['token'] is not None
    assert response.json['id'] is not None
    return response


def test_game_flow(test_client, init_database):
    # 1. Registration and Login for player1 and player2
    response_player1 = register_and_login_user(test_client, 'player1', 'password1')
    token1 = response_player1.json['token']
    response_player2 = register_and_login_user(test_client, 'player2', 'password2')
    token2 = response_player2.json['token']
    assert token1 != token2

    # 2. player1 creates a new game
    start_response = test_client.get('/api/start', headers={'Authorization': f'Bearer {token1}'})
    assert start_response.status_code == 200
    game_data = start_response.json
    game_id = game_data['gameId']
    assert isinstance(game_id, int)

    # 3. player2 joins the game
    join_response = test_client.post('/api/join', json={'gameId': game_id},
                                     headers={'Authorization': f'Bearer {token2}'})
    assert join_response.status_code == 200

    # 4. player1 and player2 make two moves each
    for player_token, moves in zip([token1, token2, token1, token2], [(0, 0), (1, 0), (0, 1), (1, 1)]):
        move_response = test_client.post('/api/move',
                                         json={'row': moves[0], 'col': moves[1], 'gameId': game_id},
                                         headers={'Authorization': f'Bearer {player_token}'})
        assert move_response.status_code == 200
        move_data = move_response.json
        assert move_data['message'] in ['Ruch wykonany pomyślnie.', 'Nieprawidłowy ruch.']

    # Optionally, you can add more assertions here to check the game state after each move


def test_multiple_independent_games(test_client, init_database):
    # Registration and Login for 6 players
    players = [register_and_login_user(test_client, f'player{i}', f'password{i}') for i in range(1, 7)]
    tokens = [player.json['token'] for player in players]

    games = []
    for i in range(0, 6, 2):  # Start 3 games
        # Player i starts a new game
        start_response = test_client.get('/api/start', headers={'Authorization': f'Bearer {tokens[i]}'})
        assert start_response.status_code == 200
        game_data = start_response.json
        game_id = game_data['gameId']
        assert isinstance(game_id, int)

        # Player i+1 joins the game
        join_response = test_client.post('/api/join', json={'gameId': game_id},
                                         headers={'Authorization': f'Bearer {tokens[i+1]}'})
        assert join_response.status_code == 200

        games.append(game_id)

    # Players make moves in their respective games
    for i, game_id in enumerate(games):
        for player_token, moves in zip([tokens[i*2], tokens[i*2+1]], [(0, 0), (1, 0), (0, 1), (1, 1)]):
            move_response = test_client.post('/api/move',
                                             json={'row': moves[0], 'col': moves[1], 'gameId': game_id},
                                             headers={'Authorization': f'Bearer {player_token}'})
            assert move_response.status_code == 200
            move_data = move_response.json
            assert move_data['message'] in ['Ruch wykonany pomyślnie.', 'Nieprawidłowy ruch.']



def test_invalid_move(test_client, init_database):
    response_player1 = register_and_login_user(test_client, 'player1', 'password1')
    token1 = response_player1.json['token']

    start_response = test_client.get('/api/start', headers={'Authorization': f'Bearer {token1}'})
    assert start_response.status_code == 200
    game_data = start_response.json
    game_id = game_data['gameId']
    assert isinstance(game_id, int)
    move_response = test_client.post('/api/move',
                                     json={'row': 19, 'col': 3, 'gameId': game_id},
                                     headers={'Authorization': f'Bearer {token1}'})
    assert move_response.status_code == 400
    move_data = move_response.json
    assert move_data['message'] in ['Ruch wykonany pomyślnie.', 'Nieprawidłowy ruch.']


# def test_game_draw(test_client, user_token):
#     # Start a new game and play moves leading to a draw
#     response = test_client.get('/api/start', headers={'Authorization': f'Bearer {user_token}'})
#     assert response.status_code == 200
#     game_id = response.json['gameId']
#     moves = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (1, 2), (2, 1), (2, 2)]
#     for row, col in moves:
#         response = test_client.post('/api/move', json={'row': row, 'col': col, 'gameId': game_id},
#                                     headers={'Authorization': f'Bearer {user_token}'})
#         assert response.status_code == 200 or (row, col) == moves[-1]
#     assert response.json['message'] == 'Gra zakończona: X'
#
#
# def test_restart_game(test_client, user_token):
#     # Start a new game
#     response = test_client.get('/api/start', headers={'Authorization': f'Bearer {user_token}'})
#     assert response.status_code == 200
#     game_id = response.json['gameId']
#
#     # Make some moves
#     test_client.post('/api/move', json={'row': 0, 'col': 0, 'gameId': game_id},
#                      headers={'Authorization': f'Bearer {user_token}'})
#     test_client.post('/api/move', json={'row': 1, 'col': 1, 'gameId': game_id},
#                      headers={'Authorization': f'Bearer {user_token}'})
#
#     # Reset the game
#     test_client.get(f'/api/reset?gameId={game_id}', headers={'Authorization': f'Bearer {user_token}'})
#
#     # Check if the board is reset
#     response = test_client.get(f'/api/start?gameId={game_id}', headers={'Authorization': f'Bearer {user_token}'})
#     assert all(cell == '' for row in response.json['boardState'] for cell in row)
#
#
# def test_game_over_condition(test_client, user_token):
#     # Start a new game and play a winning combination
#     response = test_client.get('/api/start', headers={'Authorization': f'Bearer {user_token}'})
#     assert response.status_code == 200
#     game_id = response.json['gameId']
#     winning_moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
#
#     for row, col in winning_moves:
#         test_client.post('/api/move', json={'row': row, 'col': col, 'gameId': game_id},
#                          headers={'Authorization': f'Bearer {user_token}'})
#
#     # Attempt to make a move after the game is over
#     response = test_client.post('/api/move', json={'row': 2, 'col': 2, 'gameId': game_id},
#                                 headers={'Authorization': f'Bearer {user_token}'})
#     assert response.status_code == 400
#     assert response.json['error'] == 'Nie można grać w zakończoną grę.'

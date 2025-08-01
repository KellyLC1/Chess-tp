import pandas as pd
import chess
import chess.engine
from prep_data import load_games, pgn_to_csv, fen_to_tensor

pgn_path = 'dataset/lichess_elite_2022-04.pgn'
games = load_games(pgn_path, max_games=100)
print(f"{len(games)} parties chargées.")
 
pgn_to_csv(pgn_path, max_games=100)

# Chemin vers Stockfish
STOCKFISH_PATH = r"C:\Users\keell\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

df = pd.read_csv("chess_positions.csv")
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

evals = []
for fen in df['fen']:
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = info["score"].white().score(mate_score=1000)  
    evals.append(score)

engine.quit()
df['stockfish_eval'] = evals
df.to_csv("chess_positions_evaluated.csv", index=False)
print("Évaluations Stockfish ajoutées au DataFrame'.")
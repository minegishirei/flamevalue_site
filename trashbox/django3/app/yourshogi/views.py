from django.shortcuts import render, redirect
import json
import sys
if '/God' not in sys.path:
    sys.path.append('/God')
from shogi_lib import shogi





def index(request):
    board = shogi.Board()
    board.push_usi('7g7f')
    board.push_usi('3c3d')
    #if board in board.legal_moves:

    #board.push_usi('8h2b+')
    #board.push_usi('4a5b')
    #board.push_usi('B*4b')
    params = {
        "board" : str(board.kif_str()),
        "kifu"  : str(board)
    }
    return render(request, "yourshogi/index.html", params)



def api(request, kifu_str, push_str):
    board = shogi.Board()
    board.push_usi(push_str)

    params = {
        "board" : str(board.kif_str()),
        "kifu"  : str(board)
    }
    return render(request, "yourshogi/api.html", params)






def solution(players, callings):
    player_dict = {}

    # 1. 시작 전에 장부부터 완성 (이름 -> 현재 등수)
    for i in range(len(players)):
        player = players[i]
        player_dict[player] = i

    # 2. 해설진이 부른 이름 처리
    for call in callings:
        idx = player_dict[call]

        prev_player = players[idx - 1]

        players[idx - 1], players[idx] = players[idx], players[idx - 1]

        player_dict[call] = idx - 1
        player_dict[prev_player] = idx

    return players


print(solution(["mumu", "soe", "poe", "kai", "mine"], ["kai", "kai", "mine", "mine"]))

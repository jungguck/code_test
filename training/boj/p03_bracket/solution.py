PAIR = {')': '(', ']': '[', '}': '{'}   # 닫는 괄호 -> 짝이 되는 여는 괄호

t = int(input())
for _ in range(t):
    s = input()
    stack = []
    ok = True
    for ch in s:
        if ch in '([{':
            stack.append(ch)                    # 여는 괄호는 쌓는다
        else:
            if not stack or stack.pop() != PAIR[ch]:
                ok = False                      # 짝이 안 맞거나 닫을 게 없음
                break
    # 다 돌고 스택이 비어있어야 진짜 YES (안 닫힌 게 남아있으면 NO)
    print('YES' if ok and not stack else 'NO')

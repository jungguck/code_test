n = int(input())
add = 6
layer = 1
end = 1

while end < n:
    end += add
    add += 6
    layer += 1

print(layer)

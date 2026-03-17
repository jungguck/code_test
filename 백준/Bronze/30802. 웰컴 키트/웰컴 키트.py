N = int(input())

S, M, L, XL, XXL, XXXL = map(int, input().split())

T, P = map(int, input().split())

tshirts = 0

for size in [S, M, L, XL, XXL, XXXL]:
    tshirts += (size + T - 1) // T

pen_bundle = N // P
pen_single = N % P

print(tshirts)
print(pen_bundle, pen_single)
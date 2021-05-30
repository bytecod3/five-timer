t = 1/1000

for r in range(1, 20):
    c = t / (1.1 * r)
    t_apx = 1.1 * r * c

    if t_apx == t:
        print(r, c, t_apx, sep="\n")
    else:
        continue




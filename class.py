import time 

text = 'shelton is a good boy'
colors = [31, 32, 33, 34, 35, 36, 37]

for i in range(10):
    line = ''
    for idx, char in enumerate(text):
        color_code = colors[(idx + i) % len(colors)]
        line += f'\033[{color_code}m{char}\033[0m'
    print(line)
    time.sleep(0.2)
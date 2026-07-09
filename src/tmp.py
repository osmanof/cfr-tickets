with open("constants.py", "r", encoding="utf-8") as f:
    r = f.read().lower()

with open("constants.py", "w", encoding="utf-8") as file:
    file.write(r)

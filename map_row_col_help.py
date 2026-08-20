from BASE_MAP import BASE_MAP

# 1. Spalten-Skala oben drucken (Zehner- und Einerstellen)
header_zehner = "     " + "".join(str(i // 10) if i % 10 == 0 else " " for i in range(len(BASE_MAP[0])))
header_einer  = "     " + "".join(str(i % 10) for i in range(len(BASE_MAP[0])))

print(header_zehner)
print(header_einer)
print("    +" + "-" * len(BASE_MAP[0]))

# 2. Jede Zeile mit Zeilennummer (row) links drucken
for row_idx, line in enumerate(BASE_MAP):
    print(f"{row_idx:>3} |{line}")
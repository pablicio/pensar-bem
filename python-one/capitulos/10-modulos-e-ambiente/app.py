from precos import com_margem

for p in (8.90, 3.50, 12.00):
    print(f"{p:.2f} -> {com_margem(p):.2f}")

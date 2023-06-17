#Tax Calculator Program
print("WELCOME TO TAX CALCULATOR: UK EDITION")
# Collects User's income and calculates tax bracket
inc = int(input("Enter your yearly income (£): "))
t1 = 0.2 * (inc - 12570)
t2 = 0.4 * (inc - 50270) + 0.2 * (37700)
t3 = 0.45 * (inc - 125140) + 0.4 * (74870) + 0.2 * (37700)
# Calculates taxes and shows after-tax income
if inc <= 12_570:
    atin = inc
    print(f"Your after-tax income is £{int(atin)}")
elif inc <= 50_270 and inc > 12_570:
    atin = inc - t1
    print(f"Your estimated tax bill is £{int(t1)}")
    print(f"Your after-tax income is £{int(atin)}")
elif inc <= 125_140  and inc > 50_270:
    atin = inc - t2
    print(f"Your estimated tax bill is £{int(t2)}")
    print(f"Your after-tax income is £{int(atin)}")
elif inc > 125_140:
    atin = inc - t3
    print(f"Your estimated tax bill is £{int(t3)}")
    print(f"Your after-tax income is £{int(atin)}")
else:
    print("Error in program , Please Retry !!!")

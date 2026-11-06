
# UK Income Tax Calculator (2026-27)

print("WELCOME TO TAX CALCULATOR: UK EDITION")
print("Tax Year: 2026-2027")

# Collect annual income
inc = float(input("Enter your yearly income (£): "))

if inc < 0:
    print("Invalid income. Please enter a positive amount.")

else:
    # Personal Allowance
    personal_allowance = 12570

    # Reduce Personal Allowance by £1 for every £2 above £100,000
    if inc > 100000:
        personal_allowance -= (inc - 100000) / 2

    personal_allowance = max(0, personal_allowance)

    # Calculate taxable income
    taxable_income = max(0, inc - personal_allowance)

    # Calculate tax progressively
    basic_tax = min(taxable_income, 37700) * 0.20

    higher_tax = min(
        max(0, taxable_income - 37700),
        max(0, 125140 - personal_allowance - 37700)
    ) * 0.40

    additional_tax = max(
        0, taxable_income - (125140 - personal_allowance)
    ) * 0.45

    # Total tax and after-tax income
    total_tax = basic_tax + higher_tax + additional_tax
    after_tax_income = inc - total_tax

    # Display results
    print("\n------ TAX CALCULATION ------")
    print(f"Annual Income:       £{inc:,.2f}")
    print(f"Personal Allowance:  £{personal_allowance:,.2f}")
    print(f"Taxable Income:      £{taxable_income:,.2f}")
    print(f"Basic Rate Tax:      £{basic_tax:,.2f}")
    print(f"Higher Rate Tax:     £{higher_tax:,.2f}")
    print(f"Additional Rate Tax: £{additional_tax:,.2f}")
    print("-----------------------------")
    print(f"Total Tax:           £{total_tax:,.2f}")
    print(f"After-Tax Income:    £{after_tax_income:,.2f}")
    print("-----------------------------")

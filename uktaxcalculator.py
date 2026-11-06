
# ============================================================
# UK SALARY & INCOME TAX CALCULATOR
# Tax Year: 2026-2027 (6 April 2026 - 5 April 2027)
# ============================================================

# -------------------- TAX CONSTANTS -------------------------

PERSONAL_ALLOWANCE = 12570
PA_TAPER_START = 100000
PA_TAPER_END = 125140

# England, Wales and Northern Ireland
UK_TAX_BANDS = [
    (37700, 0.20),
    (125140, 0.40),
    (float("inf"), 0.45)
]

# Scotland: bands are taxable income AFTER Personal Allowance
SCOTTISH_TAX_BANDS = [
    (3967, 0.19),
    (16956, 0.20),
    (31092, 0.21),
    (62430, 0.42),
    (125140, 0.45),
    (float("inf"), 0.48)
]

# Employee National Insurance - Category A
NI_PRIMARY_THRESHOLD = 12570
NI_UPPER_LIMIT = 50270
NI_MAIN_RATE = 0.08
NI_UPPER_RATE = 0.02

# Student loan repayment thresholds
STUDENT_LOANS = {
    "1": ("Plan 1", 26900),
    "2": ("Plan 2", 29385),
    "4": ("Plan 4", 33795),
    "5": ("Plan 5", 25000)
}

STUDENT_LOAN_RATE = 0.09
POSTGRADUATE_THRESHOLD = 21000
POSTGRADUATE_RATE = 0.06


# -------------------- HELPER FUNCTIONS ----------------------

def calculate_progressive_tax(income, tax_bands):
    """Calculate tax progressively across income bands."""

    tax = 0
    previous_limit = 0
    breakdown = []

    for upper_limit, rate in tax_bands:

        taxable_in_band = min(
            max(0, income - previous_limit),
            upper_limit - previous_limit
        )

        band_tax = taxable_in_band * rate
        tax += band_tax

        if taxable_in_band > 0:
            breakdown.append((taxable_in_band, rate, band_tax))

        previous_limit = upper_limit

        if income <= upper_limit:
            break

    return tax, breakdown


def calculate_personal_allowance(income):
    """Calculate Personal Allowance including the £100k taper."""

    if income <= PA_TAPER_START:
        return PERSONAL_ALLOWANCE

    reduction = (income - PA_TAPER_START) / 2

    return max(0, PERSONAL_ALLOWANCE - reduction)


def calculate_national_insurance(income):
    """Calculate standard employee Class 1 National Insurance."""

    main_band = max(
        0,
        min(income, NI_UPPER_LIMIT) - NI_PRIMARY_THRESHOLD
    )

    upper_band = max(0, income - NI_UPPER_LIMIT)

    main_ni = main_band * NI_MAIN_RATE
    upper_ni = upper_band * NI_UPPER_RATE

    return main_ni + upper_ni, main_ni, upper_ni


def calculate_student_loan(income, plan):
    """Calculate student loan repayment."""

    if plan == "0":
        return 0

    threshold = STUDENT_LOANS[plan][1]

    return max(0, income - threshold) * STUDENT_LOAN_RATE


def calculate_postgraduate_loan(income, has_loan):
    """Calculate postgraduate loan repayment."""

    if not has_loan:
        return 0

    return max(0, income - POSTGRADUATE_THRESHOLD) * POSTGRADUATE_RATE


def get_currency(amount):
    return f"£{amount:,.2f}"


# -------------------- USER INPUT ----------------------------

print("\n" + "=" * 55)
print("          UK SALARY & INCOME TAX CALCULATOR")
print("                   TAX YEAR 2026-27")
print("=" * 55)

try:

    salary = float(input("\nEnter your annual gross salary (£): "))

    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    print("\nSelect your UK region:")
    print("1. England")
    print("2. Wales")
    print("3. Northern Ireland")
    print("4. Scotland")

    region = input("Enter your choice (1-4): ").strip()

    if region not in ("1", "2", "3", "4"):
        raise ValueError("Invalid region selection.")

    if region == "4":
        tax_bands = SCOTTISH_TAX_BANDS
        region_name = "Scotland"
    else:
        tax_bands = UK_TAX_BANDS
        region_names = {
            "1": "England",
            "2": "Wales",
            "3": "Northern Ireland"
        }
        region_name = region_names[region]

    print("\nSelect your student loan plan:")
    print("0. No student loan")
    print("1. Plan 1")
    print("2. Plan 2")
    print("4. Plan 4")
    print("5. Plan 5")

    loan_plan = input("Enter your choice: ").strip()

    if loan_plan not in ("0", "1", "2", "4", "5"):
        raise ValueError("Invalid student loan plan.")

    postgraduate = input(
        "\nDo you have a postgraduate loan? (y/n): "
    ).strip().lower()

    if postgraduate not in ("y", "n"):
        raise ValueError("Please enter y or n.")

    # -------------------- CALCULATIONS ---------------------

    personal_allowance = calculate_personal_allowance(salary)

    taxable_income = max(0, salary - personal_allowance)

    income_tax, tax_breakdown = calculate_progressive_tax(
        taxable_income,
        tax_bands
    )

    national_insurance, main_ni, upper_ni = (
        calculate_national_insurance(salary)
    )

    student_loan = calculate_student_loan(
        salary,
        loan_plan
    )

    postgraduate_loan = calculate_postgraduate_loan(
        salary,
        postgraduate == "y"
    )

    total_deductions = (
        income_tax
        + national_insurance
        + student_loan
        + postgraduate_loan
    )

    take_home = salary - total_deductions

    # -------------------- TAX RATES -------------------------

    effective_tax_rate = (
        total_deductions / salary * 100 if salary > 0 else 0
    )

    # Income tax marginal rate
    marginal_income_rate = 0

    for upper_limit, rate in tax_bands:
        if taxable_income <= upper_limit:
            marginal_income_rate = rate * 100
            break

    # Combined marginal deduction rate
    marginal_ni = (
        NI_MAIN_RATE if salary <= NI_UPPER_LIMIT
        else NI_UPPER_RATE
    ) if salary > NI_PRIMARY_THRESHOLD else 0

    marginal_loan = (
        STUDENT_LOAN_RATE
        if loan_plan != "0"
        and salary > STUDENT_LOANS[loan_plan][1]
        else 0
    )

    marginal_postgrad = (
        POSTGRADUATE_RATE
        if postgraduate == "y"
        and salary > POSTGRADUATE_THRESHOLD
        else 0
    )

    combined_marginal_rate = (
        marginal_income_rate
        + marginal_ni * 100
        + marginal_loan * 100
        + marginal_postgrad * 100
    )

    # -------------------- RESULTS --------------------------

    print("\n" + "=" * 55)
    print("                  TAX SUMMARY")
    print("=" * 55)

    print(f"Region:                 {region_name}")
    print(f"Tax Year:               2026-2027")
    print(f"Gross Annual Salary:    {get_currency(salary)}")
    print(f"Personal Allowance:     {get_currency(personal_allowance)}")
    print(f"Taxable Income:         {get_currency(taxable_income)}")

    print("\n" + "-" * 55)
    print("INCOME TAX BREAKDOWN")
    print("-" * 55)

    for amount, rate, tax in tax_breakdown:
        print(
            f"{rate * 100:5.1f}% on {get_currency(amount):>14}"
            f" = {get_currency(tax)}"
        )

    print(f"\nTotal Income Tax:       {get_currency(income_tax)}")

    print("\n" + "-" * 55)
    print("NATIONAL INSURANCE")
    print("-" * 55)

    print(f"NI at 8%:               {get_currency(main_ni)}")
    print(f"NI at 2%:               {get_currency(upper_ni)}")
    print(f"Total National Insurance: {get_currency(national_insurance)}")

    print("\n" + "-" * 55)
    print("OTHER DEDUCTIONS")
    print("-" * 55)

    if loan_plan != "0":
        print(
            f"{STUDENT_LOANS[loan_plan][0]} repayment: "
            f"{get_currency(student_loan)}"
        )
    else:
        print("Student Loan:           £0.00")

    print(f"Postgraduate Loan:      {get_currency(postgraduate_loan)}")

    print("\n" + "=" * 55)
    print("                  FINAL RESULTS")
    print("=" * 55)

    print(f"Gross Annual Salary:    {get_currency(salary)}")
    print(f"Total Income Tax:       {get_currency(income_tax)}")
    print(f"National Insurance:     {get_currency(national_insurance)}")
    print(f"Student Loan:           {get_currency(student_loan)}")
    print(f"Postgraduate Loan:      {get_currency(postgraduate_loan)}")

    print("-" * 55)

    print(f"Total Deductions:       {get_currency(total_deductions)}")

    print(f"\nAnnual Take-Home Pay:   {get_currency(take_home)}")
    print(f"Monthly Take-Home Pay:  {get_currency(take_home / 12)}")
    print(f"Weekly Take-Home Pay:   {get_currency(take_home / 52)}")

    print("\n" + "-" * 55)

    print(f"Effective Deduction Rate: {effective_tax_rate:.2f}%")
    print(f"Marginal Income Tax Rate: {marginal_income_rate:.2f}%")
    print(f"Combined Marginal Rate:   {combined_marginal_rate:.2f}%")

    print("=" * 55)
    print("       THANK YOU FOR USING THE TAX CALCULATOR!")
    print("=" * 55)

except ValueError as error:
    print(f"\nInput Error: {error}")
    print("Please restart and enter valid information.")

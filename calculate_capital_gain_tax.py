from flask import Flask, request, render_template_string

app = Flask(__name__)

def calculate_taxable_income(capital_gain):
    if capital_gain <= 250000:
        taxable_amount = round(capital_gain * 0.50, 2)
        result = f"Capital gain ({capital_gain}) is less than or equal to 250000. Taxable amount is {taxable_amount}<br>"
    else:
        taxable_amount_first = round(250000 * 0.50, 2)
        taxable_amount_rest = round((capital_gain - 250000) * (2/3), 2)
        taxable_amount = round(taxable_amount_first + taxable_amount_rest, 2)
        result = f"Capital gain ({capital_gain}) is more than 250000. Taxable amount for first 250000 is {taxable_amount_first} and for the rest is {taxable_amount_rest}. Total taxable amount is {taxable_amount}<br>"
    return taxable_amount, result

def calculate_bc_tax(taxable_income):
    brackets = [47937, 47938, 14101, 23588, 47568, 71420, float('inf')]
    rates = [0.0506, 0.077, 0.105, 0.1229, 0.147, 0.168, 0.205]

    tax = 0
    remaining_income = taxable_income
    result = ""

    for bracket, rate in zip(brackets, rates):
        if remaining_income > bracket:
            tax_segment = round(bracket * rate, 2)
            tax += tax_segment
            remaining_income -= bracket
            result += f"Bracket: {bracket}, Rate: {rate}, Tax segment: {tax_segment}, Remaining income: {remaining_income}<br>"
        else:
            tax_segment = round(remaining_income * rate, 2)
            tax += tax_segment
            result += f"Bracket: {bracket}, Rate: {rate}, Tax segment: {tax_segment}, Remaining income: 0<br>"
            break

    tax = round(tax, 2)
    result += f"Total BC tax for taxable income {taxable_income} is {tax}<br>"
    return tax, result

def calculate_federal_tax(taxable_income):
    brackets = [55867, 55866, 61472, 73547, float('inf')]
    rates = [0.15, 0.205, 0.26, 0.29, 0.33]

    tax = 0
    remaining_income = taxable_income
    result = ""

    for bracket, rate in zip(brackets, rates):
        if remaining_income > bracket:
            tax_segment = round(bracket * rate, 2)
            tax += tax_segment
            remaining_income -= bracket
            result += f"Bracket: {bracket}, Rate: {rate}, Tax segment: {tax_segment}, Remaining income: {remaining_income}<br>"
        else:
            tax_segment = round(remaining_income * rate, 2)
            tax += tax_segment
            result += f"Bracket: {bracket}, Rate: {rate}, Tax segment: {tax_segment}, Remaining income: 0<br>"
            break

    tax = round(tax, 2)
    result += f"Total federal tax for taxable income {taxable_income} is {tax}<br>"
    return tax, result

def calculate_total_tax(taxable_income):
    bc_tax, bc_result = calculate_bc_tax(taxable_income)
    federal_tax, federal_result = calculate_federal_tax(taxable_income)
    total_tax = round(bc_tax + federal_tax, 2)
    result = f"Total tax for taxable income {taxable_income} is {total_tax}<br>"
    return total_tax, bc_result + federal_result + result

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        capital_gain = float(request.form['capital_gain'])

        capital_gain_person1 = capital_gain / 2
        capital_gain_person2 = capital_gain / 2

        taxable_income_person1, result1 = calculate_taxable_income(capital_gain_person1)
        taxable_income_person2, result2 = calculate_taxable_income(capital_gain_person2)

        total_tax_person1, total_result1 = calculate_total_tax(taxable_income_person1)
        total_tax_person2, total_result2 = calculate_total_tax(taxable_income_person2)

        result += f"<b>Person 1:</b><br>"
        result += result1
        result += total_result1
        result += f"<b>The taxable income to be included in the calculation of income tax is: ${taxable_income_person1:.2f}</b><br>"
        result += f"<b>The total tax to be paid is: ${total_tax_person1:.2f}</b><br><br>"

        result += f"<b>Person 2:</b><br>"
        result += result2
        result += total_result2
        result += f"<b>The taxable income to be included in the calculation of income tax is: ${taxable_income_person2:.2f}</b><br>"
        result += f"<b>The total tax to be paid is: ${total_tax_person2:.2f}</b><br>"

    return render_template_string('''
        <!doctype html>
        <title>Capital Gain Tax Calculator</title>
        <h1>Enter Capital Gain</h1>
        <form method=post>
          <label for="capital_gain">Capital Gain Amount:</label>
          <input type="number" step="0.01" name="capital_gain" required>
          <input type=submit value=Calculate>
        </form>
        <h2>BC Tax Brackets</h2>
        <table border="1">
            <tr><th>Income Bracket</th><th>Tax Rate</th></tr>
            <tr><td>Up to $47,937</td><td>5.06%</td></tr>
            <tr><td>$47,938 to $95,875</td><td>7.70%</td></tr>
            <tr><td>$95,876 to $117,976</td><td>10.50%</td></tr>
            <tr><td>$117,977 to $141,565</td><td>12.29%</td></tr>
            <tr><td>$141,566 to $195,627</td><td>14.70%</td></tr>
            <tr><td>$195,628 to $214,557</td><td>16.80%</td></tr>
            <tr><td>Over $214,557</td><td>20.50%</td></tr>
        </table>
        <h2>Federal Tax Brackets</h2>
        <table border="1">
            <tr><th>Income Bracket</th><th>Tax Rate</th></tr>
            <tr><td>Up to $55,867</td><td>15.00%</td></tr>
            <tr><td>$55,868 to $111,733</td><td>20.50%</td></tr>
            <tr><td>$111,734 to $173,205</td><td>26.00%</td></tr>
            <tr><td>$173,206 to $214,557</td><td>29.00%</td></tr>
            <tr><td>Over $214,557</td><td>33.00%</td></tr>
        </table>
        <p>{{ result|safe }}</p>
    ''', result=result)

if __name__ == "__main__":
    app.run(debug=True)

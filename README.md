# Capital Gain Tax Calculator

This application calculates the capital gain tax for individuals based on provided capital gain amounts. It uses BC and Federal tax brackets to compute the tax.

## Features

- Calculates taxable income from capital gain
- Calculates BC provincial tax
- Calculates Federal tax
- Provides a web interface for input and result display

## Requirements

- Python 3.x
- Flask

## Installation

1. Clone the repository or download the `calculate_capital_gain_tax.py` file.

2. Install the required packages using pip:
    ```bash
    pip install flask
    ```

## Usage

1. Run the application:
    ```bash
    python calculate_capital_gain_tax.py
    ```

2. Open your web browser and go to:
    ```
    http://127.0.0.1:5000/
    ```

3. Enter the capital gain amount and submit to see the calculated tax.

## How it works

- **Taxable Income Calculation**:
  - If the capital gain is less than or equal to 250,000, 50% of it is considered taxable.
  - If the capital gain is more than 250,000, the first 250,000 is taxed at 50% and the rest at 2/3.

- **BC Tax Calculation**:
  - Applies different tax rates to different brackets of the taxable income.

- **Federal Tax Calculation**:
  - Similar to BC tax but with different brackets and rates.

## Example

Enter a capital gain amount and the application will display:

- The taxable income
- The BC tax calculation details
- The Federal tax calculation details
- The total tax to be paid

## License

This project is licensed under the MIT License.

# Rent Receipt Generator

Generate Rent receipts for a given period of time. The script will generate receipts for all the months and years

## Setup

```
pip install -r requirements.txt
python ./main.py
```

## How to use

You only need to change the variables and the script will automatically generate recipts

```
    context = {
        "RENT_MONTH": get_period(year, month),
        "PAYEE_NAME": "Joe Smith",
        "PAID_AMOUNT": "xxxx",
        "PAYMENT_MODE": "Cash",
        "PROPERTY_ADDRESS": "1234 Elm Street, Springfield, IL 62701",
        "LANDLORD_NAME": "John Doe",
        "GENERATED_DATE": datetime.date.today().strftime("%d %B, %Y"),
    }
```

## Output

The script will generate a PDF file for each month and year in the `output` folder

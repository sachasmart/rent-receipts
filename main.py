import calendar
import datetime
import os
import pypandoc
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv

load_dotenv()


def get_period(year, month):
    """Return the period for the given month and year."""
    _, num_days = calendar.monthrange(year, month)
    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, num_days)
    return first_day.strftime("%d %B, %Y") + " to " + last_day.strftime("%d %B, %Y")


def render_rent_receipt(month, year):
    """Render rent receipt using Markdown and convert it to PDF."""
    env = Environment(
        loader=FileSystemLoader("template/"), autoescape=select_autoescape(["md"])
    )
    template = env.get_template("template.md")

    context = {
        "RENT_MONTH": get_period(year, month),
        "PAYEE_NAME": os.getenv("PAYEE_NAME", "Unknown Payee"),
        "PAID_AMOUNT": os.getenv("PAID_AMOUNT", "0"),
        "PAYMENT_MODE": os.getenv("PAYMENT_MODE", "Unknown"),
        "PROPERTY_ADDRESS": os.getenv("PROPERTY_ADDRESS", "Unknown Address"),
        "LANDLORD_NAME": os.getenv("LANDLORD_NAME", "Unknown Landlord"),
        "GENERATED_DATE": datetime.date.today().strftime("%d %B, %Y"),
    }

    output_folder = "output/"
    os.makedirs(output_folder, exist_ok=True)
    month_name = calendar.month_name[month]
    output_md_path = os.path.join(output_folder, f"{month_name} {year}.md")
    output_pdf_path = os.path.join(output_folder, f"{month_name} {year}.pdf")

    with open(output_md_path, "w") as file:
        file.write(template.render(context))

    try:
        pypandoc.convert_file(
            output_md_path,
            "pdf",
            outputfile=output_pdf_path,
            extra_args=["--resource-path=template"],
        )
        print(f"Generated PDF: {output_pdf_path}")
        os.remove(output_md_path)
    except Exception as e:
        print(f"Error converting to PDF: {e}")


def create_rent_receipts(start_month, end_month, year):
    """Generate rent receipts for a range of months."""
    for month in range(start_month, end_month + 1):
        print(f"Generating rent receipt for {calendar.month_name[month]} {year}...")
        render_rent_receipt(month, year)


def main():
    year = 2024
    start_month = 8
    end_month = 12
    create_rent_receipts(start_month, end_month, year)


if __name__ == "__main__":
    main()

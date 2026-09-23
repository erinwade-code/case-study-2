# Case Study 2

# Dataset Chosen:

## Information and Rules
(Put information and rules here about your part)

## Project Structure
main.py - entry point
config.py - input path, filter values, group columns, output folder
loader.py - loads and validates the raw data
transform.py - filtering, derived columns, grouping
numpy_ops.py - NumPy comparison and plots
validate.py - validation and audit log

## Instructions:
1. Clone this repository to your computer
2. Create a virtual environment
3. Activate it
4. Install requirements
5. Download dataset file and place it in a data/ folder in the project root (it's gitignored either way)
6. Run the program

## Reminders
1. Commit regularly on your part
2. When your part is done, open a pull request so that another member can review your part before merging

Markdown
## Data Filtering and Transformation Rules (Gab - Work B)

### Filter Rules
Filtering is performed using `pandas.loc` with a boolean mask combining two strict conditions:
1. **Origin Country Constraint (`countryorigin_iso3`):** Selected records must have an ISO3 origin code equal to `'CHN'` (China).
2. **Transaction Quantity Constraint (`tq`):** Selected records must have a Tariff Quantity (`tq`) strictly greater than `0`.

### Derived Columns
1. **`estimated_duty_php` (Numerical Measure):**
   * **Formula:** `dutiablevaluephp * duty_rate` (default `duty_rate = 0.05` or 5%).
2. **`value_category_flag` (Category / Flag):**
   * **Formula:** Binary flag assigned based on the median `dutiablevaluephp` of filtered records (`High_Value` vs `Low_Value`).

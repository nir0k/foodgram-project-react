import csv
from recipes.models import Ingredient
from pathlib import Path

file = open(Path(__file__).resolve().parent / 'ingredients.csv')
read_file = csv.reader(file)
count = 1
for record in read_file:
    if count == 1:
        count += 1
        continue
    print(f'name={record[0]}, measurement_unit={record[1]}')
    Ingredient.objects.create(name=record[0], measurement_unit=record[1])

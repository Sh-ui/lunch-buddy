import json
from pathlib import Path

from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {})


def pantry(request):
    """Render a spreadsheet-like view of the pantry.json file.

    Notes:
    - Reads from DATA_DIR / 'pantry.json'. Falls back to project var/pantry.json.
    - Passes schema, enums, and ingredients to the template for rendering.
    """
    data_path_candidates: list[Path] = [
        Path(settings.DATA_DIR) / 'pantry.json',
        Path(settings.BASE_DIR) / 'var' / 'pantry.json',
    ]
    pantry_data: dict = {"ingredients": [], "schema": {}, "enums": {}}
    for candidate in data_path_candidates:
        try:
            if candidate.exists():
                with candidate.open('r', encoding='utf-8') as f:
                    pantry_data = json.load(f)
                break
        except Exception:
            # If parsing fails, leave pantry_data empty; template will show an alert
            pantry_data = {"ingredients": [], "schema": {}, "enums": {}}

    ingredients: list[dict] = pantry_data.get('ingredients', [])
    schema: dict = pantry_data.get('schema', {})
    enums: dict = pantry_data.get('enums', {})

    # Column order: prefer schema.fields if present, otherwise a sensible default
    default_columns = [
        'key', 'name', 'type', 'tags', 'families', 'prep', 'methods',
        'allowed_in', 'storage', 'aliases', 'is_pantry',
    ]
    columns = schema.get('fields') or default_columns

    context = {
        'columns': columns,
        'ingredients': ingredients,
        'schema': schema,
        'enums': enums,
        'pantry_count': len([i for i in ingredients if i.get('is_pantry')]),
        'item_count': len(ingredients),
    }
    return render(request, 'pantry.html', context)


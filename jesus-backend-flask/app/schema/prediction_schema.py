def validate_prediction_input(data):
    required_fields = ['correo', 'BP', 'Chol', 'BMI', 'Smoker', 'Stroke', 'HDA', 'PA', 'GH', 'MH', 'PH', 'Age']
    errors = []

    for field in required_fields:
        if field not in data:
            errors.append(f'El campo {field} es requerido.')

    # Validaciones adicionales, como tipos de datos o rangos específicos
    if 'correo' in data and not isinstance(data['correo'], str):
        errors.append('El correo debe ser una cadena de texto.')

    # if 'colesterol' in data and not isinstance(data['colesterol'], (int, float)):
    #     errors.append('El colesterol debe ser un número.')

    # if 'edad' in data and not isinstance(data['edad'], int):
    #     errors.append('La edad debe ser un número entero.')

    # if 'salud_fisica' in data and not isinstance(data['salud_fisica'], (int, float)):
    #     errors.append('La salud física debe ser un número.')

    # if 'salud_mental' in data and not isinstance(data['salud_mental'], (int, float)):
    #     errors.append('La salud mental debe ser un número.')

    return errors if errors else None

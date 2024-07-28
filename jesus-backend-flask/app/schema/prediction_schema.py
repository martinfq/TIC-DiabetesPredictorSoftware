def validate_prediction_input(data):
    required_fields = ['correo', 'BP', 'Chol', 'BMI', 'Smoker', 'Stroke', 'HDA', 'PA', 'GH', 'MH', 'PH', 'Age']
    errors = []

    # Verifica que los campos no esten vacios
    for field in required_fields:
        if field not in data:
            errors.append(f'El campo {field} es requerido.')

    # Verifica el contenido de cada campo
    if 'correo' in data and not isinstance(data['correo'], str):
        errors.append('El correo debe ser una cadena de texto.')

    if 'BP' in data and (not isinstance(data['BP'], int) or (data['BP']!=0 and data['BP']!=1)):
        errors.append('El BP debe ser un número.')

    if 'Chol' in data and (not isinstance(data['Chol'], int) or (data['Chol']!=0 and data['Chol']!=1)):
        errors.append('El Chol debe ser un número.')
    
    if 'BMI' in data and (not isinstance(data['BMI'], int) or data['BMI']<10):
        errors.append('El BMI debe ser un número.')
    
    if 'Smoker' in data and (not isinstance(data['Smoker'], int) or (data['Smoker']!=0 and data['Smoker']!=1)):
        errors.append('El Smoker debe ser un número.')

    if 'Stroke' in data and (not isinstance(data['Stroke'], int) or (data['Stroke']!=0 and data['Stroke']!=1)):
        errors.append('El Stroke debe ser un número.')

    if 'HDA' in data and (not isinstance(data['HDA'], int) or (data['HDA']!=0 and data['HDA']!=1)):
        errors.append('El HDA debe ser un número.')

    if 'PA' in data and (not isinstance(data['PA'], int) or (data['PA']!=0 and data['PA']!=1)):
        errors.append('El PA debe ser un número.')

    if 'GH' in data and (not isinstance(data['GH'], int) or (data['GH']<0 and data['GH']>30)):
        errors.append('El GH debe ser un número.')

    if 'MH' in data and (not isinstance(data['MH'], int) or (data['MH']<0 and data['MH']>30)):
        errors.append('El MH debe ser un número.')

    if 'PH' in data and (not isinstance(data['PH'], int) or (data['PH']<0 and data['PH']>30)):
        errors.append('El PH debe ser un número.')

    if 'Age' in data and not isinstance(data['Age'], (int, float)):
        errors.append('El Age debe ser un número.')

    return errors if errors else None

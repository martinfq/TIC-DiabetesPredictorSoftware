def validate_prediction_input(data):
    required_fields = ['HighBP', 'HighChol', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'GenHlth', 'MentHlth', 'PhysHlth']
    errors = []

    # Verifica que los campos no esten vacios
    for field in required_fields:
        if field not in data:
            errors.append(f'El campo {field} es requerido.')

    # Verifica el contenido de cada campo

    if 'HighBP' in data and (not isinstance(data['HighBP'], int) or (data['HighBP']!=0 and data['HighBP']!=1)):
        errors.append('El BP debe ser un número entre 0 y 1.')

    if 'HighChol' in data and (not isinstance(data['HighChol'], int) or (data['HighChol']!=0 and data['HighChol']!=1)):
        errors.append('El Chol debe ser un número entre 0 y 1.')
    
    if 'BMI' in data and (not isinstance(data['BMI'], int) or data['BMI']<10):
        errors.append('El BMI debe ser un número mayor a 10.')
    
    if 'Smoker' in data and (not isinstance(data['Smoker'], int) or (data['Smoker']!=0 and data['Smoker']!=1)):
        errors.append('El Smoker debe ser un número entre 0 y 1.')

    if 'Stroke' in data and (not isinstance(data['Stroke'], int) or (data['Stroke']!=0 and data['Stroke']!=1)):
        errors.append('El Stroke debe ser un número entre 0 y 1.')

    if 'HeartDiseaseorAttack' in data and (not isinstance(data['HeartDiseaseorAttack'], int) or (data['HeartDiseaseorAttack']!=0 and data['HeartDiseaseorAttack']!=1)):
        errors.append('El HeartDiseaseorAttack debe ser un número entre 0 y 1.')

    if 'PhysActivity' in data and (not isinstance(data['PhysActivity'], int) or (data['PhysActivity']!=0 and data['PhysActivity']!=1)):
        errors.append('El PhysActivity debe ser un número entre 0 y 1.')

    if 'GenHlth' in data and (not isinstance(data['GenHlth'], int) or (data['GenHlth']<0 and data['GenHlth']>5)):
        errors.append('El GenHlth debe ser un número entre 1 y 5.')

    if 'MentHlth' in data and (not isinstance(data['MentHlth'], int) or (data['MentHlth']<0 and data['MentHlth']>30)):
        errors.append('El MentHlth debe ser un número entre 0 y 30.')

    if 'PhysHlth' in data and (not isinstance(data['PhysHlth'], int) or (data['PhysHlth']<0 and data['PhysHlth']>30)):
        errors.append('El PhysHlth debe ser un número entre 0 y 1.')

    return errors if errors else None

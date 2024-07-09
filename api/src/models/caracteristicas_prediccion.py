class CaracteristicasPrediccion:    
    def __init__(self, highBP, highChol, bmi, smoker, stroke, heartDiseaseOrAttack, physActivity, genHlth, mentHlth, physHlth, age):
        self.highBP = highBP
        self.highChol = highChol
        self.bmi = bmi
        self.smoker = smoker
        self.stroke = stroke
        self.heartDiseaseOrAttack = heartDiseaseOrAttack
        self.physActivity = physActivity
        self.genHlth = genHlth
        self.mentHlth = mentHlth
        self.physHlth = physHlth
        self.age = age

    #AGREGAR METODO DE CLASE PARA VALIDAR LOS CAMPOS Y SU DOMINIO
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
    def is_valid(self):
        #HighBP
        if not isinstance(self.highBP, int) or (self.highBP != 0 and self.highBP != 1):
            return False

        #HighChol
        if not isinstance(self.highChol, int) or (self.highChol != 0 and self.highChol != 1):
            return False

        #BMI
        if not isinstance(self.bmi, int) or self.bmi < 1:
            return False

        #Smoker
        if not isinstance(self.smoker, int) or (self.smoker != 0 and self.smoker != 1):
            return False

        #Stroke
        if not isinstance(self.stroke, int) or (self.stroke != 0 and self.stroke != 1):
            return False

        #HeartDiseaseOrAttack
        if not isinstance(self.heartDiseaseOrAttack, int) or (self.heartDiseaseOrAttack != 0 and self.heartDiseaseOrAttack != 1):
            return False

        #PhysActivity
        if not isinstance(self.physActivity, int) or (self.physActivity != 0 and self.physActivity != 1):
            return False

        #GenHlth
        if not isinstance(self.genHlth, int) or (self.genHlth < 0 or self.genHlth > 30):
            return False

        #MentHlth
        if not isinstance(self.mentHlth, int) or (self.mentHlth < 0 or self.mentHlth > 30):
            return False

        #PhysHlth
        if not isinstance(self.physHlth, int) or (self.physHlth < 0 or self.physHlth > 30):
            return False

        #Age

        return True
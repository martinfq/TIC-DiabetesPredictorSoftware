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

    def is_valid(self):
        #HighBP
        if not isinstance(self.highBP, (int, float)) or self.highBP not in (0, 1):
            return False

        #HighChol
        if not isinstance(self.highChol, (int, float)) or self.highChol not in (0, 1):
            return False

        #BMI
        if not isinstance(self.bmi, (int, float)) or self.bmi < 1:
            return False

        #Smoker
        if not isinstance(self.smoker, (int, float)) or self.smoker not in (0, 1):
            return False

        #Stroke
        if not isinstance(self.stroke, (int, float)) or self.stroke not in (0, 1):
            return False

        #HeartDiseaseOrAttack
        if not isinstance(self.heartDiseaseOrAttack, (int, float)) or self.heartDiseaseOrAttack not in (0, 1):
            return False

        #PhysActivity
        if not isinstance(self.physActivity, (int, float)) or self.physActivity not in (0, 1):
            return False

        #GenHlth
        if not isinstance(self.genHlth, (int, float)) or not (1 <= self.genHlth <= 5):
            return False

        #MentHlth y PhysHlth
        for attr in [self.mentHlth, self.physHlth]:
            if not isinstance(attr, (int, float)) or not (0 <= attr <= 30):
                return False

        #Age
        if not isinstance(self.age, (int, float)) or self.age < 0:
            return False

        return True
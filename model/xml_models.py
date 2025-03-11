class XMLStudent:
    def __init__(self,
                 fio,
                 father_fio,
                 mother_fio,
                 father_income,
                 mother_income,
                 brother_count,
                 sister_count
                 ):
        self.fio = fio
        self.father_fio = father_fio
        self.mother_fio = mother_fio
        self.father_income = float(father_income)
        self.mother_income = float(mother_income)
        self.brother_count = int(brother_count)
        self.sister_count = int(sister_count)

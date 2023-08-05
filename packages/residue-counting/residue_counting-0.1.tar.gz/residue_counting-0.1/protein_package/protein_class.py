class protein:
    def __init__(self, sequence):
        self.sequence = sequence

    def alanine_scan(self):
        return self.sequence.count('A')

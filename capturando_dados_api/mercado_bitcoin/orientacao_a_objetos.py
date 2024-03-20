import datetime
import math


class Pessoa:
    def __init__(self, nome: str, nascimento: datetime.date) -> None:
        self.nome = nome
        self.nascimento = nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f'{self.nome} tem {self.idade} anos'


mauricio = Pessoa('Mauricio Menezes', datetime.date(1995, 7, 30))

print(mauricio)
print(mauricio.idade)

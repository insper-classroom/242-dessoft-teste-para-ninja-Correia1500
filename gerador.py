import random

def gera_numeros():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    num3 = random.randint(1, 20)
    
    # Escolhe aleatoriamente dois números para somar
    soma_correta = random.choice([(num1, num2), (num1, num3), (num2, num3)])
    num4 = sum(soma_correta)
    
    return [num1, num2, num3, num4]

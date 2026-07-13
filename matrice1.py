import numpy as np
from random import randint, random


def cree_matrices():

    np.random.seed(8)

    B1 = np.zeros((66))
    B2 = np.zeros((14))
    B3 = np.zeros((1))

    M1 = np.random.randn(14, 66) * np.sqrt(2 / 14)
    M2 = np.random.randn(66, 14) * np.sqrt(2 / 66)
    M3 = np.random.randn(14,) * np.sqrt(2 / 14)

    """for i in range(14):
        for j in range(14):
            M1[i,j] = randint(-1, 1)*random()

    for i in range(14):
        for j in range(14):
            M2[i,j] = randint(-1, 1)*random()

    for i in range(14):
            M3[i] = randint(-1, 1)*random()"""


    B1 = np.random.randn(66) * np.sqrt(2/14)
    B2 = np.random.randn(14) * np.sqrt(2/66)


    B3 = np.random.randn() * np.sqrt(2/14)

    np.save('M1.npy', M1)
    np.save('M2.npy', M2)
    np.save('M3.npy', M3)

    np.save('B1.npy', B1)
    np.save('B2.npy', B2)
    np.save('B3.npy', B3)
     
    print("les matrices ont été créés !")

    return M1, M2, M3, B1, B2, B3


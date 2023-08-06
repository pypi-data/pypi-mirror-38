import sys
import os


class dvtDecimal:

    def __init__(self, p, q):
        # determination du signe
        if p * q == 0:
            self.sign = 0
        else:
            self.sign = (-1, 1)[p * q > 0]
        # valeurs initiales preservees
        self.__pInit = p
        self.__qInit = q
        self.initValues = [p, q]
        # on rend positives les valeurs
        # ce sont donc les valeurs de travail
        # attention elles sont variables !!
        # on gère le signe dans les operations +-*/
        self.__p = abs(p)
        self.__q = abs(q)
        #
        self._intInputCheck()
        self.__decalage = 0
        self._traitement()

    def __add__(self, d):
        p, q = self.initValues
        try:
            # si d est un dvtDecimal
            pp, qq = d.initValues
        except AttributeError:
            # si d est un entier positif
            if int(d) == abs(d):
                pp, qq = d, 1
            else:
                raise ValueError("Impossible +: value is not int\
                nor dvtDecimal!")
        return dvtDecimal(p * qq + pp * q, q * qq)

    def __sub__(self, d):
        p, q = self.initValues
        try:
            # si d est un dvtDecimal
            pp, qq = d.initValues
        except AttributeError:
            # si d est un entier positif
            if int(d) == abs(d):
                pp, qq = d, 1
            else:
                raise ValueError("Impossible -: value is not int\
                nor dvtDecimal!")
        return dvtDecimal(p * qq - pp * q, q * qq)

    def __mul__(self, d):
        p, q = self.initValues
        try:
            # si d est un dvtDecimal
            pp, qq = d.initValues
        except AttributeError:
            # si d est un entier positif
            if int(d) == abs(d):
                pp, qq = d, 1
            else:
                raise ValueError("Impossible *: value is not int\
                nor dvtDecimal!")
        return dvtDecimal(p * pp, q * qq)

    def __truediv__(self, d):
        p, q = self.initValues
        try:
            # si d est un dvtDecimal
            pp, qq = d.initValues
        except AttributeError:
            # si d est un entier positif
            if int(d) == abs(d):
                pp, qq = d, 1
            else:
                raise ValueError("Impossible /: value is not int\
                nor dvtDecimal!")
        return dvtDecimal(p * qq, pp * q)

    def _intInputCheck(self):
        try:
            assert self.__pInit == int(self.__pInit)
            assert self.__qInit == int(self.__qInit)
        except AssertionError:
            print('Error: Use proper integers', self.__pInit, self.__qInit)
            sys.exit(os.EX_DATAERR)

    def _gcd(self):
        # on reprend les valeurs init
        a, b = self.__pInit, self.__qInit
        # on les rend positives
        a, b = abs(a), abs(b)
        if a > b: a, b = b, a
        while b != 0:
            a, b = b, a % b
        self.gcd = a
        # on renvoie une valeur positive
        return self.gcd

    def _puissance10(self):
        while self.__q // 10 == self.__q / 10:
            self.__decalage += 1
            self.__q /= 10

    def _enleve2(self):
        while self.__q % 2 == 0:
            self.__decalage += 1
            self.__q /= 2
            self.__p *= 5

    def _enleve5(self):
        while self.__q % 5 == 0:
            self.__decalage += 1
            self.__q /= 5
            self.__p *= 2

    def _calculPartiePeriodique(self, p, q):
        self.repPart = []
        resteInit = p
        reste = -1
        while reste != resteInit:
            p *= 10
            d = p // q
            p = p % q
            reste = p
            self.repPart.append(int(d))

    def _formatagePartieIrr(self):
        lpE = len(str(self.__pi))
        self.__nbZ = self.__decalage - lpE
        self.irrPart = "0."
        if self.__nbZ >= 0:
            for i in range(self.__nbZ):
                self.irrPart += "0"
            self.irrPart += str(self.__pi)

    def _versMixedF(self):
        p, q = map(abs, self.simpValues)
        e = abs(self.intPart)
        self.mixedF = [e * self.sign, p - e * q, q]

    def _traitement(self):
        # attention travail négatif potentiel
        self.simpValues = [k//self._gcd() for k in self.initValues]
        self.intPart = int(self.__pInit / self.__qInit)
        # valeurs positives requises pour le travail
        self.__p = abs(self.__pInit) - abs(self.__qInit) * abs(self.intPart)
        self.__p, self.__q = self.__p // self._gcd(), self.__q // self._gcd()
        # debut algo
        self._puissance10()
        self._enleve2()
        self._enleve5()
        self.__pi = int(self.__p // self.__q)
        self.__p = self.__p % self.__q
        self._formatagePartieIrr()
        self._calculPartiePeriodique(self.__p, self.__q)
        # fin algo
        self._repPartConcat()
        self._periodLen()
        self._versMixedF()

    def dispResults(self):
        print("For fraction:", self.__pInit, "/", self.__qInit)
        print("    integer   part :", self.intPart)
        print("    irregular part :", self.irrPart)
        print("    periodic  part :", self.repPart)
        print("    mixed fraction :", self.mixedF)
        print("    Python outputs :", self.__pInit/self.__qInit)

    def _repPartConcat(self):
        self.repPartC = ''
        for d in self.repPart:
            self.repPartC += str(d)
        return self.repPartC

    def isDecimal(self):
        return self.repPart == [0]

    def _periodLen(self):
        self.periodLen = len(self._repPartConcat())

    # n est le nombre de chiffres apres la virgule
    def dotWrite(self, n):
        resultat = str(self.intPart)
        # on compte les longueurs (apres la virgule)
        lpI = len(str(self.irrPart)[2:])
        lpP = len(self._repPartConcat())
        if n <= lpI:
            resultat += str(self.irrPart)[1:n+2]
        elif n <= lpI+lpP:
            resultat += str(self.irrPart)[1:] + \
                        self._repPartConcat()[:n-lpI]
        else:
            resultat += str(self.irrPart)[1:]
            for i in range((n-lpI) // lpP):
                resultat += self._repPartConcat()
            resultat += self._repPartConcat()[:(n-lpI) % lpP]
        return resultat


if __name__ == '__main__':
    f = dvtDecimal(-604, 260)
    f.dispResults()
    print(f.dotWrite(20))
    print(f.intPart)
    print(f.irrPart)
    print(f.repPart)
    print(f.repPartC)
    print(f.periodLen)
    print(f.gcd)
    print(f.initValues)
    print(f.simpValues)
    print(f.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(10, 3)
    h = f + g
    print(h.mixedF)
    print('###')
    i = f / g
    print(i.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = dvtDecimal(7, 5)
    h = f - g
    print(h.simpValues)
    print(h.sign)
    print(h.mixedF)
    print('###')
    f = dvtDecimal(1, 5)
    g = 5
    h = f * g
    h.dispResults()
    print(h.sign)
    print(h.mixedF)
    print(h.isDecimal())

import os
import sys

class dvtDecimal:
    """classe d'écriture d'un nombre en fraction
    à numérateur et dénominateur entiers.
    Le principe est simple :
    - la fraction est simplifiée (pgcd)
    - on fait en sorte que le dénominateur et 10
    soient premiers entre eux
    - on isole notre partie entière, notre partie
    irégulière et notre fraction avec den. premier
    avec 10
    - on calcule par div. successives sur cette
    dernière fraction notre partie qui se répète
    """

    def __init__(self, *args):
        # si deux arguments : num et den
        if len(args) == 2:
            self._initFraction(args[0], args[1])
        # si un argument avec . : nombre décimal
        elif type(args[0]) == float:
            self._initFloat(args[0])
        # si un argmuent sans . : une période
        elif type(args[0]) == str:
            self._initStr(args[0])
        else:
            print("Can't understand your input!")
            quit()
    
    def _initFraction(self, p, q):
        """initialisation des objets de la classe"""
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
        # vérification de l'entrée
        self._intInputCheck()
        # 
        # Traitement
        # C'est ci-dessous que tout se passe
        # 
        self.__decalage = 0
        self._traitement()

    def _initFloat(self, d):
        sD = str(d)
        iVirgule = sD.find('.')
        puisDix = 10 ** (len(sD) - iVirgule - 1)
        self._initFraction(int(d * puisDix), puisDix)

    def _initStr(self, s):
        num = int(s)
        den = int("9" * len(s))
        self._initFraction(num, den)

####################################################################
####################################################################
    def _intInputCheck(self):
        try:
            assert self.__pInit == int(self.__pInit)
            assert self.__qInit == int(self.__qInit)
        except AssertionError:
            print('\nError: Use proper integers', self.__pInit, self.__qInit, '\n')
            sys.exit(os.EX_DATAERR)

####################################################################
####################################################################
    def __add__(self, d):
        """définition de l'addition
        utilisable avec le symbole + ainsi surchargé"""
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
        """voir addition"""
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
        """voir addition"""
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
        """voir addition"""
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

####################################################################
####################################################################
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

####################################################################
####################################################################
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

####################################################################
####################################################################
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

    def _repPartConcat(self):
        self.repPartC = ''
        for d in self.repPart:
            self.repPartC += str(d)
        return self.repPartC

    def _periodLen(self):
        self.periodLen = len(self._repPartConcat())

####################################################################
####################################################################
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

####################################################################
####################################################################

    def dispResults(self):
        print("For fraction:", self.__pInit, "/", self.__qInit)
        print("    integer   part :", self.intPart)
        print("    irregular part :", self.irrPart)
        print("    periodic  part :", self.repPart)
        print("    mixed fraction :", self.mixedF)
        print("    simp. fraction :", self.simpValues)
        print("               gcd :", self.gcd)
        print("    Python outputs :", self.__pInit/self.__qInit)

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

    def isDecimal(self):
        return self.repPart == [0]

####################################################################
####################################################################


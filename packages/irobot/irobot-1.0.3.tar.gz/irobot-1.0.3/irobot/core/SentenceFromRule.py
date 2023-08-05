# coding: utf8

from __future__ import print_function

class SentenceFromRule():

    def __init__(self):
        self.ent = ""
        self.rel = []
        self.prop = ""
        self.desc = ""
        self.descp = ""
        self.unit = ""
        self.unitp = ""
        self.value = []
        self.valuep = []
        self.verb = ""
        self.verbp = ""

    def setSentence(self, tag, term):
        if tag == "e":
            self.setEnt(term)
        elif tag == "r":
            self.setRel(term)
        elif tag == "p":
            self.setProp(term)
        elif tag == "v":
            self.setValue(term)
        elif tag == "d":
            self.setDesc(term)
        elif tag == "u":
            self.setUnit(term)
        elif tag == "a":
            self.setVerb(term)

    def getSentence(self, tag):
        if tag == "e":
            return self.getEnt()
        elif tag == "r":
            return self.getRel()
        elif tag == "p":
            return self.getProp()
        elif tag == "v":
            return self.getValue()
        elif tag == "d":
            return self.getDesc()
        elif tag == "u":
            return self.getUnit()
        elif tag == "a":
            return self.getVerb()

    def checkSentence(self):
        return
        if self.checkDesc() \
            and self.checkValue() \
            and self.checkUnit() \
            and self.checkVerb():
            return True
        else:
            return False

    def setEnt(self, term):
        self.ent = term

    def getEnt(self):
        return self.ent

    def setRel(self, term):
        self.rel.append(term)

    def getRel(self):
        return self.rel.pop(0)

    def setProp(self, term):
        self.prop = term

    def getProp(self):
        return self.prop

    def setValue(self, term):
        temp = term.split("\t")
        try:
            self.value.append(temp[1])
            self.valuep.append(temp[0])
        except IndexError:
            self.value.append(temp[0])

    def getValue(self):
        return self.value.pop(0)

    def checkValue(self):
        if not self.prop \
            or (len(set(self.valuep)) == 1 and self.valuep[0] == self.prop):
            return True
        else:
            return False

    def setDesc(self, term):
        temp = term.split("\t")
        try:
            self.desc = temp[1]
            self.descp = temp[0]
        except IndexError:
            self.desc = temp[0]

    def getDesc(self):
        return self.desc

    def checkDesc(self):
        if not self.desc:
            return True
        elif not self.prop \
            or self.descp == self.prop:
            return True
        else:
            return False

    def setUnit(self, term):
        temp = term.split("\t")
        try:
            self.unit = temp[1]
            self.unitp = temp[0]
        except IndexError:
            self.unit = temp[0]

    def getUnit(self):
        return self.unit

    def checkUnit(self):
        if not self.unit:
            return True
        elif not self.prop \
            or self.unitp == self.prop:
            return True
        else:
            return False
    
    def setVerb(self, term):
        temp = term.split("\t")
        try:
            self.verb = temp[1]
            self.verbp = temp[0]
        except IndexError:
            self.verb = temp[0]

    def getVerb(self):
        return self.verb

    def checkVerb(self):
        if not self.value:
            return True
        elif not self.prop \
            or self.verbp == self.prop:
            return True
        else:
            return False


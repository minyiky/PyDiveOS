class Gas:
    def __init__(self, o2: int, he: int):
        assert o2 + he <= 100
        self.o2 = o2 / 100
        self.he = he / 100
        self.n2 = (100 - o2 - he) / 100
        self.enabled = True

        self._o2 = o2
        self._he = he
        self._n2 = 100 - o2 - he
    
    @classmethod
    def from_string(cls, s: str):
        if s == "air":
            return cls(21, 0)
        if s.startswith("ean"):
            o2 = int(s[-2:])
            return cls(o2, 0)
        if s.startswith("tri"):
            o2 = int(s[-5:-3])
            he = int(s[-2:])
            return cls(o2, he)

        o2 = int(s[-2:])
        return cls(o2, 100-o2)
            
    def __str__(self):  # sourcery skip: assign-if-exp, reintroduce-else
        if self._o2 == 21 and self._he == 0:
            return "air"
        if self._he == 0:
            return f"ean{self._o2}"
        if self._n2 == 0:
            return f"heliox{self._o2}"
        return f"tri{self._o2}/{self._he}"

if __name__ == "__main__":
    print(Gas(21, 0))
    print(Gas(32, 0))
    print(Gas(35, 18))
    print(Gas(35, 65))
    print(Gas.from_string("air").o2, Gas.from_string("air").he)
    print(Gas.from_string("ean32").o2, Gas.from_string("ean32").he)
    print(Gas.from_string("heliox35").o2, Gas.from_string("heliox35").he)
    print(Gas.from_string("tri35/18").o2, Gas.from_string("tri35/18").he)
    
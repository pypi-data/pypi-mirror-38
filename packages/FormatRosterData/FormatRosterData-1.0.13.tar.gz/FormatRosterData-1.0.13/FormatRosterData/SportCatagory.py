import enum

class SportCatagory(enum.Enum):
    Basketball_Women = enum.auto()
    Basketball_Men = enum.auto()
    Hockey_Women = enum.auto()
    Hockey_Men = enum.auto()
    Wrestling = enum.auto()

    @staticmethod
    def GetFromString(sString):
        sString = sString.lower()
        if "basketball" in sString:
            if "women" in sString:
                return SportCatagory.Basketball_Women
            elif "men" in sString:
                return SportCatagory.Basketball_Men
        elif "hockey" in sString:
            if "women" in sString:
                return SportCatagory.Hockey_Women
            elif "men" in sString:
                return SportCatagory.Hockey_Men
        elif "wresting" in sString:
            return SportCatagory.Wrestling

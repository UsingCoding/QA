import sys

def checkTriangleArgs(sides):
    for arg in sides:
        try:
            convertedArg = float(arg)
            if convertedArg == float("inf") or convertedArg < 0:
                return False
        except:
            return False

    return True

def checkTriangle(sides):
    flag = checkTriangleArgs(sides)

    if (flag and (len(sides) == 3)):
        a = float(sides[0])
        b = float(sides[1])
        c = float(sides[2])

        if ((a + b > c) and (b + c > a) and (a + c > b)):
            if (a == b and b == c):
                return "Равносторонний"
            elif (a == b or a == c or b == c):
                return "Равнобедренный"
            else:
                return "Обычный"
        else:
            return "Не Треугольник"

    if (flag):
        return "Не Треугольник"

    return "Неизвестная ошибка"


if __name__ == "__main__":
    print(checkTriangle(sys.argv[1::]))

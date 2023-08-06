import math

class JustMathGenius:
    @staticmethod
    def editDistance(str1, str2):
        l1 = len(str1)
        l2 = len(str2)
        superMatrix = []
        for i in range(l2 + 1):
            superMatrix.append([])
            for j in range (l1 + 1):
                if (i == 0):
                    superMatrix[i].append(j)
                elif j == 0:
                    superMatrix[i].append(i)
                else:
                    superMatrix[i].append(0)
        temp = 0
        for i in range(1, l2 + 1):
            for j in range(1, l1 + 1):
                if str2[i - 1] == str1[j - 1]:
                    temp = 0
                else:
                    temp = 1
                superMatrix[ i ][ j ] = min(superMatrix[i - 1][j] + 1, superMatrix[i][j - 1] + 1, superMatrix[i - 1][j - 1] + temp)
        comparison = 1 - superMatrix[l2][l1] / max(l1, l2)
        return comparison
    
    @staticmethod
    def numberDeviation(number1, number2):
        if (number1 == 0):
            return 0
        return 1 - abs((number1 - number2) / number1 )

    @staticmethod
    def coordDistance(coords):
        earthR = 6371
        def degreesToRadians(degrees):
            return (degrees * math.pi / 180)
        degreesLat = degreesToRadians( coords[1]['lat'] - coords[0]['lat'] )
        degreesLon = degreesToRadians( coords[1]['lng'] - coords[0]['lng'] )
        lat1 = degreesToRadians(coords[0]['lat'])
        lat2 = degreesToRadians(coords[1]['lat'])
        a = pow(math.sin(degreesLat / 2), 2) + pow(math.sin(degreesLon / 2), 2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earthR * c * 1000
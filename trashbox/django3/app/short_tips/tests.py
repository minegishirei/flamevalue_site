from django.test import TestCase

# Create your tests here.
from .views import htmlManeger


htmlManeger = htmlManeger()
directoryInfo = htmlManeger.main("/app/engineer/templates")
for compose in (directoryInfo.nextComposeList):
    print( compose.path )
    for compose in compose.nextComposeList:
        print(compose.path)



class htmlManegerTest(TestCase):
    def a(self):
        htmlManeger = htmlManeger()
        directoryInfo = htmlManeger.main("/app/engineer/templates")
        for compose in (directoryInfo.nextComposeList):
            print( compose.path )
            for compose in compose.nextComposeList:
                print(compose.path)

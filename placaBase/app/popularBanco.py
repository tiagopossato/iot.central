#!/usr/bin/python3
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()


from central.views import newAlarmeTipo
from central.placaIO import newEntradaDigital, newPlacaExpansaoDigital, updateEntradaDigital
# from placaIO import newPlacaExpansaoDigital, newEntradaDigital, updateEntradaDigital

# newAlarmeTipo(1,"Disjuntor 1 desarmado", 3)
# newAlarmeTipo(2,"Disjuntor 2 desarmado", 3)
# newAlarmeTipo(3,"Disjuntor 3 desarmado", 3)
# newAlarmeTipo(4,"Disjuntor 4 desarmado", 3)
# newAlarmeTipo(5,"Disjuntor 5 desarmado", 3)
# newAlarmeTipo(6,"Disjuntor 6 desarmado", 3)
# newAlarmeTipo(7,"Disjuntor 7 desarmado", 3)
# newAlarmeTipo(8,"Disjuntor 8 desarmado", 3)
# newPlacaExpansaoDigital(_idRede=3)
# newPlacaExpansaoDigital(_idRede=2)
# newEntradaDigital(_placaExpansaoDigital=3, _numero=0, _codigoAlarme = 1, _nome = "Disjuntor 1")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=1, _codigoAlarme = 2, _nome = "Disjuntor 2")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=2, _codigoAlarme = 3, _nome = "Disjuntor 3")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=3, _codigoAlarme = 4, _nome = "Disjuntor 4")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=4, _codigoAlarme = 5, _nome = "Disjuntor 5")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=5, _codigoAlarme = 6, _nome = "Disjuntor 6")
# newEntradaDigital(_placaExpansaoDigital=3, _numero=6, _codigoAlarme = 7, _nome = "Disjuntor 7")
# newEntradaDigital(_placaExpansaoDigital=2, _numero=0, _codigoAlarme = None, _nome = "Disjuntor 8")
# causa erro proposital:
# newEntradaDigital(_placaExpansaoDigital=3, _numero=7, _codigoAlarme = 8, _nome = "Disjuntor 8")
# updateEntradaDigital(1, _nome="Disjuntor 1")
#updateEntradaDigital(1, _codigoAlarme=None)

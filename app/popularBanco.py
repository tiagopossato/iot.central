#!/usr/bin/python3

from alarmes import newAlarmeTipo
from placaIO import newPlacaExpansaoDigital, newEntradaDigital, updateEntradaDigital

#newAlarmeTipo(1,"Disjuntor 1 desarmado", 3)
#newAlarmeTipo(2,"Disjuntor 2 desarmado", 3)
#newAlarmeTipo(3,"Disjuntor 3 desarmado", 3)
#newPlacaExpansaoDigital(_idRede=3)
#newPlacaExpansaoDigital(_idRede=2)
#newEntradaDigital(_codigoPlacaExpansaoDigital=3, _numero=0, _codigoAlarme = 1, _nome = "Disjuntor 1")
#newEntradaDigital(_codigoPlacaExpansaoDigital=3, _numero=1, _codigoAlarme = 2, _nome = "Disjuntor 2")
#newEntradaDigital(_codigoPlacaExpansaoDigital=3, _numero=2, _codigoAlarme = 3, _nome = "Disjuntor 3")
#updateEntradaDigital(1, _nome="Disjuntor 1")
updateEntradaDigital(1, _codigoAlarme=None)

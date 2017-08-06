from aplicacao.models import Leitura, Sensor, SensorGrandeza

def novaLeitura(_idRede, _grandeza, _valor):
    try:
        sensor = Sensor.objects.get(idRede=_idRede)
        sg = SensorGrandeza.objects.get(sensor=sensor, grandeza_id=_grandeza)
        l = Leitura(valor=_valor, grandeza=sg.grandeza,
                    ambiente=sensor.ambiente, sensor=sensor)
        l.save()
    except Sensor.DoesNotExist:
        print('ID de rede: ' + str(_idRede) + ' nao encontrado')
        return False
    except SensorGrandeza.DoesNotExist:
        print('A grandeza ' + str(_grandeza) +
              ' nao esta cadastrada no sensor ' + str(sensor))
        return False
    except Exception as e:
        print(e)
        return False

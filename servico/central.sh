#!/bin/bash
#
### BEGIN INIT INFO
# Provides:             central
# Required-Start:       $network
# Required-Stop:        $network
# Default-Start:        2 3 4 5
# Default-Stop:         0 1 6
# Short-Description:    Aplicativo da central
# Description:          Aplicativo que controla a central de monitoramento de sensores
### END INIT INFO

start() {
	if ( test -f /var/run/central.pid );then
		echo "Serviço rodando, utilize restart"
		exit $?
	fi

#	if ( test -f /var/run/centralSinc.pid );then
#		echo "Serviço rodando, utilize restart"
#		exit $?
#	fi

	python3 /opt/iot.central/placaBase/app/app.py &
#	python3 /opt/iot.central/placaBase/app/sincronizaAlarmes.py &
}

stop() {
	if ( test -f /var/run/central.pid );then
		pid=$(cat /var/run/central.pid)
		kill -9 $pid
		rm /var/run/central.pid
	fi

#	if ( test -f /var/run/centralSinc.pid );then
#		pid=$(cat /var/run/centralSinc.pid)
#		kill -9 $pid
#		rm /var/run/centralSinc.pid
#	fi
}

restart() {
  stop
  start
}

case "$1" in
  start)
    start
    ;;
  stop)
  stop
    ;;
  restart)
    restart
    ;;
  *)
    echo $"Usage: $0 {start|stop|restart}"
    exit 1
esac
exit $?

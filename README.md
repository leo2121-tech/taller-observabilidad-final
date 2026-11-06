# Taller de Observabilidad
## Descripción del proyecto
Proyecto de implementación de un sistema de observabilidad utilizando herramientas de monitoreo, visualización de métricas, centralización de logs y trazabilidad distribuida.
La solución permite supervisar el estado de los servicios, analizar métricas de infraestructura, consultar registros de eventos y visualizar trazas de las aplicaciones mediante una arquitectura basada en contenedores Docker.
## Tecnologías utilizadas
- **Docker Compose:** despliegue y administración de los servicios.
- **Prometheus:** recopilación y almacenamiento de métricas.
- **Node Exporter:** exposición de métricas del sistema.
- **SNMP Exporter:** recopilación de métricas de red mediante SNMP.
- **SNMP Simulator:** simulación de un dispositivo de red.
- **Grafana:** visualización de métricas y logs mediante dashboards.
- **Loki:** almacenamiento y consulta de logs.
- **Promtail:** recopilación y envío de logs hacia Loki.
- **OpenTelemetry Collector:** recepción y procesamiento de datos de telemetría.
- **Jaeger:** visualización y análisis de trazas distribuidas.
- **HotROD:** aplicación de demostración para generar trazas distribuidas.

## Arquitectura del sistema
El proyecto integra diferentes herramientas que trabajan conjuntamente:
1. Prometheus recopila métricas de Prometheus, Node Exporter y SNMP Exporter.
2. SNMP Exporter consulta al simulador SNMP para obtener métricas de red.
3. Promtail recopila los archivos de logs y los envía a Loki.
4. Grafana permite visualizar las métricas y consultar los logs.
5. HotROD genera trazas que son enviadas al OpenTelemetry Collector.
6. OpenTelemetry Collector procesa las trazas y las envía a Jaeger.

## Estructura del proyecto
```text
taller-observabilidad-final/
│
├── docker-compose.yml
│
├── prometheus/
│   └── prometheus.yml
│
├── promtail/
│   └── promtail-config.yml
│
├── otel/
│   └── otel-collector-config.yml
│
├── snmp/
│   └── snmpd.conf
│
└── logs/
    └── app-cloud.log
```

## Requisitos
- Docker.
- Docker Compose.
- Git (opcional, para clonar el repositorio).

## Instalación y ejecución
Clonar el repositorio:

```bash
git clone https://github.com/leo2121-tech/taller-observabilidad-final.git
```

Ingresar al directorio:
```bash
cd taller-observabilidad-final
```

Levantar los servicios:
```bash
docker compose up -d
```

Verificar el estado de los contenedores:
```bash
docker compose ps
```

Consultar los registros de los servicios:
```bash
docker compose logs -f
```

Detener el entorno:
```bash
docker compose down
```

## Servicios y accesos

| Servicio | Puerto | Función |
|---|---:|---|
| Prometheus | 9090 | Consulta de métricas y estado de targets |
| Grafana | 3000 | Dashboards y visualización |
| SNMP Exporter | 9116 | Exportación de métricas SNMP |
| Node Exporter | 9100 | Métricas del sistema |
| Loki | 3100 | Almacenamiento de logs |
| Jaeger UI | 16686 | Visualización de trazas |
| OpenTelemetry Collector | 4317 | Recepción OTLP gRPC |
| OpenTelemetry Collector | 4318 | Recepción OTLP HTTP |
| HotROD | 8080 | Aplicación de demostración |

## Consultas de métricas
### Prometheus
Estado de los servicios:
```promql
up
```

Uso de CPU:
```promql
100 * (1 - avg by (instance) (
  rate(node_cpu_seconds_total{mode="idle"}[5m])
))
```

Tráfico de red entrante:
```promql
rate(ifInOctets{ifDescr="eth0"}[5m]) * 8 / 1000000
```

Tráfico de red saliente:
```promql
rate(ifOutOctets{ifDescr="eth0"}[5m]) * 8 / 1000000
```

Uso del almacenamiento visible desde el contenedor:
```promql
100 * (
  1 -
  node_filesystem_avail_bytes{mountpoint="/etc/hostname"}
  /
  node_filesystem_size_bytes{mountpoint="/etc/hostname"}
)
```
## Gestión de logs
Promtail recopila los archivos `.log` ubicados en el directorio `logs/` y los envía a Loki.

Los registros utilizan formato JSON y contienen información como:

- `timestamp`: fecha y hora registrada en el evento.
- `level`: nivel del registro.
- `service`: servicio que genera el evento.
- `msg`: descripción del evento.

Consultas LogQL:
Todos los logs:
```logql
{job="cloud-logs"}
```

Errores:

```logql
{job="cloud-logs", level="ERROR"}
```

Advertencias:

```logql
{job="cloud-logs", level="WARN"}
```

Información:

```logql
{job="cloud-logs", level="INFO"}
```

## Trazabilidad distribuida

El sistema utiliza OpenTelemetry Collector para recibir y procesar las trazas generadas por HotROD.
Posteriormente, las trazas son enviadas a Jaeger, donde se pueden analizar:

- Servicios involucrados en una solicitud.
- Duración de las operaciones.
- Relación entre spans.
- Errores y excepciones.
- Problemas de comunicación entre servicios.

Durante las pruebas se identificaron eventos `redis timeout` en spans asociados a Redis, permitiendo observar errores y tiempos de espera dentro de las operaciones distribuidas.

## Configuración SNMP
El simulador SNMP utiliza el archivo:

```text
snmp/snmpd.conf
```
Este archivo configura la comunidad de acceso y las vistas necesarias para consultar métricas del sistema y de las interfaces de red.
Docker Compose debe montar este archivo dentro del contenedor SNMP para que la configuración personalizada se aplique correctamente.

## Objetivo
Implementar una plataforma integrada de observabilidad que permita monitorear infraestructura, analizar métricas, centralizar logs y diagnosticar el comportamiento de aplicaciones mediante trazabilidad distribuida.

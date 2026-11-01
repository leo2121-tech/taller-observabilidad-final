# Informe Técnico: Despliegue y Validación de un Stack de Observabilidad Completo

**Asignatura:*infraestructura ti*
 Taller Observabilidad Infraestructura con Stack Open Source  
**Rol:** Ingeniero SRE  

---

## 1. Paso a Paso Documentado

### 1.1 Preparación y Despliegue del Entorno
Para iniciar la arquitectura completa, se estructuraron los archivos de configuración para cada servicio y se ejecutó el despliegue mediante Docker Compose:

```bash
docker compose up -d
verificacion del estado de los contenedores
docker compose ps

1.2 Validación de Recolección de Métricas (Prometheus, Node Exporter y SNMP)
Ingresar a http://localhost:9090/targets (o desde el puerto reenvíado en Codespaces).

Comprobar que los jobs prometheus, node_exporter y snmp se encuentran en estado UP.

1.3 Validación de Ingesta de Logs (Loki y Promtail)
El contenedor log-generator escribe eventos en formato JSON en ./logs/app-cloud.log. Promtail lee este archivo, ejecuta el pipeline de extracción JSON y envía los flujos a Loki en el puerto 3100.

1.4 Configuración de Grafana, Dashboard y Alerta Webhook
Acceso a Grafana (puerto 3000, credenciales admin / admin).

Fuentes de datos: Conexión exitosa de Prometheus (http://prometheus:9090) y Loki (http://loki:3100).

Contact Point (Webhook): Configuración del canal de notificación apuntando al endpoint de webhook.site.

Regla de Alerta de CPU: Creación de la regla evaluando el consumo de CPU con umbral bajo para forzar el estado Firing.

1.5 Generación y Verificación de Trazas (HotROD, OTEL Collector y Jaeger)
Se accedió a la aplicación de microservicios simulada (HotROD en el puerto 8080) para generar transacciones distribuidas y analizarlas en la interfaz de Jaeger (puerto 16686).

2. Justificación Técnica
2.1 Elección de Métricas y Consultas PromQL
Uso de CPU (node_cpu_seconds_total): Se utilizó la función irate() sobre el modo idle en una ventana de 5 minutos y se restó de 100 para detectar picos rápidos de consumo.

Ancho de Banda (node_network_receive_bytes_total): Al aplicar rate()[5m] sobre los bytes recibidos y multiplicarlo por 8 (llevándolo a bits) dividido por 1.000.000, se obtiene la tasa de transferencia en Mbps.

Patrón Multi-Target en SNMP Exporter: Utiliza relabel_configs para pasar la dirección del agente (snmp-simulator) como parámetro al snmp-exporter, traduciendo OIDs de manera centralizada.

2.2 Pipeline de Promtail e Indexación de Etiquetas (Loki)
Se diseñó un pipeline_stages con la etapa json para extraer las llaves level y service. Indexar el nivel de severidad (level) como etiqueta de baja cardinalidad permite realizar filtros ultrarrápidos en LogQL ({job="cloud-logs", level="ERROR"}) sin penalizar el rendimiento del motor.

2.3 Arquitectura de Trazabilidad con OpenTelemetry Collector
La aplicación envía sus trazas mediante el estándar OTLP hacia el otel-collector. El procesador batch agrupa las trazas en memoria antes de exportarlas a Jaeger, reduciendo la sobrecarga de red y desacoplando la instrumentación del backend.

3. Evidencia de Funcionamiento
3.1 Dashboard Operativo Unificado en Grafana
3.2 Alerta de Consumo de CPU y Recepción en Webhook
3.3 Análisis de Trazas y Cuellos de Botella en Jaeger
Análisis de latencia detectada:

En el servicio customer, se identifica un cuello de botella en la consulta a MySQL (SQL SELECT), bloqueando la ejecución durante más de 300ms.

En el servicio driver, se observan múltiples llamadas secuenciales a Redis (GetDriver) con latencias variables e incidencias de timeout que incrementan el tiempo total de respuesta[cite: 6].

4. Conclusiones y Lecciones Aprendidas
Correlación de los Tres Pilares: Las métricas (Prometheus) alertan el síntoma, los logs (Loki) revelan el detalle del error puntual, y las trazas (Jaeger/OTEL) permiten aislar la latencia exacta a nivel de código o base de datos en arquitecturas distribuidas.

Cardinalidad y Rendimiento: Una correcta estructuración de etiquetas en Promtail y Loki garantiza consultas veloces y un consumo de almacenamiento optimizado.

Estandarización Abierta: OpenTelemetry y el ecosistema open source consolidan una solución robusta, interoperable y libre de vendor lock-in para la observabilidad empresarial.
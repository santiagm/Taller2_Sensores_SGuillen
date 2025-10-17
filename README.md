# Taller 2  ROS2 en Docker y Análisis de Tráfico DDS/RTPS

📘 Descripción general
Este taller tuvo como objetivo comprender la comunicación entre nodos de ROS2 mediante el modelo publish/subscribe, implementando los nodos sensor_node, reader_node y plotter_node dentro de un entorno Docker. 
Posteriormente, se analizó el tráfico de red generado entre los nodos utilizando Wireshark, para identificar los mensajes DDS/RTPS empleados por el middleware de ROS2.

──────────────────────────────────────────────
🧩 1. Creación del entorno Docker
──────────────────────────────────────────────

1.1. Estructura de carpetas en el host
New-Item -ItemType Directory -Path "$HOME\ros2_shared"
New-Item -ItemType Directory -Path "$HOME\ros2_data"

1.2. Creación del Dockerfile
Se define una imagen basada en osrf/ros:jazzy-desktop con colcon y nano instalados.

FROM osrf/ros:jazzy-desktop
RUN apt-get update && apt-get install -y python3-colcon-common-extensions nano
ENV ROS_WS=/root/ros2_ws
RUN mkdir -p ${ROS_WS}/src
WORKDIR ${ROS_WS}
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

1.3. Construcción de la imagen
docker build -t ros2_reto:jazzy .

──────────────────────────────────────────────
⚙️ 2. Creación y montaje de contenedores
──────────────────────────────────────────────

2.1. Ejecución del contenedor principal
docker run -it --name ros2_ws `
  -v "${env:USERPROFILE}\ros2_shared:/ros2_shared" `
  -v "${env:USERPROFILE}\ros2_data:/root/ros2_ws/data" `
  ros2_reto:jazzy

2.2. Verificación de carpetas compartidas
ls /ros2_shared

──────────────────────────────────────────────
🧠 3. Implementación de nodos ROS2
──────────────────────────────────────────────

3.1. Archivos creados
- sensor_node.py → publica lecturas de temperatura simuladas.  
- reader_node.py → recibe y muestra los valores.  
- plotter_node.py → guarda y actualiza una gráfica sensor_plot.png.

3.2. Registro de nodos en setup.py
entry_points={
  'console_scripts': [
      'sensor_node = sensor_program.sensor_node:main',
      'reader_node = sensor_program.reader_node:main',
      'plotter_node = sensor_program.plotter_node:main',
  ],
},

3.3. Compilación del workspace
cd /root/ros2_ws
colcon build
source install/setup.bash

──────────────────────────────────────────────
📡 4. Ejecución de nodos
──────────────────────────────────────────────

4.1. Publicador (nodo sensor)
ros2 run sensor_program sensor_node

4.2. Suscriptor (nodo lector)
ros2 run sensor_program reader_node

4.3. Generador de gráfico
ros2 run sensor_program plotter_node

El gráfico se guarda automáticamente en:
C:\Users\<usuario>\ros2_data\sensor_plot.png

──────────────────────────────────────────────
🔍 5. Análisis de tráfico de red (Taller 3.6)
──────────────────────────────────────────────

5.1. Creación de red Docker
docker network create proyecto
docker network connect proyecto ros2_ws

5.2. Contenedor sniffer
mkdir "$HOME\ros2_pcap"

docker run --network proyecto `
  -v "${env:USERPROFILE}\ros2_pcap:/pcap" `
  --cap-add=NET_ADMIN --cap-add=NET_RAW `
  nicolaka/netshoot tcpdump -i eth0 -w /pcap/trafico_ros2.pcap

5.3. Captura y análisis en Wireshark
1. Abrir trafico_ros2.pcap.
2. Aplicar filtro:
   udp.port >= 7400 && udp.port <= 7500
3. Observar mensajes DDS/RTPS:
   - SPDP → descubrimiento de participantes.  
   - SEDP → descubrimiento de tópicos.  
   - DATA → envío de mensajes.  
   - HEARTBEAT → control de sesión.

──────────────────────────────────────────────
📈 6. Resultados
──────────────────────────────────────────────

- Comunicación exitosa entre los nodos ROS2.
- Visualización de datos generados y graficados en tiempo real.
- Captura y análisis del tráfico UDP DDS/RTPS en red Docker.
- Validación del modelo publish/subscribe de ROS2.

──────────────────────────────────────────────
🧾 7. Conclusiones
──────────────────────────────────────────────

El taller permitió integrar conceptos de virtualización, redes y robótica, demostrando cómo ROS2 utiliza el middleware DDS para establecer comunicación descentralizada entre nodos.  
El uso de Docker simplificó la configuración del entorno y facilitó el intercambio de archivos mediante carpetas compartidas, mientras que Wireshark confirmó el flujo de mensajes entre nodos a nivel de red.

──────────────────────────────────────────────
📚 Referencias
──────────────────────────────────────────────
- Docker Docs – "Sharing local files with containers"
  https://docs.docker.com/get-started/docker-concepts/running-containers/sharing-local-files/
- Spacelift – "Docker Networking: Basics, Network Types & Examples"
  https://spacelift.io/blog/docker-networking

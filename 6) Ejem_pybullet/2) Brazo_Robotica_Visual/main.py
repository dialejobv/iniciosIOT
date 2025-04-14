import pybullet as p
import pybullet_data
import time
import numpy as np
import os

# Configurar la ruta al archivo URDF
# IMPORTANTE: Asegúrate de guardar el archivo URDF anterior en la misma carpeta que este script
robot_urdf_path = "two_joint_robot_custom.urdf"

# Verificar que el archivo existe
if not os.path.exists(robot_urdf_path):
    print(f"ERROR: No se encuentra el archivo {robot_urdf_path}")
    print("Asegúrate de guardar el archivo URDF en la misma carpeta que este script")
    input("Presiona Enter para salir...")
    exit()

# Inicializar PyBullet
p.connect(p.GUI)  # Modo GUI
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)

# Configurar la física y la cámara
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[0, 0, 0.5])

# Cargar el plano y el robot
planeId = p.loadURDF("plane.urdf")
print(f"Intentando cargar robot desde: {robot_urdf_path}")
robotId = p.loadURDF(robot_urdf_path, [0, 0, 0.1], useFixedBase=True)
print(f"Robot cargado con ID: {robotId}")

# Configurar los deslizadores para los joints
joint1_slider = p.addUserDebugParameter("Joint 1", -np.pi, np.pi, 0)
joint2_slider = p.addUserDebugParameter("Joint 2", -np.pi, np.pi, 0)

# Añadir un parámetro para controlar la velocidad de simulación
speed_control = p.addUserDebugParameter("Velocidad", 0.1, 10.0, 1.0)

# Añadir un botón para pausa
pause_button = p.addUserDebugParameter("Pausar/Continuar", 1, 0, 1)
last_pause_value = 1

print("Simulación iniciada. Use los deslizadores para controlar el robot.")
print("Para mantener la ventana abierta, NO cierre este terminal.")

try:
    # Mantener la simulación en ejecución
    while True:
        # Verificar si se presionó el botón de pausa
        current_pause_value = p.readUserDebugParameter(pause_button)
        if current_pause_value != last_pause_value:
            print("Simulación pausada/continuada")
        last_pause_value = current_pause_value

        # Leer valores de los deslizadores
        joint1_value = p.readUserDebugParameter(joint1_slider)
        joint2_value = p.readUserDebugParameter(joint2_slider)
        speed = p.readUserDebugParameter(speed_control)

        # Controlar las articulaciones
        p.setJointMotorControl2(robotId, 0, p.POSITION_CONTROL, targetPosition=joint1_value, force=500)
        p.setJointMotorControl2(robotId, 2, p.POSITION_CONTROL, targetPosition=joint2_value, force=500)

        # Avanzar la simulación
        p.stepSimulation()
        time.sleep(0.01 / speed)  # Ajusta la velocidad de simulación

except KeyboardInterrupt:
    print("Simulación interrumpida por el usuario")
finally:
    # Asegurarse de que la ventana se mantenga abierta hasta que el usuario presione Enter
    input("\nSimulación finalizada. Presiona Enter para cerrar completamente...")
    p.disconnect()
import tkinter as tk
import math
import time

class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output

class LineFollowerCar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.car_x = 400
        self.car_y = 300
        self.car_angle = 0
        self.speed = 4
        self.sensor_distance = 35
        self.sensor_offset = 20
        self.pid = PIDController(1.9, 0.001, 0.8)
        self.last_time = time.time()
        
        # Elementos gráficos
        self.body = self.create_car_body()
        self.left_wheel = self.create_wheel()
        self.right_wheel = self.create_wheel()
        self.sensor_left = self.create_sensor()
        self.sensor_right = self.create_sensor()
        self.update_car()

    def create_car_body(self):
        return self.canvas.create_polygon(
            [0, 0, 50, 0, 50, 30, 0, 30],
            fill='#2E86C1', outline='#1B4F72', width=2
        )
    
    def create_wheel(self):
        return self.canvas.create_oval(
            0, 0, 12, 12,
            fill='#2C3E50', outline='#1B2631'
        )
    
    def create_sensor(self):
        return self.canvas.create_oval(
            0, 0, 8, 8,
            fill='#E74C3C', outline='#922B21'
        )

    def update_car(self):
        angle_rad = math.radians(self.car_angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Actualizar cuerpo (polígono)
        body_coords = [
            self.car_x + 45*cos_angle - 15*sin_angle,
            self.car_y + 25*sin_angle + 15*cos_angle,
            
            self.car_x + 25*cos_angle + 15*sin_angle,
            self.car_y + 25*sin_angle - 15*cos_angle,
            
            self.car_x - 25*cos_angle + 15*sin_angle,
            self.car_y - 25*sin_angle - 15*cos_angle,
            
            self.car_x - 25*cos_angle - 15*sin_angle,
            self.car_y - 25*sin_angle + 15*cos_angle
        ]
        self.canvas.coords(self.body, *body_coords)
        
        # Actualizar ruedas
        wheel_offset = 20
        self.update_wheel(self.left_wheel, -wheel_offset, angle_rad)
        self.update_wheel(self.right_wheel, wheel_offset, angle_rad)
        
        # Actualizar sensores
        sl, sr = self.get_sensor_positions()
        self.canvas.coords(self.sensor_left, sl[0]-2, sl[1]-2, sl[0]+2, sl[1]+2)
        self.canvas.coords(self.sensor_right, sr[0]-2, sr[1]-2, sr[0]+2, sr[1]+2)

    def update_wheel(self, wheel, offset, angle_rad):
        wheel_x = self.car_x + offset * math.sin(angle_rad)
        wheel_y = self.car_y - offset * math.cos(angle_rad)
        self.canvas.coords(wheel, wheel_x-6, wheel_y-6, wheel_x+6, wheel_y+6)

    def get_sensor_positions(self):
        angle_rad = math.radians(self.car_angle)
        front_x = self.car_x + (self.sensor_distance + 25) * math.cos(angle_rad)
        front_y = self.car_y + (self.sensor_distance + 25) * math.sin(angle_rad)
        
        return (
            (front_x - self.sensor_offset * math.sin(angle_rad),
             front_y + self.sensor_offset * math.cos(angle_rad)),
            
            (front_x + self.sensor_offset * math.sin(angle_rad),
             front_y - self.sensor_offset * math.cos(angle_rad))
        )

    def move(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        sl, sr = self.get_sensor_positions()
        left_active = self.check_sensor(*sl)
        right_active = self.check_sensor(*sr)
        
        error = (right_active - left_active) * 10
        steering = self.pid.compute(error, dt)
        
        self.car_angle += steering
        self.car_x += self.speed * math.cos(math.radians(self.car_angle))
        self.car_y += self.speed * math.sin(math.radians(self.car_angle))
        
        self.car_x = max(50, min(self.car_x, 650))
        self.car_y = max(50, min(self.car_y, 550))
        
        self.update_car()

    def check_sensor(self, x, y):
        overlapping = self.canvas.find_overlapping(x-3, y-3, x+3, y+3)
        return any(item in overlapping for item in [track, checkpoint])

# Configuración de ventana
window = tk.Tk()
window.title("Carro Seguidor Mejorado")
canvas = tk.Canvas(window, width=800, height=600, bg='#EAEDED')
canvas.pack()

# Pista
track = canvas.create_rectangle(100, 200, 700, 400, outline='#2C3E50', width=25, fill='#34495E')
checkpoint = canvas.create_oval(350, 190, 450, 210, fill='#27AE60', outline='#229954')

# Inicializar carro
car = LineFollowerCar(canvas)

def game_loop():
    car.move()
    canvas.create_oval(car.car_x-2, car.car_y-2, car.car_x+2, car.car_y+2, fill='#F1C40F', outline='')
    window.after(30, game_loop)

game_loop()
window.mainloop()
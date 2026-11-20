from motor import DCMotor

motor = DCMotor()
hizlar = []
for adim in range(8000):
    akim, hiz = motor.adim(12.0, 0.001)
    hizlar.append(hiz)
print("en yüksek hız:", round(max(hizlar), 2))
print("son hız:", round(hizlar[-1], 2))

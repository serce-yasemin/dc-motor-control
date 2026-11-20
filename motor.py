class DCMotor:
    def __init__(self, R=1.0, L=0.5, Ke=0.5, Kt=0.5, J=0.1, b=0.0):
        self.R, self.L, self.Ke, self.Kt, self.J, self.b = R, L, Ke, Kt, J, b
        self.akim, self.hiz = 0.0, 0.0

    def adim(self, V, dt, yuk=0.0):
        di = (V - self.R * self.akim - self.Ke * self.hiz) / self.L
        dw = (self.Kt * self.akim - self.b * self.hiz - yuk) / self.J
        self.akim += di * dt
        self.hiz += dw * dt
        return self.akim, self.hiz

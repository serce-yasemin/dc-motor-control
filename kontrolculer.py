class PID:
    def __init__(self, kp, ki, kd, dt, sinir=None, a=0.0):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.sinir, self.a = sinir, a
        self.toplam_hata, self.onceki_hata, self.turev_f = 0.0, None, 0.0

    def hesapla(self, hedef, olcum):
        hata = hedef - olcum
        if self.onceki_hata is None:
            self.onceki_hata = hata                                  # kick olmasın
        turev = (hata - self.onceki_hata) / self.dt
        self.turev_f = self.a * self.turev_f + (1 - self.a) * turev  # filtre
        u = (self.kp * hata
             + self.ki * (self.toplam_hata + hata * self.dt)
             + self.kd * self.turev_f)
        u_gercek = u if self.sinir is None else max(-self.sinir, min(self.sinir, u))
        if self.sinir is None or u_gercek == u:                      # anti-windup
            self.toplam_hata += hata * self.dt
        self.onceki_hata = hata
        return u_gercek


class DurumGeriBeslemesi:
    def __init__(self, k1, k2, N, sinir=None):
        self.k1, self.k2, self.N, self.sinir = k1, k2, N, sinir

    def hesapla(self, hedef, akim, hiz):
        V = -self.k1 * akim - self.k2 * hiz + self.N * hedef
        if self.sinir is not None:
            V = max(-self.sinir, min(self.sinir, V))
        return V

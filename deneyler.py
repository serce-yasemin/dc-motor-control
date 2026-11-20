import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from kontrolculer import PID, DurumGeriBeslemesi
from motor import DCMotor


def calistir(kontrolcu, tur, sure=14, dt=0.001, hedef=20, yuk_zamani=7, yuk=0.25):
    motor = DCMotor()
    zamanlar, hizlar, voltajlar = [], [], []
    for adim in range(int(sure / dt)):
        t = adim * dt
        if tur == "ham":
            V = 12.0
        elif tur == "pid":
            V = kontrolcu.hesapla(hedef, motor.hiz)
        else:
            V = kontrolcu.hesapla(hedef, motor.akim, motor.hiz)
        y = yuk if t >= yuk_zamani else 0.0
        motor.adim(V, dt, y)
        zamanlar.append(t)
        hizlar.append(motor.hiz)
        voltajlar.append(V)
    return zamanlar, hizlar, voltajlar


# --- Deney 1: yük altında PI ve durum geri beslemesi (hedef 20, yük t=7 s) ---
sgb = DurumGeriBeslemesi(3, 1.1, 1.6, sinir=12)
pi = PID(1, 2, 0, 0.001, sinir=12)

t1, w1, _ = calistir(sgb, "sgb")
t2, w2, _ = calistir(pi, "pid")
plt.figure()
plt.plot(t1, w1, label="Durum geri beslemesi")
plt.plot(t2, w2, label="PI")
plt.axhline(20, ls="--", c="gray", label="hedef")
plt.axvline(7, ls=":", c="red", label="yük eklendi")
plt.xlabel("zaman (s)")
plt.ylabel("hız (rad/s)")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("deney_yuk.png", dpi=150)
print("son hızlar:", round(w1[-1], 2), round(w2[-1], 2))

# --- Deney 2: ham motor ve durum geri beslemesi (hedef 24, yük yok) ---
sgb_sinirsiz = DurumGeriBeslemesi(3, 1.1, 1.6, sinir=None)
sgb_sinirli = DurumGeriBeslemesi(3, 1.1, 1.6, sinir=12)

durumlar = [
    (None,         "ham",  "Ham motor (sabit 12 V)"),
    (sgb_sinirsiz, "sgb",  "Durum g.b., sınırsız"),
    (sgb_sinirli,  "sgb",  "Durum g.b., 12 V sınırlı"),
]

fig, (ust, alt) = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
for kontrolcu, tur, etiket in durumlar:
    t, w, v = calistir(kontrolcu, tur, sure=6, hedef=24, yuk=0)
    ust.plot(t, w, label=etiket)
    alt.plot(t, v, label=etiket)
    print(f"{etiket}: tepe hız = {max(w):.2f}, en yüksek V = {max(v):.1f}")

ust.axhline(24, ls="--", c="gray")
ust.set_ylabel("hız (rad/s)"); ust.legend(); ust.grid(alpha=.3)
alt.axhline(12, ls=":", c="red", label="sürücü sınırı")
alt.set_ylabel("voltaj (V)"); alt.set_xlabel("zaman (s)"); alt.legend(); alt.grid(alpha=.3)
plt.tight_layout()
plt.savefig("deney_ham_vs_sgb.png", dpi=150)

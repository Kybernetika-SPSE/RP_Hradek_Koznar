import serial
import time
import matplotlib.pyplot as plt

PORT = "COM3"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

times = []
values = []
start = time.time()

plt.ion()

fig, ax = plt.subplots()
line, = ax.plot([], [], marker="o", label="Napětí")

ax.set_title("Napětí v čase")
ax.set_xlabel("Čas [s]")
ax.set_ylabel("Napětí [V]")
ax.set_ylim(0, 20)
ax.grid(True)
ax.legend()

info_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    verticalalignment="top"
)

print("Čtu data...")

while True:
    raw = ser.readline().decode(errors="ignore").strip()

    if not raw:
        plt.pause(0.05)
        continue

    try:
        value = float(raw)
    except ValueError:
        plt.pause(0.05)
        continue

    t = time.time() - start

    times.append(t)
    values.append(value)

    maximum = max(values)
    minimum = min(values)
    average = sum(values) / len(values)

    print(f"{t:.1f}s | {value:.3f} V | max {maximum:.3f} | min {minimum:.3f} | avg {average:.3f}")

    line.set_data(times, values)

    ax.set_xlim(max(0, t - 60), t + 1)

    info_text.set_text(
        f"Aktuálně: {value:.3f} V\n"
        f"Maximum: {maximum:.3f} V\n"
        f"Minimum: {minimum:.3f} V\n"
        f"Průměr: {average:.3f} V"
    )

    fig.canvas.draw_idle()
    plt.pause(0.1)
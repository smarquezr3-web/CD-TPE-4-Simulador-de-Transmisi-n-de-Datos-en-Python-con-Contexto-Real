import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
import random


class SimuladorContextoRealUNEMI:
    def __init__(self, root):
        self.root = root
        self.root.title("PROYECTO: COMUNICACIÓN DE DATOS - UNEMI")
        self.root.state('zoomed')
        self.root.configure(bg="#1e1e2f")

        # --- BASE DE DATOS DE CONTEXTO REAL (Basado en el material de clase) ---
        self.detalles_reales = [
            {
                "ejemplo": "WHATSAPP (WI-FI)",
                "explicacion": "Los bits de tu mensaje se modulan en ondas de radio de 2.4GHz. Aquí aplicas el Subtema 1: Datos digitales viajando en señales analógicas.",
                "teoria": "Teorema de Nyquist: Define la tasa máxima de bits en el aire."
            },
            {
                "ejemplo": "NETFLIX (FIBRA ÓPTICA)",
                "explicacion": "La luz se enciende y apaga (bits) para viajar por el vidrio. Es una señal periódica (Subtema 2) de altísima frecuencia.",
                "teoria": "Ancho de Banda: Es masivo, permitiendo video en 4K sin retrasos."
            },
            {
                "ejemplo": "LLAMADA CELULAR",
                "explicacion": "Tu voz (analógica) se digitaliza para procesarse y luego vuelve a ser onda para salir por la antena.",
                "teoria": "Relación Señal/Ruido (SNR): Si hay interferencia, la calidad de voz baja."
            },
            {
                "ejemplo": "CONTROL DE TV (INFRARROJO)",
                "explicacion": "Pulsas un botón (dato discreto) y un LED emite ráfagas de luz invisible que el TV interpreta.",
                "teoria": "Codificación: Cada botón tiene una secuencia de bits única."
            },
            {
                "ejemplo": "TRANSACCIÓN CAJERO (ATM)",
                "explicacion": "Tus datos bancarios viajan encriptados por cables de cobre usando módems DSL.",
                "teoria": "Ciberseguridad: Como dice el PDF, es una vulnerabilidad compartida en redes públicas."
            }
        ]

        # --- ESTADO DE CONTROL DE TRANSMISIÓN (nuevo) ---
        self.pausado = False
        self.detener = False
        self.transmitiendo = False

        # --- DISEÑO RESPONSIVO ---
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(4, weight=1)

        # 1. Encabezado
        header = tk.Frame(root, bg="#002147", pady=10)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(header, text="UNIVERSIDAD ESTATAL DE MILAGRO (UNEMI)", font=("Helvetica", 16, "bold"), bg="#002147", fg="white").pack()
        tk.Label(header, text="Materia: Comunicación de Datos | Grupo B | TICS 4to Semestre - C1", font=("Helvetica", 10), bg="#002147", fg="#ffcc00").pack()

        # 2. Diferencia de Señales (Subtema 1)
        diff_frame = tk.Frame(root, bg="#2a2a40", pady=10, bd=1, relief=tk.RIDGE)
        diff_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        tk.Label(diff_frame, text="CONCEPTOS CLAVE DE LA UNIDAD 3", font=("Helvetica", 10, "bold"), bg="#2a2a40", fg="#00d2ff").pack()
        info_txt = "Señal Digital: Discreta (0,1) | Señal Analógica: Continua (Ondas) | Teorema de Nyquist: C = 2 * B * log2(L)"
        tk.Label(diff_frame, text=info_txt, font=("Helvetica", 9), bg="#2a2a40", fg="white").pack()

        # 3. NUEVO: Panel de animación de codificación ASCII
        encoding_frame = tk.Frame(root, bg="#2a2a40", pady=10, bd=1, relief=tk.RIDGE)
        encoding_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)

        tk.Label(encoding_frame, text="ANIMACIÓN DE CODIFICACIÓN ASCII", font=("Helvetica", 10, "bold"),
                 bg="#2a2a40", fg="#00d2ff").pack()

        fila_ascii = tk.Frame(encoding_frame, bg="#2a2a40", pady=8)
        fila_ascii.pack()

        tk.Label(fila_ascii, text="Carácter:", bg="#2a2a40", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 3))
        self.lbl_char = tk.Label(fila_ascii, text="-", bg="#1e1e2f", fg="#ffcc00", font=("Consolas", 16, "bold"), width=3)
        self.lbl_char.pack(side=tk.LEFT, padx=5)

        tk.Label(fila_ascii, text="Código ASCII (dec):", bg="#2a2a40", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(15, 3))
        self.lbl_ascii = tk.Label(fila_ascii, text="---", bg="#1e1e2f", fg="#ffcc00", font=("Consolas", 14, "bold"), width=4)
        self.lbl_ascii.pack(side=tk.LEFT, padx=5)

        tk.Label(fila_ascii, text="Binario (8 bits):", bg="#2a2a40", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(15, 8))

        self.bit_boxes = []
        for _ in range(8):
            box = tk.Label(fila_ascii, text="-", width=2, height=1, bg="#1e1e2f", fg="white",
                            font=("Consolas", 12, "bold"), relief=tk.RIDGE, bd=2)
            box.pack(side=tk.LEFT, padx=2)
            self.bit_boxes.append(box)

        # 4. NUEVO: Barra de progreso de la transmisión
        progress_frame = tk.Frame(root, bg="#1e1e2f", pady=5)
        progress_frame.grid(row=3, column=0, sticky="ew", padx=20)

        tk.Label(progress_frame, text="Progreso de la transmisión:", bg="#1e1e2f", fg="white",
                 font=("Arial", 9)).pack(side=tk.LEFT, padx=(10, 10))

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Unemi.Horizontal.TProgressbar", troughcolor="#2a2a40", background="#00d2ff",
                         bordercolor="#2a2a40", lightcolor="#00d2ff", darkcolor="#00d2ff")

        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=400,
                                         mode='determinate', style="Unemi.Horizontal.TProgressbar")
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.lbl_progreso = tk.Label(progress_frame, text="0 / 0 caracteres", bg="#1e1e2f", fg="#33ff33",
                                      font=("Consolas", 9, "bold"))
        self.lbl_progreso.pack(side=tk.LEFT, padx=10)

        # 5. Área de Gráficos
        self.main = tk.Frame(root, bg="#1e1e2f")
        self.main.grid(row=4, column=0, sticky="nsew", padx=20)
        self.main.columnconfigure(0, weight=1)

        self.fig, (self.ax_dig, self.ax_ana) = plt.subplots(2, 1, figsize=(6, 4))
        self.fig.patch.set_facecolor('#2a2a40')
        self.fig.subplots_adjust(hspace=0.6)
        for ax in [self.ax_dig, self.ax_ana]:
            ax.set_facecolor('#1e1e2f')
            ax.tick_params(colors='white', labelsize=8)
            ax.title.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=40)

        # 4. Consola de Vida Real
        self.consola = tk.Text(self.main, height=10, bg="#0d0d0d", fg="#33ff33", font=("Consolas", 10), padx=15, pady=10)
        self.consola.pack(fill=tk.X, padx=40, pady=10)

        # 6. Panel de controles de canal (nuevo): ruido / SNR y simulación de error
        canal_frame = tk.Frame(root, bg="#1e1e2f")
        canal_frame.grid(row=5, column=0, sticky="ew", pady=(0, 5))

        tk.Label(canal_frame, text="Ruido del canal (SNR):", bg="#1e1e2f", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(30, 5))
        self.ruido = tk.DoubleVar(value=0.0)
        tk.Scale(canal_frame, variable=self.ruido, from_=0, to=1.0, resolution=0.05,
                 orient=tk.HORIZONTAL, length=150, bg="#1e1e2f", fg="white",
                 troughcolor="#2a2a40", highlightthickness=0).pack(side=tk.LEFT)

        tk.Label(canal_frame, text="Velocidad (seg/letra):", bg="#1e1e2f", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=(20, 5))
        self.velocidad = tk.DoubleVar(value=2.0)
        tk.Scale(canal_frame, variable=self.velocidad, from_=0.3, to=3.0, resolution=0.1,
                 orient=tk.HORIZONTAL, length=150, bg="#1e1e2f", fg="white",
                 troughcolor="#2a2a40", highlightthickness=0).pack(side=tk.LEFT)

        self.simular_error = tk.BooleanVar(value=False)
        tk.Checkbutton(canal_frame, text="Simular error de bit (ruido en línea)", variable=self.simular_error,
                        bg="#1e1e2f", fg="#ff4b2b", selectcolor="#2a2a40",
                        activebackground="#1e1e2f", activeforeground="#ff4b2b",
                        font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=20)

        # 7. Controles
        footer = tk.Frame(root, bg="#1e1e2f", pady=15)
        footer.grid(row=6, column=0, sticky="ew")

        self.entry_msg = tk.Entry(footer, font=("Arial", 14), width=15, justify='center')
        self.entry_msg.pack(side=tk.LEFT, padx=30)
        self.entry_msg.insert(0, "UNEMI")

        self.btn_tx = tk.Button(footer, text="⚡ TRANSMITIR Y ANALIZAR", command=self.transmitir, bg="#00d2ff", width=25, font=("bold", 10))
        self.btn_tx.pack(side=tk.LEFT, padx=5)

        self.btn_pausa = tk.Button(footer, text="⏸ PAUSAR", command=self.toggle_pausa, bg="#ffcc00", width=10, state=tk.DISABLED)
        self.btn_pausa.pack(side=tk.LEFT, padx=5)

        self.btn_detener = tk.Button(footer, text="⏹ DETENER", command=self.detener_transmision, bg="#ff4b2b", fg="white", width=10, state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=5)

        tk.Button(footer, text="🔄 RESET", command=self.reset, bg="#555577", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(footer, text="💾 EXPORTAR GRÁFICO", command=self.exportar_grafico, bg="#33cc33", fg="white", width=16).pack(side=tk.LEFT, padx=5)

    # ------------------------------------------------------------------
    # UTILIDADES DE CONSOLA
    # ------------------------------------------------------------------
    def log(self, tag, msg, color="#33ff33"):
        self.consola.insert(tk.END, f"[{tag}] ", "bold")
        self.consola.insert(tk.END, f"{msg}\n")
        self.consola.see(tk.END)
        self.root.update()

    # ------------------------------------------------------------------
    # NUEVO: Animación de codificación ASCII (carácter -> decimal -> bits)
    # ------------------------------------------------------------------
    def animar_bits(self, letra, bits):
        self.lbl_char.config(text=letra)
        self.lbl_ascii.config(text=str(ord(letra)))

        # Reinicia las casillas de bits
        for box in self.bit_boxes:
            box.config(text="-", bg="#1e1e2f", fg="white")
        self.root.update()

        # Revela cada bit uno por uno, con un pequeño destello al "transmitirse"
        for idx, bit in enumerate(bits):
            box = self.bit_boxes[idx]
            box.config(text=str(bit), bg="#ffcc00", fg="#1e1e2f")  # destello amarillo = "en tránsito"
            self.root.update()
            if not self.esperar(0.12):
                return False
            color_final = "#33ff33" if bit == 1 else "#555577"
            box.config(bg=color_final, fg="white")
            self.root.update()
        return True

    # ------------------------------------------------------------------
    # NUEVO: Actualizar la barra de progreso general del mensaje
    # ------------------------------------------------------------------
    def actualizar_progreso(self, actual, total):
        porcentaje = (actual / total) * 100 if total else 0
        self.progress['value'] = porcentaje
        self.lbl_progreso.config(text=f"{actual} / {total} caracteres")
        self.root.update()

    # ------------------------------------------------------------------
    # NUEVO: Exportar el gráfico actual como imagen
    # ------------------------------------------------------------------
    def exportar_grafico(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("Imagen PNG", "*.png")],
                                             title="Guardar gráfico de señales")
        if ruta:
            self.fig.savefig(ruta, facecolor=self.fig.get_facecolor())
            messagebox.showinfo("Exportado", f"Gráfico guardado en:\n{ruta}")

    # ------------------------------------------------------------------
    # NUEVO: Control de pausa / reanudación
    # ------------------------------------------------------------------
    def toggle_pausa(self):
        self.pausado = not self.pausado
        self.btn_pausa.config(text="▶ REANUDAR" if self.pausado else "⏸ PAUSAR")
        self.log("SISTEMA", "Transmisión en pausa." if self.pausado else "Transmisión reanudada.")

    # ------------------------------------------------------------------
    # NUEVO: Detener transmisión en curso
    # ------------------------------------------------------------------
    def detener_transmision(self):
        self.detener = True
        self.pausado = False
        self.log("SISTEMA", "Transmisión detenida por el usuario.")

    # ------------------------------------------------------------------
    # NUEVO: espera interrumpible (reemplaza el time.sleep fijo)
    # ------------------------------------------------------------------
    def esperar(self, segundos):
        pasos = max(1, int(segundos / 0.1))
        for _ in range(pasos):
            if self.detener:
                return False
            while self.pausado and not self.detener:
                self.root.update()
                time.sleep(0.1)
            if self.detener:
                return False
            time.sleep(0.1)
            self.root.update()
        return True

    def reset(self):
        self.ax_dig.clear()
        self.ax_ana.clear()
        self.canvas.draw()
        self.consola.delete(1.0, tk.END)
        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED, text="⏸ PAUSAR")
        self.btn_detener.config(state=tk.DISABLED)
        self.pausado = False
        self.detener = False
        self.transmitiendo = False

        # Reinicio del panel de animación ASCII y la barra de progreso
        self.lbl_char.config(text="-")
        self.lbl_ascii.config(text="---")
        for box in self.bit_boxes:
            box.config(text="-", bg="#1e1e2f", fg="white")
        self.progress['value'] = 0
        self.lbl_progreso.config(text="0 / 0 caracteres")

    def transmitir(self):
        texto = self.entry_msg.get().upper()
        if not texto:
            return

        self.detener = False
        self.pausado = False
        self.transmitiendo = True
        self.btn_tx.config(state=tk.DISABLED)
        self.btn_pausa.config(state=tk.NORMAL, text="⏸ PAUSAR")
        self.btn_detener.config(state=tk.NORMAL)
        self.consola.delete(1.0, tk.END)

        huvo_error = False

        for i, letra in enumerate(texto):
            self.ax_dig.clear()
            self.ax_ana.clear()

            # DIGITAL (Subtema 1)
            bits = [int(b) for b in format(ord(letra), '08b')]
            paridad_original = sum(bits) % 2

            # NUEVO: simulación opcional de error de bit por ruido en la línea
            error_en_este_bit = False
            if self.simular_error.get() and random.random() < 0.5:
                idx_error = random.randint(0, len(bits) - 1)
                bits[idx_error] = 1 - bits[idx_error]
                error_en_este_bit = True

            # NUEVO: animación de codificación ASCII (carácter -> decimal -> bits)
            if not self.animar_bits(letra, bits):
                self.log("SISTEMA", "Transmisión interrumpida antes de completarse.")
                break

            self.ax_dig.step(range(len(bits)), bits, where='post', color='#00d2ff', lw=2)
            self.ax_dig.set_title(f"DOMINIO DIGITAL: Carácter '{letra}' procesado en CPU")
            self.ax_dig.set_ylim(-0.2, 1.2)

            # ANALÓGICO (Subtema 2: Señales Periódicas)
            t = np.linspace(0, len(bits), 1000)
            frecuencia = 5
            senal = np.sin(2 * np.pi * frecuencia * t) * np.repeat(bits, 1000 // len(bits))

            # NUEVO: ruido gaussiano sobre la señal analógica (simula SNR bajo)
            nivel_ruido = self.ruido.get()
            if nivel_ruido > 0:
                senal = senal + np.random.normal(0, nivel_ruido, size=senal.shape)

            self.ax_ana.plot(t, senal, color='#ff4b2b', lw=1)
            titulo_analogico = f"MEDIO FÍSICO: Onda Analógica transportando '{letra}'"
            if nivel_ruido > 0:
                titulo_analogico += f"  (ruido={nivel_ruido:.2f})"
            self.ax_ana.set_title(titulo_analogico)

            self.canvas.draw()

            # DETALLE DE VIDA REAL
            detalle = self.detalles_reales[i % len(self.detalles_reales)]
            self.log("ESCENARIO", detalle['ejemplo'])
            self.log("APLICACIÓN", detalle['explicacion'])
            self.log("TEORÍA U3", detalle['teoria'])

            # NUEVO: verificación de paridad por carácter
            paridad_recibida = sum(bits) % 2
            if error_en_este_bit and paridad_recibida != paridad_original:
                self.log("ALERTA", f"ERROR DE PARIDAD DETECTADO en '{letra}' (bit {idx_error} invertido).")
                huvo_error = True
            elif error_en_este_bit:
                self.log("ALERTA", f"Bit invertido en '{letra}', pero no afectó la paridad (error no detectado).")

            self.consola.insert(tk.END, "-" * 60 + "\n")

            # NUEVO: actualizar barra de progreso general del mensaje
            self.actualizar_progreso(i + 1, len(texto))

            if not self.esperar(self.velocidad.get()):
                self.log("SISTEMA", "Transmisión interrumpida antes de completarse.")
                break
        else:
            if huvo_error:
                self.log("SISTEMA", f"Mensaje '{texto}' recibido CON errores de paridad. Se recomienda retransmisión.")
            else:
                self.log("SISTEMA", f"Mensaje '{texto}' recibido. Verificación de paridad OK.")

        self.btn_tx.config(state=tk.NORMAL)
        self.btn_pausa.config(state=tk.DISABLED, text="⏸ PAUSAR")
        self.btn_detener.config(state=tk.DISABLED)
        self.transmitiendo = False


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorContextoRealUNEMI(root)
    root.mainloop()

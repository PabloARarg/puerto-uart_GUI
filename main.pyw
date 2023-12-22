from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from comunicacion_serial import Comunicacion
import collections

class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)

        self.datos_placa = Comunicacion()
        self.actualizar_puertos()

        self.muestra = 2000
        self.datos = 0.0

        self.fig, ax = plt.subplots(facecolor='#090808', dpi=100, figsize=(4, 2))
        plt.title("Grafica de Datos", color='white', size=12, family="Arial")
        ax.tick_params(direction='out', length=5, width=2,
                       colors='white',
                       grid_color='b', grid_alpha=0.5)
        
        ax.grid(True) # Agregar cuadrícula en todo el gráfico

        ax.invert_xaxis() # Invertir el eje x

        self.line, = ax.plot([], [], color='#00ff00', marker=',',
                             linewidth=2, markersize=3)

        self.line2, = ax.plot([], [], color='#a2085c', marker=',',
                              linewidth=2, markersize=1)

        plt.xlim([0, self.muestra])
        plt.ylim([20, 90])

        ax.set_facecolor('#000020')
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['top'].set_color('gray')
        ax.spines['right'].set_color('gray')

        self.datos_señal_uno = collections.deque([0] * self.muestra, maxlen=self.muestra)
        self.datos_señal_dos = collections.deque([0] * self.muestra, maxlen=self.muestra)

        self.widgets()

    def animate(self, i):
        
        self.datos = (self.datos_placa.datos_recibidos.get())
        archivo_texto.write(self.datos + '\n')
        dato = self.datos.split(" ")
        ciclo_trabajo = dato[0]
        set_point = float(dato[1])
        temperatura = float(dato[2])
        numero_muestra = dato[3]
        control_pid = dato[4]

        self.datos_señal_uno.append(set_point)
        self.datos_señal_dos.append(temperatura)
        self.line.set_data(range(self.muestra), self.datos_señal_uno)
        self.line2.set_data(range(self.muestra), self.datos_señal_dos)

        self.duty_cycle.config(text=ciclo_trabajo, bg='#090808', fg='white', font=('Arial', 12, 'bold'))
        self.v_set_point.config(text=dato[1], bg='#090808', fg='#00ff00', font=('Arial', 12, 'bold'))
        self.temperatura.config(text=dato[2], bg='#090808', fg='#a2085c', font=('Arial', 12, 'bold'))
        self.muestras.config(text=numero_muestra, bg='#090808', fg='white', font=('Arial', 12, 'bold'))
        self.pid.config(text=control_pid, bg='#090808', fg='white', font=('Arial', 12, 'bold'))

    def iniciar(self, ):
        self.ani = animation.FuncAnimation(self.fig, self.animate,
                                           interval=1000, blit=False)
        self.bt_graficar.config(state='disabled')
        self.bt_pausar.config(state='normal')
        self.canvas.draw()

    def pausar(self):
        self.ani.event_source.stop()
        self.bt_reanudar.config(state='normal')

    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state='disabled')

    def widgets(self):

        ## define los frames en lo que se divide la interface grafica
        frame = Frame(self.master, bg='#090808', bd=2)
        frame.grid(column=0, columnspan=5, row=0, sticky='nsew')
        frame0 = Frame(self.master, bg='#090808')             
        frame0.grid(column=0, row=1, sticky='nsew')
        frame1 = Frame(self.master, bg='#090808')
        frame1.grid(column=1, row=1, sticky='nsew')
        frame2 = Frame(self.master, bg='#090808')              
        frame2.grid(column=2, row=1, sticky='nsew')
        frame3 = Frame(self.master, bg='#090808')             
        frame3.grid(column=3, row=1, sticky='nsew')
        frame4 = Frame(self.master, bg='#090808')
        frame4.grid(column=4, row=1, sticky='nsew')


        ## establece los tamaños relatitivos de ecpancion de las filar y columas
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=2)
        self.master.columnconfigure(3, weight=2)
        self.master.columnconfigure(4, weight=2)
        self.master.rowconfigure(0, weight=10)
        self.master.rowconfigure(1, weight=1)

        ## define un widget para la grafica y la vincula a un frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(padx=0, pady=0, expand=True, fill='both')

        ## define etiquetas de referencia
        Label(frame0, text='Duty Cycle %', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        Label(frame0, text='Set Point °C', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        Label(frame0, text='Temperatura °C', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        Label(frame0, text='Muestra N°', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        Label(frame0, text='PID', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)

        ## define los valores ingresados por uart
        self.duty_cycle=Label(frame1)
        self.duty_cycle.pack(padx=5, expand=1)
        self.v_set_point=Label(frame1)
        self.v_set_point.pack(padx=5, expand=1)
        self.temperatura=Label(frame1)
        self.temperatura.pack(padx=5, expand=1)
        self.muestras=Label(frame1)
        self.muestras.pack(padx=5, expand=1)
        self.pid=Label(frame1)
        self.pid.pack(padx=5, expand=1)

        ## define  botones
        self.bt_graficar = Button(frame4, text='Graficar', font=('Arial', 12, 'bold'),
                                width=12, bg='#0cbccc', fg='black', command=self.iniciar)
        self.bt_graficar.pack(pady=5, expand=1)

        self.bt_pausar = Button(frame4, state='disabled', text='Pausar', font=('Arial', 12, 'bold'),
                                width=12, bg='#2898ee', fg='black', command=self.pausar)
        self.bt_pausar.pack(pady=5, expand=1)

        self.bt_reanudar = Button(frame4, state='disabled', text='Reanudar', font=('Arial', 12, 'bold'),
                                width=12, bg='#284eee', fg='black', command=self.reanudar)
        self.bt_reanudar.pack(pady=5, expand=1)

        ## extrae informacion de puertos y velocidades
        port = self.datos_placa.puertos
        baud = self.datos_placa.baudrates

        Label(frame2, text='Puertos COM', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        self.combobox_port = ttk.Combobox(frame2, values=port, justify='center', width=12, font='Arial')
        self.combobox_port.pack(pady=0, expand=1)
        self.combobox_port.current(0)

        Label(frame2, text='Baudrates', bg='#090808', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        self.combobox_baud = ttk.Combobox(frame2, values=baud, justify='center', width=12, font='Arial')
        self.combobox_baud.pack(padx=20, expand=1)
        self.combobox_baud.current(3)

        ## establece botones
        self.bt_conectar = Button(frame3, text='Conectar', font=('Arial', 12, 'bold'), width=12, bg='#0cbccc',
                                command=self.conectar_serial)
        self.bt_conectar.pack(pady=5, expand=1)

        self.bt_actualizar = Button(frame3, text='Actualizar', font=('Arial', 12, 'bold'), width=12, bg='#2898ee',
                                    command=self.actualizar_puertos)
        self.bt_actualizar.pack(pady=5, expand=1)

        self.bt_desconectar = Button(frame3, state='disabled', text='Desconectar', font=('Arial', 12, 'bold'),
                                    width=12, bg='#284eee', command=self.desconectar_serial)
        self.bt_desconectar.pack(pady=5, expand=1)

    def actualizar_puertos(self):
        self.datos_placa.puertos_disponibles()

    def conectar_serial(self):
        self.bt_conectar.config(state='disabled')
        self.bt_desconectar.config(state='normal')
        self.bt_graficar.config(state='normal')
        self.bt_reanudar.config(state='disabled')

        self.datos_placa.placa.port = self.combobox_port.get()
        self.datos_placa.placa.baudrate = self.combobox_baud.get()
        self.datos_placa.conexion_serial()

        archivo_texto = open('datos_uart.txt', 'w')

    def desconectar_serial(self):
        self.bt_conectar.config(state='normal')
        self.bt_desconectar.config(state='disabled')
        self.bt_pausar.config(state='disabled')
        archivo_texto.close()
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_placa.desconectar()
    

if __name__ == "__main__":
    archivo_texto = open('datos_uart.txt', 'w')
    ventana = Tk()
    ventana.geometry('742x535')
    ventana.config(bg='#090808', bd=4)
    ventana.wm_title('Terminal Grafica')
    ventana.minsize(width=700, height=400)  # Corregido el nombre de 'minisize' a 'minsize'
    ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='logo.png'))
    app = Grafica(ventana)
    app.mainloop()
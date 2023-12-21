from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from comunicacion_serial import Comunicacion
import collections

class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)

        self.datos_arduino = Comunicacion()
        self.actualizar_puertos()

        self.muestra = 1000
        self.datos = 0.0

        self.fig, ax = plt.subplots(facecolor='black', dpi=100, figsize=(4, 2))
        plt.title("Graficar Datos", color='white', size=12, family="Arial")
        ax.tick_params(direction='out', length=5, width=2,
                       colors='white',
                       grid_color='b', grid_alpha=0.5)

        self.line, = ax.plot([], [], color='m', marker='o',
                             linewidth=2, markersize=1, markeredgecolor='m')

        self.line2, = ax.plot([], [], color='g', marker='o',
                              linewidth=2, markersize=1, markeredgecolor='g')

        plt.xlim([0, self.muestra])
        plt.ylim([-1, 6])

        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color('blue')
        ax.spines['left'].set_color('blue')
        ax.spines['top'].set_color('blue')
        ax.spines['right'].set_color('blue')

        self.datos_señal_uno = collections.deque([0] * self.muestra, maxlen=self.muestra)
        self.datos_señal_dos = collections.deque([0] * self.muestra, maxlen=self.muestra)

        self.widgets()

    def animate(self, i):
        self.datos = (self.datos_arduino.datos_recibidos.get())
        dato = self.datos.split(",")
        dato1 = float(dato[0])
        dato2 = float(dato[1])

        self.datos_señal_uno.append(dato1)
        self.datos_señal_dos.append(dato2)
        self.line.set_data(range(self.muestra), self.datos_señal_uno)
        self.line2.set_data(range(self.muestra), self.datos_señal_dos)

        # return self.line, self.line2

    def iniciar(self, ):
        self.ani = animation.FuncAnimation(self.fig, self.animate,
                                           interval=100, blit=False)
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
        frame = Frame(self.master, bg='gray50', bd=2)
        frame.grid(column=0, columnspan=4, row=0, sticky='nsew')
        frame1 = Frame(self.master, bg='white')
        frame1.grid(column=3, row=1, sticky='nsew')
        frame4 = Frame(self.master, bg='red')
        frame4.grid(column=0, row=1, sticky='nsew')
        frame2 = Frame(self.master, bg='blue')              
        frame2.grid(column=1, row=1, sticky='nsew')
        frame3 = Frame(self.master, bg='green')             
        frame3.grid(column=2, row=1, sticky='nsew')

        ## establece los tamaños relatitivos de ecpancion de las filar y columas
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(0, weight=15)
        self.master.rowconfigure(1, weight=1)

        ## define un widget para la grafica y la vincula a un frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(padx=0, pady=0, expand=True, fill='both')

        ## define  botones
        self.bt_graficar = Button(frame4, text='Graficar Datos', font=('Arial', 12, 'bold'),
                                width=12, bg='purple4', fg='white', command=self.iniciar)
        self.bt_graficar.pack(pady=5, expand=1)

        self.bt_pausar = Button(frame4, state='disabled', text='Pausar', font=('Arial', 12, 'bold'),
                                width=12, bg='salmon', fg='white', command=self.pausar)
        self.bt_pausar.pack(pady=5, expand=1)

        self.bt_reanudar = Button(frame4, state='disabled', text='Reanudar', font=('Arial', 12, 'bold'),
                                width=12, bg='green', fg='white', command=self.reanudar)
        self.bt_reanudar.pack(pady=5, expand=1)

        '''
        ## define una imagen
        self.logo = PhotoImage(file='logo1.png')
        Label(frame2, text='Control Analógico', font=('Arial', 15), bg='black', fg='white').pack(padx=5, expand=1)
        ## define la barras laterales
        style = ttk.Style()
        style.configure("Horizontal.TScale", background='black')

        self.slider_uno = ttk.Scale(frame2, command=self.dato_slider_uno, state='disabled', to=255,
                                    from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_uno.pack(pady=5, expand=1)

        self.slider_dos = ttk.Scale(frame2, command=self.dato_slider_dos, state='disabled', to=255,
                                    from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_dos.pack(pady=5, expand=1) 
        #'''

        port = self.datos_arduino.puertos
        baud = self.datos_arduino.baudrates

        Label(frame2, text='Puertos COM', bg='black', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        self.combobox_port = ttk.Combobox(frame2, values=port, justify='center', width=12, font='Arial')
        self.combobox_port.pack(pady=0, expand=1)
        self.combobox_port.current(0)

        Label(frame2, text='Baudrates', bg='black', fg='white', font=('Arial', 12, 'bold')).pack(padx=5, expand=1)
        self.combobox_baud = ttk.Combobox(frame2, values=baud, justify='center', width=12, font='Arial')
        self.combobox_baud.pack(padx=20, expand=1)
        self.combobox_baud.current(3)

        self.bt_conectar = Button(frame3, text='Conectar', font=('Arial', 12, 'bold'), width=12, bg='green2',
                                command=self.conectar_serial)
        self.bt_conectar.pack(pady=5, expand=1)

        self.bt_actualizar = Button(frame3, text='Actualizar', font=('Arial', 12, 'bold'), width=12, bg='magenta',
                                    command=self.actualizar_puertos)
        self.bt_actualizar.pack(pady=5, expand=1)

        self.bt_desconectar = Button(frame3, state='disabled', text='Desconectar', font=('Arial', 12, 'bold'),
                                    width=12, bg='red2', command=self.desconectar_serial)
        self.bt_desconectar.pack(pady=5, expand=1)


        #Label(frame3, image=self.logo, bg='black').pack(pady=5, expand=1)

    def actualizar_puertos(self):
        self.datos_arduino.puertos_disponibles()

    def conectar_serial(self):
        self.bt_conectar.config(state='disabled')
        self.bt_desconectar.config(state='normal')
        #self.slider_uno.config(state='normal')
        #self.slider_dos.config(state='normal')
        self.bt_graficar.config(state='normal')
        self.bt_reanudar.config(state='disabled')

        self.datos_arduino.arduino.port = self.combobox_port.get()
        self.datos_arduino.arduino.baudrate = self.combobox_baud.get()
        self.datos_arduino.conexion_serial()

    def desconectar_serial(self):
        self.bt_conectar.config(state='normal')
        self.bt_desconectar.config(state='disabled')
        self.bt_pausar.config(state='disabled')
        #self.slider_uno.config(state='disabled')
        #self.slider_dos.config(state='disabled')
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_arduino.desconectar()
    
    '''
    def dato_slider_uno(self, *args):
        dato = '1,' + str(int(self.slider_uno.get()))
        self.datos_arduino.enviar_datos(dato)

    def dato_slider_dos(self, *args):
        dato = '2,' + str(int(self.slider_dos.get()))
        self.datos_arduino.enviar_datos(dato)
    #'''
if __name__ == "__main__":
    ventana = Tk()
    ventana.geometry('742x535')
    ventana.config(bg='gray30', bd=4)
    ventana.wm_title('Grafica Matplotlib Animacion')
    ventana.minsize(width=700, height=400)  # Corregido el nombre de 'minisize' a 'minsize'
    ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='logo.png'))
    app = Grafica(ventana)
    app.mainloop()
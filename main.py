# -----------------------------------------------------
# Importy knihoven
# -----------------------------------------------------
#core
import ctypes
import os
import csv
import sys
import threading
import time
from queue import Queue
from collections import deque
import struct

#Grafika
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QAction, QLineEdit, QDialog, QFileDialog, QSpinBox, QGroupBox, QFormLayout, QSlider, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsProxyWidget, QComboBox, QSplitter, QDoubleSpinBox, QTabWidget, QMessageBox, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, Qt
from qtwidgets import Toggle

#matematika, grafy
import numpy as np
import pyqtgraph as pg
import math

#pro ukládání dat, konfiguračních souborů
import datetime
import json
import logging

#Pro spouštění Netcans
import psutil       
import subprocess


# -----------------------------------------------------
# Backend
# -----------------------------------------------------
class Can:
    """
    Backendová třída pro komunikaci s CANOpen zařízením.
    Umožňuje čtení a zápis PDO/SDO dat, zpracování bufferů a výpočet spektra.
    """
    def __init__(self, can_file_name = "fnc.can", can_ID = 47, parent_gui=None):
        """
        Inicializuje CAN komunikaci, načte knihovnu, nastaví buffery a spustí potřebné procesy.
        Vyžaduje:
         - aplikaci netcansb.exe v netcans/netcansb.exe
         - konfigurační .can soubor
         - CANUSB32 DLL knihovnu
        """
        #Konstanty
        self.process_name = "netcansb.exe" #Aplikace Netcans je nutná ke komunikaci s lokální can sítí.
        self.app_path = "netcans\\netcansb.exe"
        self.can_file_name = can_file_name  # Cesta k .can souboru
        self.enable_can_tx = False #Na začátku deaktivované odesílání
        
        #Odkaz na rodiče - pro spouštění GUI funkcí a čtení hodnot
        self.parent_gui = parent_gui

        #Inicializace canUSB32 knihovny
        try:
            self.can_dll = ctypes.cdll.LoadLibrary(os.getcwd() + "\\canusb32.dll")
            logging.info("canusb32.dll loaded successfully")
        except:
            exit("[ERROR] canUSB32.DLL loading error")

        if self.can_dll.CANInit(ctypes.c_char_p(self.can_file_name.encode('utf-8'))):
            logging.info("Can init OK")
        else:
            exit("[ERROR] Can init error")

        #Proměnné pro běh programu
        self.DTO_ID = can_ID #DTO ID
        self.CANOpenData = (ctypes.c_uint8 * 8)() #buffer pro data z CANu
        self.rx_stop_event = threading.Event()  # Událost pro správu zastavení vlákna
        self.toggle = True  # Přepínač pro běh vlákna
        self.toggle_event = threading.Event()  # Event pro správu přerušení smyčky
        self.device_connected = True #tag jestli je zařízení připojeno
        
        #délky bufferů
        self.phase_A_rad_buffer_length = 2000
        self.dFTW_out_buffer_length = 2000
        self.I_buffer_length = 100
        self.Q_buffer_length = self.I_buffer_length

        #Proměnné pro data ze zařízení a buffery pro některé proměnné
        # ============== PDO1 ===============
        self.phase_A = ctypes.pointer(ctypes.c_int32())
        self.phase_A_rad = 0
        #buffer pro fázová data
        self.phase_A_rad_buffer = deque(maxlen=self.phase_A_rad_buffer_length)  # buffer_length
        self.I_A = ctypes.pointer(ctypes.c_int16())
        self.Q_A = ctypes.pointer(ctypes.c_int16())
        # Buffery pro I a Q
        self.I_buffer = deque(maxlen=self.I_buffer_length)  # Maximální délka bufferu
        self.Q_buffer = deque(maxlen=self.Q_buffer_length)  # Maximální délka bufferu
        # ============= PDO2 =================
        self.dFTW_out = ctypes.pointer(ctypes.c_int32())
        self.DA1_out = ctypes.pointer(ctypes.c_int16())
        self.DA2_out = ctypes.pointer(ctypes.c_int16())
        # ============= PDO3 ================
        self.DDS_mHz = ctypes.pointer(ctypes.c_int32())
        self.DDS_Hz = 0
        self.dFTW_out_buffer = deque(maxlen=self.dFTW_out_buffer_length)  # buffer_length
        self.dF_mHz = ctypes.pointer(ctypes.c_int32())
        self.dF_Hz = 0
        # ============= PDO4 ===============
        self.CH1_mag = ctypes.pointer(ctypes.c_uint16())
        self.CH2_mag = ctypes.pointer(ctypes.c_uint16())
        self.act_chan = ctypes.pointer(ctypes.c_uint8())
        # ============= SDO ================
        self.sdo_command = ctypes.pointer(ctypes.c_uint8())
        self.sdo_index = ctypes.pointer(ctypes.c_uint16())
        self.sdo_subindex = ctypes.pointer(ctypes.c_uint8())
        self.sdo_data = ctypes.pointer(ctypes.c_uint32())

        #Fronta pro odesílání
        self.tx_queue = Queue()

        # Spouštění Netcans, pokud už neběží
        if not self.is_process_running(self.process_name):
            logging.info(f"Launching {self.process_name}")
            self.launch_application(self.app_path)
        else:
            logging.info(f"{self.process_name} already running")
    
    def set_phase_A_rad_buffer_length(self, N):
        """Nastaví délku bufferu phase_A_rad a vytvoří nový buffer délky N."""
        self.phase_A_rad_buffer_length = N
        self.phase_A_rad_buffer = deque(maxlen=N)

    def set_dFTW_out_buffer_length(self, N):
        """Nastaví délku bufferu DDS_Hz a vytvoří nový buffer délky N"""
        self.dFTW_out_buffer_length = N
        self.dFTW_out_buffer = deque(maxlen=N)
    
    def set_IQ_buffer_length(self, N):
        """Nastaví délku bufferů I a Q a vytvoří nové buffery délky N."""
        self.I_buffer_length = N
        self.Q_buffer_length = N
        self.I_buffer = deque(maxlen=N)
        self.Q_buffer = deque(maxlen=N)

    @staticmethod
    def channelID(rx_tx: str, CANOpenID: int, dataObject: int) -> int:
        """
        Vypočítá číslo kanálu pro komunikaci podle typu (rx/tx), CANOpenID a čísla objektu.
        """
        return 128 + 256 * (dataObject if dataObject in [1, 2, 3, 4] else 5) + (128 if rx_tx == 'tx' else 0) + CANOpenID

    @staticmethod
    def subChannelID(CANOpenID: int, variable: int) -> int:
        """
        Vypočítá číslo subkanálu pro daný CANOpenID a proměnnou.
        """
        return 10000 + 100 * CANOpenID + variable
    
    def is_process_running(self, process_name):
        """Zjistí, zda běží proces se zadaným názvem."""
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                return True
        return False
    
    def is_device_connected(self):
        """
        Pokusí se přečíst název zařízení přes SDO.
        Vrací True pokud zařízení odpoví, jinak False.
        """
        try:
            # Odeslání SDO požadavku na čtení indexu 0x1008 (device name)
            self.can_rx_SDO(CANOpenID=self.DTO_ID, index=0x1008, subindex=0)
            time.sleep(0.1)
            value = self.sdo_data.contents.value
            connected = (value != 0)
            if connected == True and self.device_connected == False:
                logging.info(f"Device connected")                
            self.device_connected = connected
            return value != 0 
        except Exception as e:
            logging.error(f"{e}")
            return False
        

    def launch_application(self, app_path):
        """Spustí externí aplikaci s danou cestou."""
        app_dir = os.path.dirname(app_path)  # Získá adresář aplikace
        try:
            subprocess.Popen(app_path, cwd=app_dir, shell=False)  # Nastaví pracovní adresář
            logging.info(f"Successfully launched {app_path} from {app_dir}")
        except Exception as e:
            logging.error(f"Error launching {app_path}: {e}")

    def can_rx_thread(self, CANOpenID, timeout=10.0):
        """
        Hlavní smyčka pro příjem dat z CAN sběrnice.
        Zpracovává PDO a SDO zprávy, ukládá je do bufferů.
        """
        def PDO_rx_ID (PDO_number=1):
            return Can.channelID('rx', CANOpenID=CANOpenID, dataObject=PDO_number)
        def PDO_rx_ChanNum(variable=1):
            return Can.subChannelID(CANOpenID=CANOpenID, variable=variable)
        
        #Výpočet adres PDO1-4 a SDO
        pdo_id_1 = PDO_rx_ID(1)
        pdo_id_2 = PDO_rx_ID(2)
        pdo_id_3 = PDO_rx_ID(3)
        pdo_id_4 = PDO_rx_ID(4)
        sdo_id = Can.channelID('rx', CANOpenID=CANOpenID, dataObject=5)

        n_received = 0
        start_time = time.time()
        while not self.rx_stop_event.is_set(): #smyčka aktivní jen když není flagnuté zastavení
            # Zpracování odesílací fronty
            if self.enable_can_tx:
                self.process_tx_queue()

            chan = self.can_dll.CANReadChanNum()

            if not chan:
                #Pokud dlouho nepřichází data, ukončí se smyčka
                if time.time() - start_time > timeout:
                    self.sdo_data.contents.value = 0
                    if self.device_connected == True:
                        logging.warning(f"Device disconnected")
                    self.device_connected = False
                    
                    return None  # Timeout vypršel
                time.sleep(0.001)
                #print(f"\rID: {self.DTO_ID}, phase_A: {self.phase_A.contents.value}, I_A: {self.I_A.contents.value}, Q_A: {self.Q_A.contents.value}, n_received: {n_received}    ", end='')
                continue
            else:
                if self.device_connected == False:
                    self.device_reconnected = True
                self.device_connected = True
                start_time = time.time()
                #Funkce ve smyčce vyčítá číslo kanálu a přiřazuje data z daného kanálu a subkanálu do správných proměnných
                if chan == pdo_id_1:
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(1), self.CANOpenData)
                    self.rx_data_sort(self.phase_A)
                    n_received += 1
                    self.phase_A_rad = self.phase_A.contents.value*(2 * math.pi / 65536)
                    self.phase_A_rad_buffer.append(self.phase_A_rad)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(2), self.CANOpenData)
                    self.rx_data_sort(self.I_A)
                    self.I_buffer.append(self.I_A.contents.value)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(3), self.CANOpenData)
                    self.rx_data_sort(self.Q_A)
                    self.Q_buffer.append(self.Q_A.contents.value)
                elif chan == pdo_id_2:
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(4), self.CANOpenData)
                    self.rx_data_sort(self.dFTW_out)
                    self.dFTW_out_buffer.append(self.dFTW_out.contents.value)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(5), self.CANOpenData)
                    self.rx_data_sort(self.DA1_out)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(6), self.CANOpenData)
                    self.rx_data_sort(self.DA2_out)
                elif chan == pdo_id_3:
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(7), self.CANOpenData)
                    self.rx_data_sort(self.DDS_mHz)
                    self.DDS_Hz = self.DDS_mHz.contents.value/1000
                    
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(8), self.CANOpenData)
                    self.rx_data_sort(self.dF_mHz)
                    self.dF_Hz = self.dF_mHz.contents.value/1000
                elif chan == pdo_id_4:
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(9), self.CANOpenData)
                    self.rx_data_sort(self.CH1_mag)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(10), self.CANOpenData)
                    self.rx_data_sort(self.CH2_mag)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(11), self.CANOpenData)
                    self.rx_data_sort(self.act_chan)
                elif chan == sdo_id:
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(15), self.CANOpenData)
                    self.rx_data_sort(self.sdo_command)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(16), self.CANOpenData)
                    self.rx_data_sort(self.sdo_index)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(17), self.CANOpenData)
                    self.rx_data_sort(self.sdo_subindex)
                    self.can_dll.CANReadChan(PDO_rx_ChanNum(18), self.CANOpenData)
                    self.rx_data_sort(self.sdo_data)
                    #print(f"SDO command: {self.sdo_command.contents.value}, index: {self.sdo_index.contents.value}, subindex: {self.sdo_subindex.contents.value}, data: {self.sdo_data.contents.value}")   
                if self.parent_gui.quick_data_logging and self.parent_gui.data_logging_enabled:
                    self.write_data_log_row_can()
        return 1
    def stop_rx(self):
        """Nastaví událost pro zastavení přijímacího vlákna."""
        self.rx_stop_event.set()  # Nastavení události k zastavení vlákna

    def can_tx_PDO1(self, CANOpenID = 47, data1 = 0, data2 = 0, data3 = 0):
        """Přidá požadavek na zápis PDO1 do odesílací fronty."""
        self.tx_queue.put(("PDO1", CANOpenID, data1, data2, data3))

    def can_tx_SDO(self, CANOpenID = 47, index = 8206, subindex = 6, data = 666):
        """Přidá požadavek na zápis SDO do odesílací fronty."""
        self.tx_queue.put(("SDO", CANOpenID, index, subindex, data))

    def process_tx_queue(self):
        """Zpracuje všechny požadavky v odesílací frontě."""
        while not self.tx_queue.empty():
            request = self.tx_queue.get()
            if request[0] == "SDO":
                _, CANOpenID, index, subindex, data = request
                channel = CANOpenID + 1536
                command = struct.pack('B', 43)
                pack_index = struct.pack('H', index)
                pack_subindex = struct.pack('B', subindex)
                pack_data = struct.pack('I', data)
                packet = command + pack_index + pack_subindex + pack_data
                self.can_dll.CANWriteChan(channel, packet)
                self.can_dll.CANWriteChanNum(channel)
                #print(f"[INFO] SDO command sent: {command}, index: {index}, subindex: {subindex}, data: {data}")
            elif request[0] == "PDO1":
                _, CANOpenID, data1, data2, data3 = request
                channel = Can.channelID('tx', CANOpenID=CANOpenID, dataObject=1)
                var1 = struct.pack('h', data1)
                var2 = struct.pack('h', data2)
                var3 = struct.pack('I', data3)
                packet = var1 + var2 + var3
                self.can_dll.CANWriteChan(channel, packet)
                self.can_dll.CANWriteChanNum(channel)
                #print(f"[INFO] PDO1 command sent: {packet}, data1: {data1}, data2: {data2}, data3: {data3}")

    def can_rx_SDO(self, CANOpenID = 47, index = 8206, subindex = 6):
        """Odešle požadavek na čtení SDO hodnoty z CAN zařízení."""
        channel = CANOpenID + 1536
        command = struct.pack('B', 64) #64 = čtení
        pack_index = struct.pack('H', index)
        pack_subindex = struct.pack('B',subindex)

        packet = command+pack_index+pack_subindex
        #print(packet)
        
        self.can_dll.CANWriteChan(channel, packet)
        self.can_dll.CANWriteChanNum(channel)
    
    def start_rx_thread(self):
        """Spustí přijímací vlákno pro CAN komunikaci."""
        self.toggle_event.clear()
        self.rx_stop_event.clear()
        self.DTO_thread = threading.Thread(target=self.load_dto_rx, daemon=True)
        self.DTO_thread.start()
        logging.info("RX thread started")
        
    def stop_rx_thread(self):
        """Zastaví přijímací vlákno pro CAN komunikaci."""
        if self.DTO_thread and self.DTO_thread.is_alive():
            self.stop_rx()
            self.toggle_event.set()
            self.DTO_thread.join()
            logging.info("RX thread stopped")

    def load_dto_rx(self):
        """Načte data z CAN bufferu do příslušných proměnných"""
        while not self.toggle_event.is_set():
            self.can_rx_thread(self.DTO_ID)

    def rx_data_sort(self, *variables):
        """Zkopíruje data z self.CANOpenData do proměnných podle jejich typu."""
        index = 0  # Ukazatel na aktuální pozici v CANOpenData

        for arg in variables:
            size = ctypes.sizeof(arg.contents)  # Velikost dat [Byte]
            
            # Zabrání přetečení velikosti bufferu
            if index + size > len(self.CANOpenData):
                logging.warning(f"Not enough data for {arg}. Skipping...")
                continue

            # Zkopírování dat do struktury
            ctypes.memmove(ctypes.addressof(arg.contents), ctypes.addressof(self.CANOpenData) + index, size)

            index += size
    
    def calculate_spectral_data(self, buffer, target_length, set_buffer_length, time_interval_sec = 10, sample_period_ms = 5, window_type='Hanning'):
        """
        Spočítá spektrum z bufferu a vrátí frekvenční osu a spektrum v dB.
        Args:
            buffer: vstupní data (deque)
            target_length: délka bufferu
            set_buffer_length: funkce pro nastavení délky bufferu
            time_interval_sec: délka časového úseku pro výpočet (s)
            sample_period_ms: perioda vzorkování (ms)
            window_type: typ okna ('Hanning', 'Hamming', 'Blackman', 'Rectangular')
        Returns:
            freq: frekvenční osa
            magnitude_dB: amplitudové spektrum v dB
            psd_dB: výkonové spektrum v dB
        """
        sample_period = sample_period_ms / 1000.0 # Převede milisekundy na sekundy
        
        N = int(time_interval_sec / sample_period) #Počet vzorků v daném časovém intervalu
        
        if target_length != N:   #Pokud  buffer není délky N, nastaví se na N
            set_buffer_length(N)
        
        if len(buffer) < N: #Pokud v bufferu není dostatek dat, vrátí None
            return None            
        else:
            #https://www.youtube.com/watch?v=pfjiwxhqd1M - jak správně počítat FFT
            
            signal = np.array(list(buffer)[-N:]) # použije posledních N vzorků z bufferu
            signal = signal-np.mean(signal) # Odstranění DC složky (průměr signálu)
            half = N // 2 #délka jednosměrného spektra

            # 1. Oknování signálu
            # Výběr okna podle parametru
            if window_type == 'Hanning':
                window = np.hanning(N)
            elif window_type == 'Hamming':
                window = np.hamming(N)
            elif window_type == 'Blackman':
                window = np.blackman(N)
            elif window_type == 'Rectangular':
                window = np.ones(N)
            else:
                raise ValueError(f"Neznámý typ okna: {window_type}")

            windowed_signal = signal * window # Aplikace okna na signál

            # 2. Výpočet FFT
            fft_result = np.fft.fft(windowed_signal) 

            # 3. Výpočet normalizačního faktoru U
            U = np.sum(window**2)  # normalization factor for PSD calculation (Energy of the window)

            # 4. Výpočet výkonové spektrální hustoty (PSD)
            #https://www.mathworks.com/help/signal/ref/enbw.html#btrjo7i-5?s_eid=PSM_15028
            psd = (np.abs(fft_result[:half]) ** 2) * (sample_period / U)  #jednostranné spektrum výkonové hustoty děleno normalizačním faktorem U
            psd[1:-1] *= 2 #Hodnoty jednostranného spektra kromě prvního a posledního vzorku (DC a Nyquist) musí být vynásobeny 2
            psd_dB = 10 * np.log10(psd + 1e-12) #převod na dB a ochrana proti log(0)

            # 5. calculation of amplitude spectrum
            magnitude = np.abs(fft_result[:half]) / np.sum(window)   #jednostranné spektrum amplitudy děleno součtem okna (amplitudový normalizační faktor)
            magnitude[1:-1] *= 2  #Hodnoty jednostranného spektra kromě prvního a posledního vzorku (DC a Nyquist) musí být vynásobeny 2
            magnitude_dB = 20 * np.log10(magnitude + 1e-12) #převod na dB a ochrana proti log(0)

            #6. Calculation of frequency axis
            freq = np.fft.fftfreq(N, d=sample_period)   #frekvenční osa pro N vzorků a periodu vzorkování
            freq = freq[:half]                          #převede na frekvenční osu jednostranného spektra

            #7. nastavení nulových hodnot pro DC
            magnitude_dB[0] = 0
            psd_dB[0] = 0
            return freq, magnitude_dB, psd_dB
        
    def write_data_log_row_can(self):
        """Zapíše řádek s daty do log souboru při rychlém logování."""
        if self.device_connected:
            values = []
            now = datetime.datetime.now()
            timestamp = now.time().isoformat()
            values.append(timestamp)
            for var in self.parent_gui.data_log_variables:
                value = getattr(self, var, "")
                # Pokud je to pointer, vezmi .contents.value
                if hasattr(value, "contents"):
                    value = value.contents.value
                values.append(str(value))
            self.parent_gui.data_log_file.write(self.parent_gui.data_log_separator.join(values) + "\n")
            self.parent_gui.data_log_file.flush()

# -----------------------------------------------------
# Frontend
# -----------------------------------------------------
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #Nastavovací proměnné
        self.can_file_name = "fnc.can"  # Cesta k .can souboru
        self.history_seconds = 10
        self.update_interval_ms = 200
        self.n_samples = 1000 * self.history_seconds // self.update_interval_ms
        self.phase_integration_time = 10  # Výchozí integrační čas v s
        self.DDS_integration_time = 20  # Výchozí integrační čas v s
        self.phase_window_type = 'Hanning'  # Výchozí typ okna pro spektrum
        self.DDS_window_type = 'Hanning'

        self.PDO1_Tsamp = 0.005
        self.PDO2_Tsamp = 0.010
        self.PDO3_Tsamp = 1.000
        self.PDO4_Tsamp = 0.050
        self.DDS_ref_freq = 20000000
        self.DDS_ref_freq_multiplier = 20
        self.fclk = self.DDS_ref_freq * self.DDS_ref_freq_multiplier
        self.DDS_frequency_step = self.fclk/(2**32)

        self.spectrum_update_interval_ms = 1000  # Výchozí perioda obnovení spekter v ms
        self.IQ_plot_update_interval_ms = 60  # Výchozí perioda obnovení IQ grafu v ms
        self.IQ_plot_history_samples = 100

        #Logování dat
        self.data_logging_enabled = False
        self.quick_data_logging = False
        self.data_log_variables = ["phase_A_rad", "DDS_Hz"]
        self.data_log_interval_ms = 200
        self.data_log_path = "data_log.csv"
        self.data_log_separator = ";"
        self.data_log_duration_s = 0
        self.data_log_remaining_s = 0

        #Verze aplikace
        self.app_version = "0.2"

        #Logování eventů
        self.event_log_path = "trosca.log"
        self.setup_DTO_ID = 47
        #3D text: https://patorjk.com/software/taag/#p=display&v=0&f=Sub-Zero&t=Trosca
        #font: "Sub-Zero" font by Sub-Zero
        print(" ______   ______     ______     ______     ______     ______\n/\__  _\ /\  == \   /\  __ \   /\  ___\   /\  ___\   /\  __ \   \n\/_/\ \/ \ \  __<   \ \ \/\ \  \ \___  \  \ \ \____  \ \  __ \  \n   \ \_\  \ \_\ \_\  \ \_____\  \/\_____\  \ \_____\  \ \_\ \_\ \n    \/_/   \/_/ /_/   \/_____/   \/_____/   \/_____/   \/_/\/_/")
        
        self.load_app_config()
        self.setup_logging()
        self.log_plain(f"________________________________________________________________\nTrosca v{self.app_version} started. Hello")
        
        # Inicializace dalších atributů
        self.can = Can(self.can_file_name, self.setup_DTO_ID, parent_gui=self)
        self.oscillator_settings_window = None  # Okno Nastavení oscilátoru
        self.DTO_param_table_window = None

        # Window setup
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowTitle('TrOSCa')
        self.setGeometry(50, 50, 800, 600)
        self.accent_color = '#04D9FF'
        self.setStyleSheet(self.load_styles())

        # Správce grafů
        self.graph_manager = GraphManager()

        # Initializace UI
        self.initUI()
        self.reinitialize_components()
    
        # Start DTO thread
        self.can.start_rx_thread()

    # === inicializační funkce ===
    def initUI(self):
        """Inicializuje všechny komponenty UI."""
        self.create_layout()
        self.create_menu_bar()
        self.create_left_column()
        self.create_right_column()

        
        self.timer = QTimer()
        self.timer.start(self.update_interval_ms)
        self.timer2 = QTimer()
        self.timer2.start(self.spectrum_update_interval_ms)
        self.timer3 = QTimer()
        self.timer3.start(self.IQ_plot_update_interval_ms)

        
        # Spustí časovače pro aktualizaci UI
        self.timer.timeout.connect(self.update_ui)
        self.timer2.timeout.connect(self.update_ui_slow)
        self.timer3.timeout.connect(self.update_ui_fast)
        QTimer.singleShot(2000, self.one_shot_update)

    def save_app_config(self, dialog=0):
        """Uloží konfiguraci aplikace do souboru.
    
        Args:
            dialog (int): Pokud 1, zobrazí dialog pro výběr souboru.
            Pokud 0, uloží do výchozího souboru.
        """
        self.can.DTO_ID = self.channel_selector.value()
        config = {
            #Provozní soubory
            "DTO_ID": self.can.DTO_ID,
            "can_file_name": self.can_file_name,
            #Časové diagramy
            "history_seconds": self.history_seconds,
            "update_interval_ms": self.update_interval_ms,
            #Spektra
            "phase_integration_time": self.phase_integration_time,
            "DDS_integration_time": self.DDS_integration_time,
            "phase_window_type": self.phase_window_type,
            "DDS_window_type": self.DDS_window_type,
            "spectrum_update_interval_ms": self.spectrum_update_interval_ms,
            #IQ graf
            "IQ_plot_update_interval_ms": self.IQ_plot_update_interval_ms,
            "IQ_plot_history_samples": self.IQ_plot_history_samples,
            #Proměnné pro export dat
            "data_log_variables": self.data_log_variables,
            "data_log_interval_ms": self.data_log_interval_ms,
            "data_log_path": self.data_log_path,
            "data_log_separator": self.data_log_separator,
            "data_log_duration_s": self.data_log_duration_s,
            #Logování eventů
            "event_log_path": self.event_log_path

        }
    
        if dialog == 1:
            # Zobrazí dialog pro výběr souboru
            file_name, _ = QFileDialog.getSaveFileName(self, "Uložit konfiguraci", "", "JSON Files (*.json)")
            if not file_name:
                logging.info("Config save cancelled by user.")
                return
        else:
            # Použije výchozí soubor
            file_name = "app_config.json"
    
        # Uložení do souboru
        try:
            with open(file_name, "w") as file:
                json.dump(config, file, indent=4)
            logging.info(f"Configuration saved to {file_name}")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")

    def load_app_config(self, dialog=0):
        """Načte konfiguraci aplikace ze souboru.
    
        Args:
            dialog (int): Pokud 1, zobrazí dialog pro výběr souboru. Pokud 0, načte z výchozího souboru.
        """
        if dialog == 1:
            # Zobrazí dialog pro výběr souboru
            file_name, _ = QFileDialog.getOpenFileName(self, "Otevřít konfiguraci", "", "JSON Files (*.json)")
            if not file_name:
                logging.info("Config load cancelled by user.")
                return
        else:
            # Použije výchozí soubor
            file_name = "app_config.json"
    
        # Načtení ze souboru
        try:
            with open(file_name, "r") as file:
                config = json.load(file)
                self.setup_DTO_ID = config.get("DTO_ID", "47")
                self.can_file_name = config.get("can_file_name", "fnc.can")
                self.history_seconds = config.get("history_seconds", 10)
                self.update_interval_ms = config.get("update_interval_ms", 200)
                self.phase_integration_time = config.get("phase_integration_time", 10)
                self.DDS_integration_time = config.get("DDS_integration_time", 20)
                self.phase_window_type = config.get("phase_window_type", "Hanning")
                self.DDS_window_type = config.get("DDS_window_type", "Hanning")
                self.spectrum_update_interval_ms = config.get("spectrum_update_interval_ms", 1000)
                self.IQ_plot_update_interval_ms = config.get("IQ_plot_update_interval_ms", 60)
                self.IQ_plot_history_samples = config.get("IQ_plot_history_samples", 100)
                #Proměnné pro export dat
                self.data_log_variables = config.get("data_log_variables", ["phase_A_rad", "DDS_Hz"])
                self.data_log_interval_ms = config.get("data_log_interval_ms", 200)
                self.data_log_path = config.get("data_log_path", "data_log.csv")
                self.data_log_separator = config.get("data_log_separator", ";")
                self.data_log_duration_s = config.get("data_log_duration_s", 0)
                #logování eventů
                self.event_log_path = config.get("event_log_path", "trosca.log")
                
                logging.info(f"Configuration loaded from {file_name}")
    
            # Re-inicializace timerů atd
            
        except FileNotFoundError:
            logging.warning(f"Soubor {file_name} nebyl nalezen. Používají se výchozí hodnoty.")
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")

        try:
            self.reinitialize_components()
        except:
            return
        
    def reinitialize_components(self):
        """Znovu inicializuje komponenty po načtení konfigurace."""
        # Aktualizace časovačů
        self.timer.setInterval(self.update_interval_ms)
        self.timer2.setInterval(self.spectrum_update_interval_ms)
        self.timer3.setInterval(self.IQ_plot_update_interval_ms)
        self.channel_selector.setValue(self.setup_DTO_ID)    
        # Aktualizace délky bufferů
        self.can.set_IQ_buffer_length(self.IQ_plot_history_samples)
    
        # Aktualizace nastavení grafů
        self.n_samples = int(self.history_seconds * 1000 / self.update_interval_ms)
        for graph_key in self.graph_manager.graphs.keys():
            self.graph_manager.update_graph_settings(
                graph_key,
                history_length=self.n_samples,
                update_interval_ms=self.update_interval_ms
            )
    
        logging.info("Components reinitialized after loading configuration.")

    def setup_logging(self):
        """Nastaví logování"""
        logging.getLogger().handlers.clear()
        file_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%d.%m %H:%M") # V souboru s časem
        console_format = logging.Formatter("[%(levelname)s] %(message)s") # V konzoli bez času

        file_handler = logging.FileHandler(self.event_log_path, encoding="utf-8")
        file_handler.setFormatter(file_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_format)

        logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
    
    def log_plain(self, msg):
        """Pomocná funkce pro psaní a logování zpráv bez tagů jako INFO atd"""
        print(msg)
        with open(self.event_log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        
    
    # === funkce pro otevření dialogů ===
    def open_export_spectra(self):
        """Otevře dialog pro export spekter."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Uložit spektra", "", "text files (*.txt)")
        if not file_name:
            logging.info("Spectra save cancelled by user.")
            return
        self.export_spectra(file_name)

    def open_about_dialog(self):
        """Otevře okno O aplikaci."""
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def open_oscillator_settings(self):
        """Otevře okno Nastavení oscilátoru."""
        if self.oscillator_settings_window is None:
            self.oscillator_settings_window = OscillatorSettingsWindow(self, CANOpenID=self.can.DTO_ID)
        self.oscillator_settings_window.refresh_on_show()
        self.oscillator_settings_window.show()
        self.oscillator_settings_window.raise_()  # Přesune okno na vrchol
        
    def open_export_settings(self):
        """Otevře dialog pro nastavení exportu dat."""
        dialog = ExportSettingsDialog(self)
        if dialog.exec_():
            (self.data_log_variables,
            self.data_log_interval_ms,
            self.data_log_path,
            self.data_log_separator,
            self.data_log_duration_s) = dialog.get_values()
    
    def open_CANTableDialog(self):
        """Otevře dialog s tabulkou SDO parametrů."""
        if self.DTO_param_table_window is None:
            self.DTO_param_table_window = CANTableDialog("docs/DTO_params.csv")
        self.DTO_param_table_window.show()
        self.DTO_param_table_window.raise_()

    def open_help(self):
        """Otevře nápovědu v prohlížeči."""
        import webbrowser
        help_file = "docs/help.html"
        try:
            webbrowser.open(help_file)
            print(f"[INFO] Opened help: {help_file}")
        except Exception as e:
            logging.error(f"Can't open help: {e}")


    # === funkce pro vytvoření UI komponent ===
    def create_layout(self):
        """Vytvoří hlavní layout aplikace."""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Hlavní layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # QSplitter pro levý a pravý sloupec
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setHandleWidth(5)  # Nastavení šířky oddělovače

        # Levý sloupec
        self.left_column_widget = QWidget(self)
        self.left_column_widget.setMaximumWidth(350) 
        self.left_column = QVBoxLayout(self.left_column_widget)
        self.splitter.addWidget(self.left_column_widget)

        # Pravý sloupec
        self.right_column_widget = QWidget(self)
        self.right_column = QVBoxLayout(self.right_column_widget)
        self.splitter.addWidget(self.right_column_widget)

        # Nastavení výchozí velikosti sloupců
        self.splitter.setSizes([300, 500])  # Šířka levého a pravého sloupce

        # Přidání splitteru do hlavního layoutu
        self.main_layout.addWidget(self.splitter)

    def create_left_column(self):
        """Vytvoří levý sloupec s ovládacími prvky."""
        # Logo UPT
        self.image_label = QLabel(self)
        pixmap = QPixmap("images/UPT_text_en_white_15.png")
        pixmap = pixmap.scaledToHeight(80)  # případně změň velikost
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignHCenter)
        self.image_label.setMaximumHeight(80)
        self.left_column.addWidget(self.image_label)

        # DTO_ID input spinbox
        self.channel_selector = QSpinBox()
        self.channel_selector.setMaximumWidth(100)
        self.channel_selector.setMinimumWidth(70)
        self.channel_selector.setRange(0, 127)
        self.channel_selector.setValue(self.can.DTO_ID)
        self.channel_selector.valueChanged.connect(self.restart_rx_thread)

        # RX thread on-off toggle
        # https://www.pythonguis.com/widgets/pyqt-toggle-widget/
        self.CANToggle = Toggle(checked_color=self.accent_color) 
        self.CANToggle.setFixedSize(45, 30)
        self.CANToggle.setChecked(True)
        self.CANToggle.stateChanged.connect(
            lambda state: (
                setattr(self.can, "toggle", bool(state)),
                self.can.start_rx_thread() if self.can.toggle else self.can.stop_rx_thread()
            )
        )

        left_form_layout = QFormLayout()
        self.left_column.addLayout(left_form_layout)

        left_form_layout.addRow("CAN ID karty:", self.channel_selector)
        left_form_layout.setAlignment(self.channel_selector, Qt.AlignRight)

        left_form_layout.addRow("Povolit CAN komunikaci:", self.CANToggle)
        left_form_layout.setAlignment(self.CANToggle, Qt.AlignRight)

        # Přepínač enable can tx
        self.enable_can_tx_toggle = QCheckBox()
        self.enable_can_tx_toggle.clicked.connect(self.toggle_can_tx)
        left_form_layout.addRow("Povolit CAN TX:", self.enable_can_tx_toggle)
        left_form_layout.setAlignment(self.enable_can_tx_toggle, Qt.AlignRight)

        #přepínač zápisu dat
        self.data_logging_toggle = QCheckBox("Ukládat data do souboru")
        self.data_logging_toggle.setChecked(False)
        self.data_logging_toggle.clicked.connect(self.toggle_data_logging)
        self.left_column.addWidget(self.data_logging_toggle)

        #label zbývajícího času zápisu dat
        self.data_log_time_label = QLabel("Zbývající čas záznamu: -")
        self.left_column.addWidget(self.data_log_time_label)
        
        #Skupina sliderů
        slider_group = QGroupBox("Upravit")
        slider_form_layout = QFormLayout()
        slider_group.setLayout(slider_form_layout)
        self.left_column.addWidget(slider_group)

        # Přepínač PID Lock
        self.pid_lock_toggle = Toggle(checked_color=self.accent_color)
        self.pid_lock_toggle.setFixedSize(45, 30)
        self.pid_lock_toggle.stateChanged.connect(self.toggle_pid_lock)
        slider_form_layout.addRow("PID Lock:", self.pid_lock_toggle)
        slider_form_layout.setAlignment(self.pid_lock_toggle, Qt.AlignRight)

        # Slidery a spinboxy
        self.Slider1 = SlidBox(-2048, 2047, self.can.DA1_out.contents.value, self.download_slider_values)
        slider_form_layout.addRow("DA1 (-)", self.Slider1)
        self.Slider2 = SlidBox(-2048, 2047, self.can.DA2_out.contents.value, self.download_slider_values)
        slider_form_layout.addRow("DA2 (-)", self.Slider2) 
        self.Slider3 = SlidBox(0, 200000000, self.can.dFTW_out.contents.value, self.download_slider_values)
        slider_form_layout.addRow("f_NCO (Hz)", self.Slider3)
      
        # Tlačítko Phase Detector Reset
        self.phase_reset_button = QPushButton("Reset fázového detektoru", self)
        self.phase_reset_button.setMaximumWidth(200)
        self.phase_reset_button.clicked.connect(self.phase_detector_reset)
        slider_form_layout.addWidget(self.phase_reset_button)
        slider_form_layout.setAlignment(self.phase_reset_button, Qt.AlignRight)
        
        #refresh hodnot (upload ze zařízení)
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.setMaximumWidth(200)
        self.refresh_button.clicked.connect(self.one_shot_update)
        self.left_column.addWidget(self.refresh_button, alignment=Qt.AlignRight)

        # SDO send input fields
        SDO_group = QGroupBox("SDO")
        SDO_group_layout = QFormLayout()
        SDO_group.setLayout(SDO_group_layout)
        self.left_column.addWidget(SDO_group)

        self.sdo_index_field = QLineEdit(self)
        self.sdo_index_field.setPlaceholderText("SDO index [hex]")
        SDO_group_layout.addRow("SDO index:", self.sdo_index_field)
        
        self.sdo_subindex_field = QLineEdit(self)
        self.sdo_subindex_field.setPlaceholderText("SDO subindex [hex]")
        SDO_group_layout.addRow("SDO subindex:", self.sdo_subindex_field)

        self.sdo_data_field = QLineEdit(self)
        self.sdo_data_field.setPlaceholderText("Vložit SDO data")
        SDO_group_layout.addRow("SDO data:", self.sdo_data_field)

        # SDO tlačítka
        self.upload_btn = QPushButton('Upload', self)
        self.upload_btn.clicked.connect(self.manual_SDO_upload)
        SDO_group_layout.addWidget(self.upload_btn)

        self.download_btn = QPushButton('Download', self)
        self.download_btn.clicked.connect(self.manual_SDO_download)
        SDO_group_layout.addWidget(self.download_btn)        

        # tlačítko pro otevření nastavení  aplikace
        self.settings_button = QPushButton("Nastavení")
        self.settings_button.clicked.connect(self.open_settings)
        self.left_column.addWidget(self.settings_button)
    
    def create_right_column(self):
        """Vytvoří pravý sloupec s grafy a dalšími widgety."""
        # --- Horní skupina ---
        self.top_group = QGroupBox("Hodnoty v čase")
        self.top_group_layout = QGridLayout()
        self.top_group.setLayout(self.top_group_layout)
        self.right_column.addWidget(self.top_group)

        # Přidání IQ widgetu
        self.iq_widget = IQWidget(x=200, y=200, parent=self, title="IQ Graf")
        self.top_group_layout.addWidget(self.iq_widget, 0, 0)

        # Intenzity
        self.intensity_plot = self.graph_manager.add_graph(
            names=["CH1_mag", "CH2_mag"],
            title="Intenzity kanálů",
            xlabel="Čas (s)",
            ylabel="Intenzita",
            units="-",
            history_length=self.n_samples,
            update_interval_ms=self.update_interval_ms,
            parent=self,
            with_legend=True
        )
        self.top_group_layout.addWidget(self.intensity_plot, 0, 1)

        # Phase Plot
        self.phase_plot = self.graph_manager.add_graph(
            names="phase_dev",
            title="Fázové odchylky",
            xlabel="Čas (s)",
            ylabel="Fáze",
            units="rad",
            history_length=self.n_samples,
            update_interval_ms=self.update_interval_ms,
            parent=self
        )
        self.top_group_layout.addWidget(self.phase_plot, 0, 2)

        # Frequency Plot
        self.frequency_plot = self.graph_manager.add_graph(
            names="frequency_dev",
            title="Frekvenční odchylky",
            xlabel="Čas (s)",
            ylabel="Frekvence",
            units="Hz",
            history_length=self.n_samples,
            update_interval_ms=self.update_interval_ms,
            parent=self
        )
        self.top_group_layout.addWidget(self.frequency_plot, 1, 1)

        # DDS Frequency Plot
        self.dds_frequency_plot = self.graph_manager.add_graph(
            names="frequency_DDS",
            title="Frekvence DDS",
            xlabel="Čas (s)",
            ylabel="Frekvence",
            units="Hz",
            history_length=self.n_samples,
            update_interval_ms=self.update_interval_ms,
            parent=self
        )
        self.top_group_layout.addWidget(self.dds_frequency_plot, 1, 2)

        #  --- Spodní skupina ---
        self.bottom_group = QGroupBox("Spektra")
        self.bottom_group_layout = QHBoxLayout()
        self.bottom_group.setLayout(self.bottom_group_layout)
        self.right_column.addWidget(self.bottom_group)

        # PSD fázového šumu
        self.spectrum1_plot = SpectrumPlot(
            title="PSD fázového šumu",
            xlabel="Fourierova frekvence (Hz)",
            ylabel="PSD",
            yunit="(dBc/Hz)",
            parent=self
        )
        self.bottom_group_layout.addWidget(self.spectrum1_plot.plot_widget)

        # PSD akčního zásahu DDS
        self.spectrum2_plot = SpectrumPlot(
            title="PSD akčního zásahu DDS",
            xlabel="Fourierova frekvence (Hz)",
            ylabel="PSD",
            yunit="(dBc/Hz)",
            parent=self
        )
        self.bottom_group_layout.addWidget(self.spectrum2_plot.plot_widget)

    def create_menu_bar(self):
        """Vytvoří horní nabídku."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Soubor")
        edit_menu = menu_bar.addMenu("Upravit")
        view_menu = menu_bar.addMenu("Zobrazit")
        help_menu = menu_bar.addMenu("Nápověda")

        # --- Soubor ---
        # Akce pro otevření konfigurace do Soubor
        open_action = QAction("Otevřít konfiguraci", self)
        open_action.triggered.connect(lambda: self.load_app_config(dialog=1))
        file_menu.addAction(open_action)

        # Akce pro uložení konfigurace do Soubor
        save_action = QAction("Uložit konfiguraci", self)
        save_action.triggered.connect(lambda: self.save_app_config(dialog=1))
        file_menu.addAction(save_action)

        #Akce pro export spekter do Soubor
        export_spectra_action = QAction("Exportovat spektra", self)
        export_spectra_action.triggered.connect(self.open_export_spectra)
        file_menu.addAction(export_spectra_action)

        # Akce ukončit do Soubor
        file_menu.addSeparator()
        exit_action = QAction("Ukončit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # --- Upravit ---
        # Nastavení do Upravit
        settings_action = QAction("Nastavení aplikace", self)
        settings_action.triggered.connect(self.open_settings) 
        edit_menu.addAction(settings_action)

        # Nastavení karty do Upravit
        oscillator_settings_action = QAction("Nastavení karty", self)
        oscillator_settings_action.triggered.connect(self.open_oscillator_settings)
        edit_menu.addAction(oscillator_settings_action)

        # Nastavení exportu dat do Upravit
        export_settings_action = QAction("Nastavení exportu dat", self)
        export_settings_action.triggered.connect(self.open_export_settings)
        edit_menu.addAction(export_settings_action)

        # --- Zobrazit ---
        # Tabulka CAN parametrů do Zobrazit
        CANTableDialog_action = QAction("Tabulka SDO parametrů", self)
        CANTableDialog_action.triggered.connect(self.open_CANTableDialog)
        view_menu.addAction(CANTableDialog_action)

        # --- Nápověda ---
        # O aplikaci do Nápověda
        about_action = QAction("O aplikaci", self)
        about_action.triggered.connect(self.open_about_dialog)
        help_menu.addAction(about_action)

        # Nápověda do Nápověda
        help_action = QAction("Nápověda", self)
        help_action.triggered.connect(self.open_help) 
        help_menu.addAction(help_action)
    

    # === Funkce GUI pro ovládání CANu ===
    def gray_out_(self):
        """deaktivuje všechny ovládací prvky v levém sloupci"""
        rx_on = self.can.DTO_thread.is_alive()
        tx_on = self.can.enable_can_tx
        pid_on = self.pid_lock_toggle.isChecked()

        self.Slider1.setEnabled(rx_on and tx_on and not pid_on)
        self.Slider2.setEnabled(rx_on and tx_on and not pid_on)
        self.Slider3.setEnabled(rx_on and tx_on and not pid_on)
        self.download_btn.setEnabled(rx_on and tx_on)
        self.upload_btn.setEnabled(rx_on)
        self.phase_reset_button.setEnabled(rx_on and tx_on)
        self.pid_lock_toggle.setEnabled(rx_on and tx_on)

        if not rx_on:
            self.can.enable_can_tx = False
            self.enable_can_tx_toggle.setChecked(False)
            self.enable_can_tx_toggle.setEnabled(False)
        else:
            self.enable_can_tx_toggle.setEnabled(True)

    def restart_rx_thread(self):
        """Restartuje RX thread"""
        self.can.DTO_ID = self.channel_selector.value()
        self.can.stop_rx_thread()
        self.can.start_rx_thread()  
        logging.info(f"DTO ID changed: {self.can.DTO_ID}")

    def read_sdo_value(self, index, subindex):
        """Načte hodnotu z SDO na zadaném indexu a subindexu."""
        try:
            self.can.can_rx_SDO(CANOpenID=self.can.DTO_ID, index=index, subindex=subindex)
            time.sleep(0.1)  # Čekání na přijetí dat
            value = self.can.sdo_data.contents.value
            #print(f"[INFO] SDO value loaded: (index=0x{index:X}, subindex=0x{subindex:X}): {value}")
            return value
        except Exception as e:
            logging.error(f"Error loading SDO value (index=0x{index:X}, subindex=0x{subindex:X}): {e}")
            return None  # Výchozí hodnota při chybě
        
    def one_shot_update(self):
        """Provede jednorázovou aktualizaci vybraných hodnot z DTO."""
        if not self.can.is_device_connected():
            QMessageBox.critical(self, "Chyba CAN", "Nelze načíst data \nZařízení není připojeno nebo neodpovídá.\nZkontrolujte připojení a zkuste znovu.")
            # Nabídka další pokus
            logging.error("One shot update failed")
            retry = QMessageBox.question(self, "Zkusit znovu?", "Chcete provést další pokus o připojení? \nPozději můžete použít tlačítko Refresh.", QMessageBox.Yes | QMessageBox.No)
            if retry == QMessageBox.Yes:
                self.one_shot_update()
            return
        self.channel_selector.setValue(self.can.DTO_ID)

        self.PDO1_Tsamp = self.read_sdo_value(index=0x2009, subindex=1)
        self.PDO2_Tsamp = self.read_sdo_value(index=0x2009, subindex=2)
        self.PDO3_Tsamp = self.read_sdo_value(index=0x2009, subindex=3)
        self.PDO4_Tsamp = self.read_sdo_value(index=0x2009, subindex=4)

        self.DDS_ref_freq = self.read_sdo_value(index=0x200c, subindex=0x15)
        self.DDS_ref_freq_multiplier = np.int16(self.read_sdo_value(index=0x200c, subindex=0x16) & 0xFFFF) #převod na int16
        self.fclk = np.int32(np.int32(self.DDS_ref_freq) * np.int32(self.DDS_ref_freq_multiplier))
        self.DDS_frequency_step = self.fclk/2**32
        
        # Načtení hodnoty PID Lock
        pid_lock_value = self.read_sdo_value(index=0x2007, subindex=0)
        pid_lock_state = pid_lock_value == 0x111  # Pokud je hodnota 0x111, přepínač je zapnutý
        name = self.int_to_str(self.read_sdo_value(index=0x1008, subindex=0))
        version = self.int_to_str(self.read_sdo_value(index=0x1009, subindex=0))
        logging.info(f"One shot update performed:")
        self.log_plain(f"       Name: {name}")
        self.log_plain(f"       Version: {version}")
        self.log_plain(f"       PID Lock value: {hex(pid_lock_value)}")
        self.log_plain(f"       CAN timing: PDO1: {self.PDO1_Tsamp} ms, PDO2: {self.PDO2_Tsamp} ms, PDO3: {self.PDO3_Tsamp} ms, PDO4: {self.PDO4_Tsamp} ms")
        self.log_plain(f"       DDS reference frequency: {self.fclk/10**6} MHz")
        self.log_plain(f"       DDS frequency step: {self.DDS_frequency_step}")

        # Aktualizace přepínače PID Lock
        self.pid_lock_toggle.setChecked(pid_lock_state)  # Nastaví přepínač podle hodnoty
        #self.pid_lock_toggle.blockSignals(True)  # Zabrání vyvolání signálu při změně stavu
    
    def int_to_str(self, value):
        """Převede int na string"""
        try:
            if value == 0:
                return ""
            return value.to_bytes(4, 'little').decode('ascii', errors='ignore').rstrip('\x00')
        except Exception:
            return str(value)

    def toggle_pid_lock(self, state):
        """
        Odešle hodnotu na SDO index 0x2007 podle stavu přepínače.
        Slouží k současnému povolení/zakázání všech 3 PID regulátorů
        """
        try:
            value = 0x111 if state else 0x0
            self.can.can_tx_SDO(CANOpenID=self.can.DTO_ID, index=0x2007, subindex=0, data=value)
            logging.info(f"PID Lock {'enabled' if state else 'disabled'} (value: {hex(value)})")
        except Exception as e:
            self.log_plain(f" [ERROR]: Error sending PID LOCK: {e}")

    def toggle_can_tx(self, state):
        """Přepínač pro povolení/zakázání CAN TX s potvrzením."""
        if state:
            reply = QMessageBox.question(
                self,
                "Potvrzení",
                "Opravdu chcete POVOLIT CAN TX?\nTato akce umožní zápis do zařízení.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.can.enable_can_tx = True
                logging.info(f"CAN TX enabled")
            else:
                self.enable_can_tx_toggle.blockSignals(True)
                self.enable_can_tx_toggle.setChecked(False)
                #self.can.enable_can_tx = False
                self.enable_can_tx_toggle.blockSignals(False)
                logging.info(f"CAN TX enable cancelled by user")
                return
        else:
                self.can.enable_can_tx = False
                logging.info(f"CAN TX disabled")

    def phase_detector_reset(self):
        """Odešle hodnotu 1 na SDO index 0x2006 pro reset phase detectoru."""
        try:
            self.can.can_tx_SDO(CANOpenID=self.can.DTO_ID, index=0x2006, subindex=0, data=1)
            logging.info("Phase Detector reset")
        except Exception as e:
            logging.error(f"Couldn't reset phase detector: {e}")

    def manual_SDO_upload(self):
        """Přijme SDO data z DTO zařízení."""
        self.can.sdo_data.contents.value = 0
        self.sdo_data_field.setText("")
        sdo_index = self.sdo_index_field.text()
        sdo_subindex = self.sdo_subindex_field.text()

        try:
                sdo_index = int(sdo_index, 16)
                sdo_subindex = int(sdo_subindex, 16)
                self.can.can_rx_SDO(CANOpenID=self.can.DTO_ID, index=sdo_index, subindex=sdo_subindex)  # Odeslání SDO dat
        except ValueError:
                logging.error(" Invalid SDO data. Please enter a valid integer.")
        time.sleep(0.2)
        self.sdo_data_field.setText(str(self.can.sdo_data.contents.value))  # Předpokládám, že sdo_data je správně nastaven
   
    def manual_SDO_download(self):
        """Odešle SDO data do DTO zařízení."""
        # Odeslání obsahu SDO send pole
        sdo_index = self.sdo_index_field.text()
        sdo_subindex = self.sdo_subindex_field.text()
        sdo_data = self.sdo_data_field.text()
        if sdo_data:
            try:
                sdo_value = int(sdo_data)  # Převede vstup na celé číslo
                sdo_index = int(sdo_index)
                sdo_subindex = int(sdo_subindex)
                self.can.can_tx_SDO(CANOpenID=self.can.DTO_ID, index=sdo_index, subindex=sdo_subindex, data=sdo_value)  # Odeslání SDO dat
                logging.info(f"SDO data sent: {sdo_value}")
            except ValueError:
                logging.error(" Invalid SDO data. Please enter a valid integer.")
    
    def download_slider_values(self):
        """Odešle hodnoty DA1_value, DA2_value a f_NCO_Hz pomocí can_tx_PDO1."""
        # Získání hodnot ze všech sliderů
        #print(f"[INFO] Slider {name} changed to {value}")
        da1_value = self.Slider1.value()
        da2_value = self.Slider2.value()
        f_nco_hz =  self.Slider3.value()
        # Odeslání hodnot pomocí CAN
        self.can.can_tx_PDO1(
            CANOpenID=self.can.DTO_ID,
            data1=da1_value,
            data2=da2_value,
            data3=f_nco_hz
        )
        #print(f"\r[INFO] added to tx queue: DA1={da1_value}, DA2={da2_value}, f_NCO_Hz={f_nco_hz}",  end='')

    def upload_slider_values(self):
        """Načte hodnoty DA1_out, DA2_out a dFTW_out z DTO zařízení a nastaví je do sliderů."""
        # Načtení hodnot pro slidery
        da1_value = self.can.DA1_out.contents.value
        da2_value = self.can.DA2_out.contents.value 

        # Nastavení hodnot do sliderů
        self.Slider1.set_value(da1_value)
        self.Slider2.set_value(da2_value)
 

    # === funkce pro zápis dat do souboru ===
    def toggle_data_logging(self, state):
        """Přepínač pro povolení/zakázání záznamu dat do souboru."""
        self.data_logging_enabled = bool(state)
        if self.data_logging_enabled:
            self.start_data_logging()
        else:
            self.stop_data_logging()

    def start_data_logging(self):
        """Spustí záznam dat do souboru."""
        if os.path.exists(self.data_log_path):
            # Načti první řádek (hlavičku) existujícího souboru
            with open(self.data_log_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=self.data_log_separator)
                try:
                    header = next(reader)
                except Exception:
                    header = []

            expected_header = ["timestamp"] + self.data_log_variables
            
            # Nabídni možnosti
            msg = QMessageBox(self)
            msg.setWindowTitle("Soubor existuje")
            msg.setText(f"Soubor {self.data_log_path} již existuje. Co teď?")
            append_btn = msg.addButton("Pokračovat ve stávajícím", QMessageBox.AcceptRole)
            overwrite_btn = msg.addButton("Přepsat soubor", QMessageBox.DestructiveRole)
            overwrite_btn.setStyleSheet(f"""
                    QPushButton {{border: 2px solid red;  color: white; }}
                    QPushButton:hover {{background-color: red; color: black;}}""")
            newfile_btn = msg.addButton("Vybrat nový soubor", QMessageBox.ActionRole)
            cancel_btn = msg.addButton("Zrušit", QMessageBox.RejectRole)
            cancel_btn.setStyleSheet(f"""
                QPushButton {{border: 2px solid {self.accent_color};  color: white; }}
                QPushButton:hover {{background-color: {self.accent_color}; color: black;}}""")
            msg.setDefaultButton(cancel_btn)
            
            if header != expected_header:
                append_btn.setEnabled(False)
            
            msg.exec_()
            self.data_logging_toggle.setChecked(True)

            clicked = msg.clickedButton()
            if clicked == cancel_btn:
                self.data_logging_toggle.setChecked(False)
                return
            elif clicked == overwrite_btn:
                mode = "w"
            elif clicked == newfile_btn:
                file_name, _ = QFileDialog.getSaveFileName(self, "Vyberte nový soubor", self.data_log_path, "CSV Files (*.csv);;All Files (*)")
                if not file_name:
                    self.data_logging_toggle.setChecked(False)
                    return
                self.data_log_path = file_name
                mode = "w"
            elif clicked == append_btn:
                    mode = "a"
            else:
                self.data_logging_toggle.setChecked(False)
                return
        else:
            mode = "w"

        # Otevři soubor a zapisuj
        try:
            self.data_log_file = open(self.data_log_path, mode, encoding="utf-8", newline="")
        except Exception as e:
                logging.error(f"Failed to open file: {e}")
                QMessageBox.critical(self, "Chyba", f"Nepodařilo se otevřít soubor: \n {e} \n Možná jej používá jiný proces?")
                self.data_logging_toggle.setChecked(False)
                return


        if mode == "w": #vytvoří hlavičku
            self.data_log_file.write(self.data_log_separator.join(["timestamp"] + self.data_log_variables) + "\n")
            logging.info(f"New data log file created: {self.data_log_path}")
        logging.info(f"Data logging started. Interval: {self.data_log_interval_ms} ms, Duration: {self.convert_S_to_HHMMSS(self.data_log_duration_s)}")
        #Pokud je interval zápisu větší než 0, řídí se zápis časovačem, jinak se řídí kartou CAN
        if self.data_log_interval_ms > 0:
            self.quick_data_logging = False
            self.data_log_timer = QTimer()
            self.data_log_timer.timeout.connect(self.write_data_log_row)
            self.data_log_timer.start(self.data_log_interval_ms)
        else:
            self.quick_data_logging = True
        
        self.data_log_start_time = time.time()
        self.data_log_remaining_s = self.data_log_duration_s
        self.data_log_time_label.setText(f"Zbývající čas záznamu: {self.convert_S_to_HHMMSS(self.data_log_remaining_s)}")
        if self.data_log_duration_s > 0:
            self.data_log_countdown_timer = QTimer()
            self.data_log_countdown_timer.timeout.connect(self.update_data_log_countdown)
            self.data_log_countdown_timer.start(1000)
    
    def update_data_log_countdown(self):
        """Aktualizuje zbývající čas záznamu."""
        if self.data_logging_enabled:
            elapsed = int(time.time() - self.data_log_start_time)
            self.data_log_remaining_s = max(0, self.data_log_duration_s - elapsed)
            # Aktualizuj label v levém sloupci
            self.data_log_time_label.setText(f"Zbývající čas záznamu: {self.convert_S_to_HHMMSS(self.data_log_remaining_s)}")
            #self.data_log_time_label.setText(f"Zbývající čas záznamu: {self.data_log_remaining_s}")
            if self.data_log_remaining_s <= 0:
                self.stop_data_logging()
                self.data_logging_toggle.setChecked(False)
                self.data_logging_enabled = False

    def convert_S_to_HHMMSS(self, secs):
        """Převede int na string ve formátu HH:MM:SS."""
        hours = secs//(60**2)
        minutes = (secs-hours*60**2)//60
        seconds = (secs-hours*60**2-minutes*60)
        return(f"{hours:02} : {minutes:02} : {seconds:02}")

    def stop_data_logging(self):
        """Zastaví záznam dat do souboru."""
        if hasattr(self, "data_log_timer"):
            self.data_log_timer.stop()
        if hasattr(self, "data_log_countdown_timer"):
            self.data_log_countdown_timer.stop()
        if hasattr(self, "data_log_file"):
            self.data_log_file.close()
        logging.info(f"Data logging stopped.")

    def write_data_log_row(self):
        """Zapíše řádek s daty do data log souboru."""
        if self.can.device_connected:
            values = []
            timestamp = datetime.datetime.now().isoformat(sep = " ", timespec='milliseconds') #časová značka
            values.append(timestamp)
            for var in self.data_log_variables:
                value = getattr(self.can, var, "")
                # Pokud je to pointer, vezmi .contents.value
                if hasattr(value, "contents"):
                    value = value.contents.value
                values.append(str(value))
            self.data_log_file.write(self.data_log_separator.join(values) + "\n")
            self.data_log_file.flush()

    def export_spectra(self, file_path="spectra_export.txt"):
        """
        Uloží aktuální spektra do texťáku, hodnoty budou ve sloupcích:
        1. sloupec: Amplituda šumu (dBc)
        2. sloupec: PSD šumu (dBc/Hz)
        3. sloupec: frekvenční osa šumu (Hz)
        4. sloupec: Amplituda akčního zásahu (dBc)
        5. sloupec: PSD akčního zásahu (dBc/Hz)
        6. sloupec: frekvenční osa akčního zásahu (Hz)
        """
        # Výpočet spekter
        phase_data = self.can.calculate_spectral_data(
            self.can.phase_A_rad_buffer,
            self.can.phase_A_rad_buffer_length,
            self.can.set_phase_A_rad_buffer_length,
            self.phase_integration_time,
            self.PDO1_Tsamp,
            self.phase_window_type
        )
        dds_data = self.can.calculate_spectral_data(
            np.array(self.can.dFTW_out_buffer) * self.DDS_frequency_step,
            self.can.dFTW_out_buffer_length,
            self.can.set_dFTW_out_buffer_length,
            self.DDS_integration_time,
            self.PDO2_Tsamp,
            self.DDS_window_type
        )

        if phase_data is None or dds_data is None:
            QMessageBox.warning(self, "Chyba exportu", "Nelze exportovat spektra – nejsou k dispozici data.")
            return

        freq_phase, mag_phase, psd_phase = phase_data
        freq_dds, mag_dds, psd_dds = dds_data

        # Musim seřadit data do sloupcu => najdu max. delku
        max_len = max(len(mag_phase), len(psd_phase), len(freq_phase), len(mag_dds), len(psd_dds), len(freq_dds))

        # Připrav data do sloupců
        columns = [
            mag_phase, psd_phase, freq_phase,
            mag_dds, psd_dds, freq_dds
        ]
           # Kratší sloupce jsou doplněny mezerami, aby to vyšlo všude stejně
        columns = [list(col) + [""] * (max_len - len(col)) for col in columns]

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Hlavička
                f.write("mag_phase;psd_phase;freq_phase;mag_dds;psd_dds;freq_dds\n")
                # Po řádcích se zapisují hodnoty ze sloupců
                for i in range(max_len):
                    row = []
                    for col in columns:
                        val = col[i]
                        if isinstance(val, float):
                            row.append(f"{val:.2f}")
                        else:
                            row.append(str(val))
                    f.write(";".join(row) + "\n")
            QMessageBox.information(self, "Export spekter", f"Spektra byla uložena do:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Chyba exportu", f"Chyba při ukládání spekter:\n{e}")
   

    # === funkce pro otevření nastavení ===
    def open_settings(self):
        """Otevře dialog pro nastavení grafů a aplikuje změny po zavření dialogu."""
        old_update_interval_ms = self.update_interval_ms
        old_phase_integration_time = self.phase_integration_time
        old_DDS_integration_time = self.DDS_integration_time
        old_spectrum_update_interval_ms = self.spectrum_update_interval_ms

        dialog = SettingsDialog(self)
        if dialog.exec_():
            # Získání nových hodnot
            (
                self.history_seconds,
                self.update_interval_ms,
                self.IQ_plot_update_interval_ms,
                self.IQ_plot_history_samples,

                self.spectrum_update_interval_ms,
                self.phase_integration_time,
                self.DDS_integration_time,
                self.phase_window_type,
                self.DDS_window_type,

                self.can_file_name,
                self.data_log_path,
                self.event_log_path
            ) = dialog.get_values()

            logging.info(f"New settings values:\n")
            self.print_settings_values()
            self.n_samples = int(self.history_seconds * 1000 / self.update_interval_ms)

            # Pokud se změnila perioda obnovení
            if self.update_interval_ms != old_update_interval_ms:
                self.timer.setInterval(self.update_interval_ms)
                self.clear_all_plots()

            # Pokud se změnila perioda obnovení spekter
            if self.spectrum_update_interval_ms != old_spectrum_update_interval_ms:
                self.timer2.setInterval(self.spectrum_update_interval_ms)

            # Aktualizace nastavení pro IQWidget
            self.timer3.setInterval(self.IQ_plot_update_interval_ms)
            # Aktualizace délky bufferů
            self.can.set_IQ_buffer_length(self.IQ_plot_history_samples)
            

            # Aktualizace nastavení pro všechny grafy
            for graph_key in self.graph_manager.graphs.keys():
                self.graph_manager.update_graph_settings(
                    graph_key,
                    history_length=self.n_samples,
                    update_interval_ms=self.update_interval_ms
                )
   
    def print_settings_values(self):
        """ Vytiskne aktuální hodnoty nastavení do logu a konzole."""
        indent = " " * 4
        self.log_plain(f"{indent}{'Name':<30} {'Value':<20}")
        self.log_plain(f"{indent}{'-' * 50}")
        self.log_plain(f"{indent}{'history (s)':<30} {self.history_seconds:<20}")
        self.log_plain(f"{indent}{'update_interval (ms)':<30} {self.update_interval_ms:<20}")
        self.log_plain(f"{indent}{'IQ_plot_update_interval (ms)':<30} {self.IQ_plot_update_interval_ms:<20}")
        self.log_plain(f"{indent}{'IQ_plot_history_samples':<30} {self.IQ_plot_history_samples:<20}")
        print()
        self.log_plain(f"{indent}{'spectrum_update_interval (ms)':<30} {self.spectrum_update_interval_ms:<20}")
        self.log_plain(f"{indent}{'phase_integration_time (s)':<30} {self.phase_integration_time:<20}")
        self.log_plain(f"{indent}{'DDS_integration_time (s)':<30} {self.DDS_integration_time:<20}")
        self.log_plain(f"{indent}{'phase_window_type':<30} {self.phase_window_type:<20}")
        self.log_plain(f"{indent}{'DDS_window_type':<30} {self.DDS_window_type:<20}")


    # === funkce pro aktualizaci GUI ===
    def update_ui(self):
        """Aktualizuje labely, grafy atd"""
        if self.can.DTO_thread and self.can.DTO_thread.is_alive() and self.can.device_connected:
            self.update_plots()
                 
    def update_ui_slow(self):
        """Aktualizuje spektra a slidery"""
        if self.can.DTO_thread and self.can.DTO_thread.is_alive() and self.can.device_connected:
            self.upload_slider_values()  # Aktualizace hodnot sliderů
            self.gray_out_()  # Změna barvy textu na šedou podle stavu přepínače
            try: 
                Phase_spectral_data = self.can.calculate_spectral_data(self.can.phase_A_rad_buffer, self.can.phase_A_rad_buffer_length, self.can.set_phase_A_rad_buffer_length, self.phase_integration_time, self.PDO1_Tsamp, self.phase_window_type)
                if Phase_spectral_data is not None:
                    freq, magnitude_dB, psd_dB = Phase_spectral_data
                    self.spectrum1_plot.update(freq, psd_dB)  # Aktualizace spektra fázového šumu
            except Exception as e:
                logging.error(f"Can't calculate spectral data: {e}")

            try:
                DDS_spectral_data = self.can.calculate_spectral_data(np.array(self.can.dFTW_out_buffer) * self.DDS_frequency_step, self.can.dFTW_out_buffer_length, self.can.set_dFTW_out_buffer_length, self.DDS_integration_time, self.PDO2_Tsamp, self.DDS_window_type)
                if DDS_spectral_data is not None:
                    freq, magnitude_dB, psd_dB = DDS_spectral_data
                    self.spectrum2_plot.update(freq, psd_dB)        # Aktualizace spektrální výkonové hustoty
            except Exception as e:
                logging.error(f"Can't calculate spectral data: {e}")

    def update_ui_fast(self):
        """"Aktualizuje IQ plot (děsně rychle)"""
        if self.can.DTO_thread and self.can.DTO_thread.is_alive() and self.can.device_connected:
            self.iq_widget.update_plot(self.can.I_buffer, self.can.Q_buffer)

    def update_plots(self):
        """Aktualizuje všechny grafy."""
        self.graph_manager.update_graph("phase_dev", self.can.phase_A_rad)
        self.graph_manager.update_graph(
            ["CH1_mag", "CH2_mag"],
            {"CH1_mag": self.can.CH1_mag.contents.value, "CH2_mag": self.can.CH2_mag.contents.value}
        )
        self.graph_manager.update_graph("frequency_dev", self.can.dF_Hz)
        self.graph_manager.update_graph("frequency_DDS", self.can.DDS_Hz)

    def clear_all_plots(self):
        """Vymaže všechny grafy."""
        self.graph_manager.reset_all()
        self.iq_widget.reset()

    # === další funkce GUI ===
    def load_styles(self):
        """Načte stylesheet GUI."""
        return """

        QWidget { background-color: black; color: white; }
        QPushButton { background-color: black; color: white; border: 1px solid white; padding: 5px; }
        QPushButton:hover { background-color: #D3D3D3; color: black; }
        QPushButton:pressed { background-color: #A9A9A9; color: black; }
        QPushButton:disabled { background-color: #333333; color: #666666; }
        QMenuBar, QMenu { background-color: black; color: white; border: 1px solid white; }
        QMenuBar::item:selected, QMenu::item:selected { background-color: #D3D3D3; color: black; }
        QMenuBar::item:pressed, QMenu::item:pressed { background-color: #A9A9A9; color: black; }
        QGroupBox {border: 1px solid #333333; margin-top: 10px; padding: 1px;}
        QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; background-color: black; color: #666666; padding: 2px 2px; border-radius: 0px; font-weight: bold; spacing: 10px; }
        QProgressBar {border: 1px solid gray; background-color: black;}
        QProgressBar::chunk {background-color: #444444;}
        QSlider::groove:horizontal {background-color: #333333; border: 1px solid; height: 2px; margin: 0px; }
        QSlider::handle:horizontal {background-color:  white; border: 2px  black; height: 10px; width: 10px; margin: -15px 0px; }        
        QSlider::handle:horizontal:hover {background-color: #666666;}
        QSlider::handle:horizontal:disabled {background-color: #333333;}
        QSpinBox:disabled {background-color: #222222; color: #999999;}
        QTabBar::tab { background: #222222; color: white; padding: 5px 13px; font-weight: bold; border: none; border-bottom: 1px solid #04D9FF; min-width: 100px;}
        QTabBar::tab:selected {background: #04D9FF; color: black; }
        QTabWidget::pane {border: 1px solid #04D9FF; top: -1px;}
        QComboBox { background-color: black; color: white; border: 1px solid gray; padding: 2px 5px; border-radius: none; min-width: 80px; }
        QComboBox QAbstractItemView { background-color: black; color: white; selection-background-color: white; selection-color: black; border: 1px solid gray; padding: 2px 2px; }
        QComboBox::drop-down { border-left: 1px solid gray; background: black; padding: 4px 10px; }
        QComboBox::down-arrow {width: 6px; height: 8px; image: url("images/arrow_down.png");    }
        QToolTip {background-color: yellow;  color: black; border: black solid 1px }
        QCheckBox::indicator::unchecked {width: 16px; height: 16px; }
        QCheckBox::indicator:checked { border: 2px solid #04D9FF; image: url(images/checkbox.png);}

        """

    def closeEvent(self, event):
        """AAkce při zavření okna."""
        self.save_app_config()  # Uložení konfigurace aplikace
        self.can.stop_rx_thread()
        event.accept()  # Zavře okno správně
        self.log_plain("Exiting Trosca. Goodbye")

# -----------------------------------------------------
# Přídy dalších widgetů
# ----------------------------------------------------

class SlidBox(QWidget):
    """Kombinovaný spinbox a slider s navzájem propojenými hodnotami."""
    def __init__(self, minimum=0, maximum=100, initial=0, callback=None):
        super().__init__()

        self._minimum = minimum
        self._maximum = maximum
        self._callback = callback
        self._internal_change = False
        self._last_spinbox_value = initial
        self._user_editing = False

        self.slider = QSlider(Qt.Horizontal)
        self.spinbox = QSpinBox()

        self.slider.setRange(minimum, maximum)
        self.spinbox.setRange(minimum, maximum)

        self.slider.setValue(self._clamp(initial))
        self.spinbox.setValue(self._clamp(initial))

        layout = QHBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.spinbox)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self._slider_changed)
        self.spinbox.editingFinished.connect(self._spinbox_done_editing)
        self.spinbox.installEventFilter(self) # Přidání event filter na spinbox - automatické sledování událostí - přímo zabudované v Qt


    def _clamp(self, value):
        """Ořízne číslo do rozsahu"""
        return max(self._minimum, min(self._maximum, value)) # Omezí hodnotu na rozsah

    def _slider_changed(self, value):
        """Zjišťuje zda se hodnota změnila"""
        if not self._internal_change:
            self._internal_change = True
            self.spinbox.setValue(value)
            self._internal_change = False
            if self._callback:
                self._callback()
            self._last_spinbox_value = value

    def _spinbox_done_editing(self):
        """Zjišťuje zda uživatel dopsal číslo"""
        if self._internal_change:
            return
        value = self._clamp(self.spinbox.value())
        if value != self._last_spinbox_value:
            self._internal_change = True
            self.slider.setValue(value)
            self.spinbox.setValue(value)  
            self._internal_change = False
            self._last_spinbox_value = value
            if self._callback:
                self._callback()

    def set_value(self, value):
        """Externí nastavení hodnoty – nevyvolá callback"""
        if self._user_editing:
            return  # pokud právě upravuju hodnotu, nezmění se hodnota zvenčí
        clamped = self._clamp(value)
        self._internal_change = True
        self.slider.setValue(clamped)
        self.spinbox.setValue(clamped)
        self._internal_change = False

    def value(self):
        """Vrátí aktuální hodnotu slideru."""
        return self.slider.value()

    def set_enabled(self, enabled):
        """Povolí nebo zakáže widget."""
        self.slider.setEnabled(enabled)
        self.spinbox.setEnabled(enabled)

    def set_callback(self, callback):
        """Nastaví callback, který se zavolá při změně hodnoty."""
        self._callback = callback

    def eventFilter(self, source, event):
        """Zachytává události focusu na spinboxu."""
        if source == self.spinbox:
            if event.type() == event.FocusIn:
                self._user_editing = True
            elif event.type() == event.FocusOut:
                self._user_editing = False
        return super().eventFilter(source, event)
       
class IQWidget(QWidget):
    """
    Widget pro zobrazení IQ grafu.
    Zobrazí body v I/Q prostoru s různými barvami a velikostmi podle stáří bodů.
    """
    def __init__(self, x=150, y=150, parent=None, primary_color=(0, 255, 255, 255), secondary_color=(255, 0, 0, 255), title="IQ graf"):
        super().__init__(parent)

        self.setFixedSize(x, y)
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.IQ_plot_widget = pg.PlotWidget()
        html_title = f"<b>{title}</b>"
        self.IQ_plot_widget.setTitle(html_title, color=self.primary_color, size='10pt')
        self.IQ_plot_widget.setAspectLocked(True)
        self.IQ_plot_widget.showGrid(x=True, y=True)
        self.IQ_plot_widget.getPlotItem().hideButtons()
        self.IQ_plot_widget.getPlotItem().setLabel('left', 'Q (-)')
        self.IQ_plot_widget.getPlotItem().setLabel('bottom', 'I (-)')
        self.IQ_plot_widget.setXRange(-40000, 40000)
        self.IQ_plot_widget.setYRange(-40000, 40000)

        self.scatter = pg.ScatterPlotItem()
        self.IQ_plot_widget.addItem(self.scatter)
        layout.addWidget(self.IQ_plot_widget)


    def update_plot(self, I_buffer, Q_buffer):
        """Aktualizuje IQ graf s body na základě předaných bufferů."""
        # Získání dat z bufferů
        I_data = list(I_buffer)[-len(I_buffer):]
        Q_data = list(Q_buffer)[-len(Q_buffer):]    

        spots = []
        for idx, (i, q) in enumerate(zip(I_data, Q_data)):
            if idx == len(I_data) - 1:
                # Nejnovější bod
                color = self.primary_color
                size = 10
                alpha = 255
            else:
                age_factor = idx / len(I_data)
                size = 6 + 4 * (age_factor)
                alpha = int(180 * (age_factor))
                color = (*self.secondary_color[:3], alpha)

            spots.append({
                'pos': (i, q),
                'brush': pg.mkBrush(color),
                'size': size
            })

        self.scatter.setData(spots)

class Graph(QWidget):
    """
    Widget pro zobrazení grafu časových hodnot.
    Umožňuje zobrazit více datových řad s možností legendy a digitálních ukazatelů hodnot.
    """
    def __init__(self, names, title, xlabel, ylabel, units, history_length, update_interval_ms, parent=None, with_legend=False, minimum_height=170):
        super().__init__(parent)

        self.names = names if isinstance(names, list) else [names]
        self.history_length = history_length
        self.update_interval_ms = update_interval_ms
        self.units = units  
        self.x_data = []
        self.y_data = {name: [] for name in self.names}

        # Hlavní layout widgetu
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Vytvoření grafu
        self.plot_widget = pg.PlotWidget(parent)
        html_title = f"<b>{title}</b>"
        self.plot_widget.setTitle(html_title, color=parent.accent_color, size='10pt')
        self.plot_widget.setLabel('bottom', xlabel)
        self.plot_widget.setMinimumHeight(minimum_height)  # Nastavení minimální výšky grafu
        self.plot_widget.setLabel('left', ylabel, units=units)
        self.plot_widget.showGrid(x=True, y=True)

        # Přidání legendy, pokud je zapnutá
        if with_legend:
            self.legend = self.plot_widget.addLegend()
            self.legend.anchor((1, 1), (1, 1))

        # Křivky grafu
        self.curves = {}
        color_cycle = [parent.accent_color, 'r', 'g', 'b', 'm', 'c', 'w']
        for idx, name in enumerate(self.names):
            color = color_cycle[idx % len(color_cycle)]
            self.curves[name] = self.plot_widget.plot(pen=color, name=name)  # Přidání názvu křivky pro legendu

        # Přidání grafu do layoutu
        self.layout.addWidget(self.plot_widget)

        # Widgety pro digitální ukazatele hodnot
        self.value_labels = {}
        self.value_layout = QHBoxLayout()
        for name in self.names:
            label = QLabel(f"{name}: 0 {self.units}")
            label.setStyleSheet("color: white; font-size: 10pt; font-weight: bold;")
            self.value_labels[name] = label
            self.value_layout.addWidget(label)

        # Přidání digitálních ukazatelů pod graf
        self.layout.addLayout(self.value_layout)

    def update(self, values):
        """Aktualizuje graf novými hodnotami."""
        if not isinstance(values, dict):
            values = {self.names[0]: values}

        for name, value in values.items():
            if name in self.y_data:
                self.y_data[name].append(value)

                # Pokud je délka dat větší než historie, odstraň staré hodnoty
                if len(self.y_data[name]) > self.history_length:
                    self.y_data[name].pop(0)

        # Aktualizace osy X (časové hodnoty)
        self.x_data = [self.update_interval_ms * (x - len(self.y_data[self.names[0]])) / 1000 for x in range(len(self.y_data[self.names[0]]))]

        # Aktualizace křivek a digitálních ukazatelů
        for name in self.names:
            self.curves[name].setData(self.x_data, self.y_data[name])

            # Aktualizace digitálního ukazatele
            if self.y_data[name]:
                current_value = self.y_data[name][-1]
                self.value_labels[name].setText(f"{name} = {current_value:.2f} ({self.units})")

    def reset(self):
        """Resetuje data grafu."""
        self.x_data = []
        for name in self.names:
            self.y_data[name] = []
            self.curves[name].setData([], [])
            self.value_labels[name].setText(f"{name} = ??? ({self.units})")

    def update_graph_settings(self, history_length=None, update_interval_ms=None):
        """Aktualizuje nastavení grafu (délku historie a periodu obnovení)."""
        if history_length is not None:
            self.history_length = history_length
            for name in self.names:
                if len(self.y_data[name]) > history_length:
                    self.y_data[name] = self.y_data[name][-history_length:]

        if update_interval_ms is not None:
            self.update_interval_ms = update_interval_ms

class GraphManager:
    """
    Spravuje více grafů a umožňuje jejich přidávání, aktualizaci a resetování.
    Umožňuje také aktualizaci nastavení grafů.
    """
    def __init__(self):
        self.graphs = {}

    def add_graph(self, names, title, xlabel, ylabel, units, history_length, update_interval_ms, parent=None, with_legend=False):
        """Přidá nový graf."""
        graph = Graph(names, title, xlabel, ylabel, units, history_length, update_interval_ms, parent, with_legend)
        key = "_".join(names) if isinstance(names, list) else names
        self.graphs[key] = graph
        return graph

    def update_graph(self, names, values):
        """Aktualizuje graf podle názvu nebo názvů."""
        key = "_".join(names) if isinstance(names, list) else names
        if key in self.graphs:
            self.graphs[key].update(values)

    def reset_graph(self, names):
        """Resetuje graf podle názvu nebo názvů."""
        key = "_".join(names) if isinstance(names, list) else names
        if key in self.graphs:
            self.graphs[key].reset()

    def update_graph_settings(self, names, history_length=None, update_interval_ms=None):
        """Aktualizuje nastavení grafu (délku historie a periodu obnovení)."""
        key = "_".join(names) if isinstance(names, list) else names
        if key in self.graphs:
            self.graphs[key].update_graph_settings(history_length, update_interval_ms)

    def reset_all(self):
        """Resetuje všechny grafy."""
        for graph in self.graphs.values():
            graph.reset()

def format_value_with_units(value, unit):
    """Převede hodnotu na vhodný řád a přidá odpovídající jednotku."""
    prefixes = [
        (1e9, "G"),    # giga
        (1e6, "M"),    # mega
        (1e3, "k"),    # kilo
        (1e0, ""),   # bez prefixu
        (1e-3, "m"),   # mili
        (1e-6, "μ"),   # mikro
        (1e-9, "n"),   # nano
        (1e-12, "p")   # piko
    ]

    for factor, prefix in prefixes:
        if abs(value) >= factor:
            return f"{value / factor:.2f} {prefix}{unit}"

    # Pokud hodnota neodpovídá žádnému prefixu, vrátíme ji s původní jednotkou
    return f"{value:.2f} {unit}"

class SpectrumPlot:
    """
    Widget pro zobrazení spektrálního grafu.
    """
    def __init__(self, title, xlabel, ylabel, yunit, width=400, height=200, parent=None):
        """Inicializuje spektrální graf."""
        self.plot_widget = pg.PlotWidget(parent)
        self.plot_widget.setMinimumSize(width, height)
        html_title = f"<b>{title}</b>"
        self.plot_widget.setTitle(html_title, color='#04D9FF', size='10pt')
        self.plot_widget.setLabel('left', f"{ylabel} {yunit}")
        self.plot_widget.setLabel('bottom', xlabel)
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLogMode(x=True, y=False)  # Logaritmická osa x
        self.plot_widget.setMouseEnabled(x=True, y=False)
        
        # Nastavení počátečního rozsahu osy Y
        self.current_max_y = -30  # Počáteční horní doraz
        self.current_min_y = -80
        self.plot_widget.setYRange(-self.current_min_y, self.current_max_y)  # Dolní limit -80 dB

        # Křivka grafu
        self.curve = self.plot_widget.plot(pen='y')  # Žlutá čára

    def update(self, freqs, spectrum_db):
        """Aktualizuje data spektrálního grafu."""
        self.curve.setData(freqs, spectrum_db)
        # Dynamické nastavení horního dorazu osy Y
        max_value = max(spectrum_db)
        min_value = min(spectrum_db)
        if max_value > self.current_max_y:
            self.current_max_y = max_value
            self.plot_widget.setYRange(self.current_min_y, self.current_max_y)  # Aktualizace horního dorazu
        if min_value < self.current_min_y:
            self.current_min_y = min_value
            self.plot_widget.setYRange(self.current_min_y, self.current_max_y)


    def reset(self):
        """Resetuje spektrální graf."""
        self.curve.setData([], [])
        self.current_max_y = -30  # Počáteční horní doraz
        self.current_min_y = -80
        self.plot_widget.setYRange(-self.current_min_y, self.current_max_y)  

# -----------------------------------------------------
# Třídy dalších oken
# ----------------------------------------------------

class SettingsDialog(QDialog):
    """
    Dialog pro nastavení aplikace.
    Umožňuje uživateli nastavit parametry časových diagramů, spekter a cesty k souborům.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nastavení aplikace")
        self.setMinimumWidth(300)

        # Hlavní layout
        main_layout = QVBoxLayout(self)

        # Vytvoření záložek
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # --- Záložka Časové diagramy ---
        time_tab = QWidget()
        time_layout = QFormLayout(time_tab)

        self.samples_spin = QSpinBox()
        self.samples_spin.setRange(1, 10000)
        self.samples_spin.setValue(parent.history_seconds)
        time_layout.addRow("Délka historie (s):", self.samples_spin)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(10, 5000)
        self.interval_spin.setValue(parent.update_interval_ms)
        time_layout.addRow("Perioda obnovení (ms):", self.interval_spin)

        self.iq_plot_interval_spin = QSpinBox()
        self.iq_plot_interval_spin.setRange(1, 1000)
        self.iq_plot_interval_spin.setValue(parent.IQ_plot_update_interval_ms)
        time_layout.addRow("Perioda obnovení IQ grafu (ms):", self.iq_plot_interval_spin)

        self.iq_plot_history_spin = QSpinBox()
        self.iq_plot_history_spin.setRange(1, 1000)
        self.iq_plot_history_spin.setValue(parent.IQ_plot_history_samples)
        time_layout.addRow("Délka historie IQ grafu (samples):", self.iq_plot_history_spin)

        self.tabs.addTab(time_tab, "Časové diagramy")

        # --- Záložka Spektra ---
        spectrum_tab = QWidget()
        spectrum_layout = QFormLayout(spectrum_tab)

        self.spectrum_interval_spin = QSpinBox()
        self.spectrum_interval_spin.setRange(100, 10000)
        self.spectrum_interval_spin.setValue(parent.spectrum_update_interval_ms)
        spectrum_layout.addRow("Perioda obnovení spekter (ms):", self.spectrum_interval_spin)

        
        label = QLabel("Spektrum PSD fázového šumu:")
        label.setStyleSheet("font-weight: bold; color: #04D9FF;")  # Volitelné zvýraznění
        spectrum_layout.addRow(label)

        self.phase_integration_spin = QSpinBox()
        self.phase_integration_spin.setRange(1, 100)
        self.phase_integration_spin.setValue(parent.phase_integration_time)
        spectrum_layout.addRow("Integrační čas (s):", self.phase_integration_spin)

        self.phase_window_type = QComboBox()
        self.phase_window_type.addItems(["Hanning", "Hamming", "Blackman", "Rectangular"])
        self.phase_window_type.setCurrentText(parent.phase_window_type)
        spectrum_layout.addRow("Typ okna:", self.phase_window_type)

        spectrum_layout.addRow(QLabel("Spektrum PSD akčního zásahu DDS:"))


        self.tabs.addTab(spectrum_tab, "Spektra")
        self.DDS_integration_spin = QSpinBox()
        self.DDS_integration_spin.setRange(1, 100)
        self.DDS_integration_spin.setValue(parent.DDS_integration_time)
        spectrum_layout.addRow("Integrační čas (s):", self.DDS_integration_spin)

        self.DDS_window_type = QComboBox()
        self.DDS_window_type.addItems(["Hanning", "Hamming", "Blackman", "Rectangular"])
        self.DDS_window_type.setCurrentText(parent.DDS_window_type)
        spectrum_layout.addRow("Typ okna:", self.DDS_window_type)

        # ______________ Záložka Cesty _______________________
        paths_tab = QWidget()
        paths_layout = QFormLayout(paths_tab)

        # CAN soubor
        self.can_file_edit = QLineEdit(parent.can_file_name)
        paths_layout.addRow("CAN konfigurační soubor:", self.can_file_edit)

        # Data log
        self.data_log_edit = QLineEdit(parent.data_log_path)
        paths_layout.addRow("Soubor pro záznam dat:", self.data_log_edit)

        # Event log
        self.event_log_edit = QLineEdit(parent.event_log_path)
        paths_layout.addRow("Soubor pro logování událostí:", self.event_log_edit)

        # (Případně další cesty zde...)

        self.tabs.addTab(paths_tab, "Cesty")

        # Tlačítko OK
        self.ok_button = QPushButton("   OK    ")
        self.ok_button.clicked.connect(self.accept)
        main_layout.addWidget(self.ok_button, alignment=Qt.AlignRight)

        


    def get_values(self):
        """Vrátí hodnoty z nastavení."""
        return (
            self.samples_spin.value(),
            self.interval_spin.value(),
            self.iq_plot_interval_spin.value(),
            self.iq_plot_history_spin.value(),

            self.spectrum_interval_spin.value(),
            self.phase_integration_spin.value(),
            self.DDS_integration_spin.value(),
            self.phase_window_type.currentText(),
            self.DDS_window_type.currentText(),
            # cesty:
            self.can_file_edit.text(),
            self.data_log_edit.text(),
            self.event_log_edit.text()
        )
 
class OscillatorSettingsWindow(QMainWindow):
    """
    Hlavní okno pro nastavení oscilátoru.
    Umožňuje uživateli upravit parametry NCO, DA1 a DA2 větví oscilátoru.
    """
    def __init__(self, parent=None, CANOpenID=47):
        super().__init__(parent)
        self.setWindowTitle("Nastavení oscilátoru")
        self.setGeometry(100, 100, 800, 500)  # Nastavení velikosti okna

        # Uložení CANOpenID
        self.CANOpenID = CANOpenID

        # Historie a perioda grafů
        self.update_interval_ms = parent.spectrum_update_interval_ms

        #seznam proměnných
        self.variables = [        
            #NCO loop filter
            {
                "name": "NCO_loop_filter input",
                "index": 0x200B,
                "subindex": 0x01,
                "mapping": {
                    "Phase det": 0,
                    "DAC1": 1,
                    "DAC2": 2,
                    "I": 3,
                    "Q": 4
                },
                "type": "uint32",
                "tooltip": "Vybírá vstupní signál větve NCO (DDS)",
                "x": 386,
                "y": 337
            },

            {
                "name": "NCO_LP enable",
                "index": 0x200B,
                "subindex": 0x0B,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná vstupní dolní propust větve NCO.",
                "x": 295,
                "y": 294
            },

            {
                "name": "NCO_LP_fc (Hz)",
                "index": 0x200B,
                "subindex": 0x0A,
                "mapping": (0.0, 100000.0),
                "type": "real32", 
                "decimals": 1,
                "tooltip": "Dolní propust NCO (Hz). Nastavuje mezní frekvenci filtru. \n Rozsah: ?",
                "x": 295,
                "y": 435
            }, 

              {
                "name": "NCO_PID_Kc",
                "index": 0x200B,
                "subindex": 0x02,
                "mapping": (-1000.0, 1000),
                "type": "real32",
                "decimals": 4,
                "tooltip": "Nastavuje K parametr NCO PID.",
                "x": 188,
                "y": 435
            },
            {
                "name": "NCO_PID_PI_corner (Hz)",
                "index": 0x200B,
                "subindex": 0x03,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje I parametr NCO PID.",
                "x": 188,
                "y": 475
            },

             {
                "name": "NCO_PID_PD_corner (Hz)",
                "index": 0x200B,
                "subindex": 0x04,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje D parametr NCO PID.",
                "x": 188,
                "y": 515
            },
            {
                "name": "NCO_PID_setpoint",
                "index": 0x200B,
                "subindex": 0x08,
                "mapping": (-2048, 2047),
                "type": "int32",
                "tooltip": "Nastavuje NCO PID setpoint \n rozsah: -2048, 2047.",
                "x": 50,
                "y": 435
            },
            {
                "name": "NCO_PID_enable",
                "index": 0x200B,
                "subindex": 0x09,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná NCO PID.",
                "x": 188,
                "y": 294
            },

            #DA1 loop filter
             {
                "name": "DA1_PID input",
                "index": 0x2021,
                "subindex": 0x01,
                "mapping": {
                    "Phase det": 0,
                    "DAC2": 2,
                    "NCO dFTW": 3,
                    "I": 4,
                    "Q": 5 
                },
                "type": "uint32",
                "tooltip": "Vybírá vstupní signál větve DA1",
                "x": 515 ,
                "y": 156
            },

            {
                "name": "DA1_LP enable",
                "index": 0x2021,
                "subindex": 0x0B,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná vstupní dolní propust větve DA1.",
                "x": 630,
                "y": 198
            },

            {
                "name": "DA1_LP_fc (Hz)",
                "index": 0x2021,
                "subindex": 0x0A,
                "mapping": (0.0, 250000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Dolní propust DA1 (Hz). Nastavuje mezní frekvenci filtru. \n Rozsah: 0, 250 000 Hz",
                "x": 630,
                "y": 111
            },

             {
                "name": "DA1_PID_Kc",
                "index": 0x2021,
                "subindex": 0x03,
                "mapping": (-1000, 1000),
                "type": "real32",
                "decimals": 4,
                "tooltip": "Nastavuje K parametr DA1 PID.",
                "x": 715,
                "y": 31
            },
            {
                "name": "DA1_PID_PI_corner (Hz)",
                "index": 0x2021,
                "subindex": 0x04,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje I parametr DA1 PID.",
                "x": 715,
                "y": 71
            },
            {
                "name": "DA1_PID_PD_corner (Hz)",
                "index": 0x2021,
                "subindex": 0x05,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje D parametr DA1 PID.",
                "x": 715,
                "y": 111
            },
            {
                "name": "DA1_PID_setpoint",
                "index": 0x2021,
                "subindex": 0x08,
                "mapping": (-2048, 2047),
                "type": "int32",
                "tooltip": "Nastavuje DA1 PID setpoint \n rozsah: -2048, 2047.",
                "x": 860,
                "y": 111
            },
            {
                "name": "DA1_PID_enable",
                "index": 0x2021,
                "subindex": 0x09,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná DA1 PID.",
                "x": 715,
                "y": 198
            },

            #DA2 loop filter
            {
                "name": "DA2_PID input",
                "index": 0x2022,
                "subindex": 0x01,
                "mapping": {
                    "Phase det": 0,
                    "DAC2": 2,
                    "NCO dFTW": 3,
                    "I": 4,
                    "Q": 5
                },
                "type": "uint32",
                "tooltip": "Vybírá vstupní signál větve DA2",
                "x": 515,
                "y": 337
            },

            {
                "name": "DA2_LP enable",
                "index": 0x2022,
                "subindex": 0x0B,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná vstupní dolní propust větve DA2.",
                "x": 630,
                "y": 294
            },

            {
                "name": "DA2_LP_fc (Hz)",
                "index": 0x2022,
                "subindex": 0x0A,
                "mapping": (0.0, 250000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Dolní propust DA2 (Hz). Nastavuje mezní frekvenci filtru. \n Rozsah: 0, 250 000 Hz",
                "x": 630,
                "y": 435
            },
        
            {
                "name": "DA2_PID_Kc",
                "index": 0x2022,
                "subindex": 0x03,
                "mapping": (-1000, 1000),
                "type": "real32",
                "decimals": 4,
                "tooltip": "Nastavuje K parametr DA2 PID.",
                "x": 715,
                "y": 435
            },
            {
                "name": "DA2_PID_PI_corner (Hz)",
                "index": 0x2022,
                "subindex": 0x04,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje I parametr DA2 PID.",
                "x": 715,
                "y": 475
            },
            {
                "name": "DA2_PID_PD_corner (Hz)",
                "index": 0x2022,
                "subindex": 0x05,
                "mapping": (0, 100000.0),
                "type": "real32",
                "decimals": 1,
                "tooltip": "Nastavuje D parametr DA2 PID.",
                "x": 715,
                "y": 515
            },
            {
                "name": "DA2_PID_setpoint",
                "index": 0x2022,
                "subindex": 0x08,
                "mapping": (-2048, 2047),
                "type": "int32",
                "tooltip": "Nastavuje DA2 PID setpoint \n rozsah: -2048, 2047.",
                "x": 860,
                "y": 435
            },
            {
                "name": "DA2_PID_enable",
                "index": 0x2022,
                "subindex": 0x09,
                "mapping": {"Off": 0, "On": 1},
                "type": "uint32",
                "tooltip": "Zapíná/vypíná DA2 PID.",
                "x": 715,
                "y": 294
            }
        ]

        # Hlavní widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout pro hlavní widget
        self.layout = QVBoxLayout(self.central_widget)

        # QGraphicsView a QGraphicsScene
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)

        # Zakázání scrollbarů
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Načtení obrázku jako pozadí
        self.image_item = QGraphicsPixmapItem(QPixmap("images/schema.png"))
        self.graphics_scene.addItem(self.image_item)

        # Nastavení velikosti obrázku na fixní
        self.graphics_view.setFixedSize(self.image_item.pixmap().size())
        self.graphics_scene.setSceneRect(0, 0, self.image_item.pixmap().width(), self.image_item.pixmap().height())

        # Přidání QGraphicsView do layoutu
        self.layout.addWidget(self.graphics_view)

        # Přidání plovoucích ovládacích prvků
        self.add_floating_controls()

        # Přidání labelů
        self.add_labels()

        # Přidání tlačítek
        self.add_buttons()

        # Časovač pro aktualizaci grafů
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(self.update_interval_ms)

        # Načtení hodnot při otevření
        #self.load_settings()
        self.update_buttons()

    def refresh_on_show(self):
        """Obnoví nastavení při zobrazení okna."""
        self.load_settings()
        self.update_buttons()

    def add_labels(self):
        """Přidá labely do QGraphicsScene."""
        self.dFTW_out_label = self.add_label("dFTW_out: 0", 0, 280)
        self.DA1_out_label = self.add_label("DA1_out: 0", 862, 212)
        self.DA2_out_label = self.add_label("DA2_out: 0", 862, 295)
    
    def update_labels(self):
        """Aktualizuje hodnoty v labelech."""
        self.dFTW_out_label.setText(f"dFTW_out: {self.parent().can.dFTW_out.contents.value}")
        self.DA1_out_label.setText(f"DA1_out: {self.parent().can.DA1_out.contents.value}")
        self.DA2_out_label.setText(f"DA2_out: {self.parent().can.DA2_out.contents.value}")
    
    def add_buttons(self):
        """Přidá tlačítka."""
        button_layout = QHBoxLayout()

        self.open_button = QPushButton("Otevřít", self)
        self.open_button.clicked.connect(self.load_config)  # Připojení k metodě load_config
        button_layout.addWidget(self.open_button)

        self.save_button = QPushButton("Uložit", self)
        self.save_button.clicked.connect(self.save_config)  # Připojení k metodě save_config
        button_layout.addWidget(self.save_button)

        button_layout.addStretch()

        self.save_button = QPushButton("Nahrát do zařízení a zavřít", self)
        self.save_button.clicked.connect(self.apply_settings_and_close)
        self.save_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {self.parent().accent_color};  color: white; }}
            QPushButton:hover {{
                background-color: {self.parent().accent_color}; color: black;}}
            """)
        button_layout.addWidget(self.save_button)

        self.apply_button = QPushButton("Nahrát do zařízení", self)
        self.apply_button.clicked.connect(self.apply_settings)  # Uloží nastavení, ale nezavře okno
        button_layout.addWidget(self.apply_button)

        # Přidání tlačítka "Načíst znovu"
        self.reload_button = QPushButton("Načíst ze zařízení", self)
        self.reload_button.clicked.connect(self.load_settings)  # Připojení k metodě load_settings
        button_layout.addWidget(self.reload_button)

        self.cancel_button = QPushButton("Zavřít", self)
        self.cancel_button.clicked.connect(self.close)  # Zavře okno bez uložení
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

    def update_buttons(self):
        """Aktualizuje povolení tlačítek zápisu na základě stavu přepínače TX."""
        can_tx_enabled = getattr(self.parent().can, "enable_can_tx", False)
        self.save_button.setEnabled(can_tx_enabled)
        self.apply_button.setEnabled(can_tx_enabled)

    def add_dropdown(self, x, y, options):
        """
        Přidá dropdown (QComboBox) na zadanou pozici s danými možnostmi.

        Args:
            x (int): X-ová pozice na obrázku.
            y (int): Y-ová pozice na obrázku.
        """
        dropdown = QComboBox()
        dropdown.addItems(options)
        dropdown_proxy = QGraphicsProxyWidget()
        dropdown_proxy.setWidget(dropdown)
        dropdown_proxy.setPos(x, y)  # Nastavení pozice na obrázku
        self.graphics_scene.addItem(dropdown_proxy)
        return dropdown
        
    def add_label(self, text, x, y):
        """Vytvoří QLabel a přidá ho do QGraphicsScene.

        Args:
            text (str): Text, který se má zobrazit v labelu.
            x (int): X-ová pozice na obrázku.
            y (int): Y-ová pozice na obrázku.
        """
        #konverze čísla na text
        if isinstance(text, (int, float)):
            text = str(text)
        label = QLabel(text)
        label.setStyleSheet("color: white; background-color: gray; padding: 2px;")
        label.setMinimumWidth(150)  # Nastavení minimální šířky
        label.setMinimumHeight(20)  # Nastavení minimální výšky
        label.setAlignment(Qt.AlignCenter)  # Zarovnání textu na střed
        label_proxy = QGraphicsProxyWidget()
        label_proxy.setWidget(label)
        label_proxy.setPos(x, y)
        self.graphics_scene.addItem(label_proxy)
        return label
    
    def add_spinbox(self, label, x, y, min_value, max_value, is_double=False, decimals=2):
        """
        Přidá spinbox na zadanou pozici.

        Args:
            label (str): Textový popisek pro spinbox.
            x (int): X-ová pozice na obrázku.
            y (int): Y-ová pozice na obrázku.
            min_value (float): Minimální hodnota spinboxu.
            max_value (float): Maximální hodnota spinboxu.
            is_double (bool): Pokud True, použije QDoubleSpinBox.
        """
        if is_double:
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(decimals)  # Nastavení počtu desetinných míst
        else:
            spinbox = QSpinBox()

        spinbox.setRange(min_value, max_value)
        spinbox_proxy = QGraphicsProxyWidget()
        spinbox_proxy.setWidget(spinbox)
        spinbox_proxy.setPos(x, y)
        self.graphics_scene.addItem(spinbox_proxy)

        text_label = QLabel(label)
        label_proxy = QGraphicsProxyWidget()
        label_proxy.setWidget(text_label)
        label_proxy.setPos(x, y - 15)  # Popisek umístěn nad spinboxem
        self.graphics_scene.addItem(label_proxy)
        return spinbox

    def add_floating_controls(self):
        """Přidá plovoucí ovládací prvky na obrázek na základě tabulky variables."""
        for var in self.variables:
            name = var["name"]
            mapping = var["mapping"]
            x = var.get("x", 0) 
            y = var.get("y", 0) 
            value_type = var.get("type", "int32")
            decimals = var.get("decimals", 2)
            tooltip = var.get("tooltip", "")

            # Vytvoření widgetu na základě typu
            if isinstance(mapping, dict):  # Dropdown
                dropdown = self.add_dropdown(x, y, list(mapping.keys()))
                if tooltip:
                    dropdown.setToolTip(tooltip)
                setattr(self, name, dropdown)
            elif isinstance(mapping, tuple):  # Spinbox (rozsah hodnot)
                min_value, max_value = mapping
                
                # Určí zda použít QDoubleSpinBox nebo QSpinBox
                is_double = isinstance(min_value, float) or isinstance(max_value, float) or value_type == "real32"
                spinbox = self.add_spinbox(name, x, y, min_value, max_value, is_double=is_double, decimals = decimals)
                if tooltip:
                    spinbox.setToolTip(tooltip)
                setattr(self, name, spinbox)

    def load_settings(self):
        """Načte hodnoty všech widgetů pomocí can_rx_SDO."""
        logging.info(f"\n[LOADING] Loading SDO values from device")
        indent = " " * 10
        self.parent().log_plain(f"{indent}{'Name':<25} {'Index':<10} {'Subindex':<10} {'Value':<10}")
        self.parent().log_plain(f"{indent}{'-' * 60}")

        for var in self.variables:
            name = var["name"]
            index = var["index"]
            subindex = var["subindex"]
            mapping = var["mapping"]
            value_type = var.get("type", "int32")

            # Načtení hodnoty pomocí SDO
            self.parent().can.can_rx_SDO(CANOpenID=self.CANOpenID, index=index, subindex=subindex)
            # Čekání na přijetí dat
            time.sleep(0.1)

            # Získání hodnoty
            raw_value = self.parent().can.sdo_data.contents.value

            # Dekódování podle typu
            if value_type == "real32":
                value = struct.unpack('<f', struct.pack('<I', raw_value))[0]
            elif value_type == "uint32":
                value = raw_value & 0xFFFFFFFF
            elif value_type == "int32":
                value = struct.unpack('<i', struct.pack('<I', raw_value))[0]
            else:
                value = raw_value

            self.parent().log_plain(f"{indent}{name:<25} {index:<10X} {subindex:<10X} {value:<10}")

            # Rozlišení typu mapping
            if isinstance(mapping, dict):  # Dropdown
                value_text = next((k for k, v in mapping.items() if v == value), None)
                if value_text is not None:
                    widget = getattr(self, name)
                    widget.setCurrentText(value_text)
            elif isinstance(mapping, tuple):  # Spinbox
                min_value, max_value = mapping
                if min_value <= value <= max_value:
                    widget = getattr(self, name)
                    widget.setValue(value)
        logging.info("SDO values loaded from device")

    def apply_settings(self):
        self.save_settings()  # Uložení nastavení
    
    def apply_settings_and_close(self):
        self.save_settings()
        self.close()  # Zavře okno po uložení nastavení

    def save_settings(self):
        """Zpracuje nastavení všech widgetů a odešle příslušné SDO packety."""
        self.parent().logging.info("\n[LOADING] Saving config to device...")
        # Hlavička tabulky
        indent = " " * 10
        self.parent.log_plain(f"{indent}{'Name':<25} {'Index':<10} {'Subindex':<10} {'Value':<10}")
        self.parent.log_plain(f"{indent}{'-' * 60}")
        for var in self.variables:
            name = var["name"]
            index = var["index"]
            subindex = var["subindex"]
            mapping = var["mapping"]
            value_type = var.get("type", "int32")

            # Získání hodnoty z widgetu
            widget = getattr(self, name)

            if isinstance(mapping, dict):  # Dropdown
                value_raw = widget.currentText()
                value = mapping.get(value_raw, -1)
            elif isinstance(mapping, tuple):  # Spinbox
                value_raw = widget.value()

                if value_type == "real32":
                    value_bytes = struct.pack('<f', float(value_raw))
                    value = struct.unpack('<I', value_bytes)[0]
                elif value_type == "uint32":
                    value = int(value_raw) & 0xFFFFFFFF
                elif value_type == "int32":
                    value = int(value_raw)
                else:
                    value = int(value_raw)

            # Odeslání SDO packetu
            # Výpis do tabulky
            self.parent().log_plain(f"{indent}{name:<25} {index:<10X} {subindex:<10X} {value_raw:<10}")

            self.parent().can.can_tx_SDO(CANOpenID=self.CANOpenID, index=index, subindex=subindex, data=value)
        time.sleep(0.5)
        self.parent().one_shot_update()  # Aktualizace grafu po každém odeslání SDO

    def save_config(self):
        """Uloží aktuální hodnoty SDO do JSON souboru."""
        config = {}
    
        for var in self.variables:
            name = var["name"]
            index = var["index"]
            subindex = var["subindex"]
            mapping = var["mapping"]
    
            # Získání hodnoty z widgetu
            widget = getattr(self, name)
            if isinstance(mapping, dict):  # Dropdown
                value_text = widget.currentText()
                value = mapping.get(value_text, -1)
            elif isinstance(mapping, tuple):  # Spinbox
                value = widget.value()
    
            config[f"{index:04X}:{subindex:02X}"] = value
    
        # Uložení do souboru
        file_name, _ = QFileDialog.getSaveFileName(self, "Uložit konfiguraci", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, "w") as file:
                json.dump(config, file, indent=4)
            logging.info(f"Configuration saved to {file_name}")

    def load_config(self):
        """Načte hodnoty SDO z JSON souboru a aktualizuje widgety."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Otevřít konfiguraci", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, "r") as file:
                    config = json.load(file)
    
                for var in self.variables:
                    name = var["name"]
                    index = var["index"]
                    subindex = var["subindex"]
                    mapping = var["mapping"]
    
                    key = f"{index:04X}:{subindex:02X}"
                    if key in config:
                        value = config[key]
    
                        # Aktualizace widgetu
                        widget = getattr(self, name)
                        if isinstance(mapping, dict):  # Dropdown
                            value_text = next((k for k, v in mapping.items() if v == value), None)
                            if value_text is not None:
                                widget.setCurrentText(value_text)
                        elif isinstance(mapping, tuple):  # Spinbox
                            widget.setValue(value)
    
                logging.info(f"Configuration loaded from {file_name}")
            except Exception as e:
                logging.error(f"Failed to load configuration: {e}")

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("O aplikaci")
        self.setFixedSize(300, 200)  # Nastavení pevné velikosti okna

        # Layout
        layout = QVBoxLayout()

        icon_label = QLabel(self)
        pixmap = QPixmap("images/icon_46x42.png")  # Cesta k ikoně aplikace
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Přidání textu o aplikaci
        about_label = QLabel("TrOSCa - Tracking Oscillator Control Application\n\n"
                             "Verze: 0.2\n"
                             "Autor: Jindřich Zoabč\n\n"
                             "Tato aplikace slouží k ovládání karty Digital Tracking Oscilátoru\n"
                             )
        about_label.setWordWrap(True)  # Povolení zalamování textu
        about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_label)

        # Tlačítko Zavřít
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

class ExportSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nastavení exportu dat")
        layout = QVBoxLayout(self)

        # Výběr proměnných (checkboxy)
        self.var_checks = []
        self.variables = ["phase_A_rad", "DDS_Hz", "I_A", "Q_A", "dFTW_out", "DA1_out", "DA2_out", "CH1_mag", "CH2_mag"]
        group = QGroupBox("Ukládat proměnné:")
        group_layout = QVBoxLayout()
        for var in self.variables:
            cb = QCheckBox(var)
            if var in self.parent().data_log_variables:
                cb.setChecked(True)
            else:
                cb.setChecked(False)
            self.var_checks.append(cb)
            group_layout.addWidget(cb)
        group.setLayout(group_layout)
        layout.addWidget(group)

        # Interval
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(0, 10000)
        self.interval_spin.setValue(self.parent().data_log_interval_ms)
        layout.addWidget(QLabel("Interval ukládání (ms):"))
        layout.addWidget(self.interval_spin)

        # Cesta k souboru
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setText(self.parent().data_log_path)
        layout.addWidget(QLabel("Cesta k souboru:"))
        path_layout.addWidget(self.path_edit)
        
        #Tlačítko na nastavení cesty přes dialog
        self.path_button = QPushButton("Vybrat soubor")
        self.path_button.clicked.connect(self.open_file)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)

        # Oddělovač
        self.separator_edit = QLineEdit()
        self.separator_edit.setText(self.parent().data_log_separator)
        layout.addWidget(QLabel("Oddělovač:"))
        layout.addWidget(self.separator_edit)

        # Časovač
        hours = self.parent().data_log_duration_s//(60**2)
        minutes = (self.parent().data_log_duration_s-hours*60**2)//60
        seconds = (self.parent().data_log_duration_s-hours*60**2-minutes*60)

        layout.addWidget(QLabel("Délka záznamu (HH:MM:SS, 0 = neomezeně):"))
        duration_layout = QHBoxLayout()

        self.duration_spin_h = QSpinBox()
        self.duration_spin_h.setRange(0, 23)
        self.duration_spin_h.setValue(hours)
        duration_layout.addWidget(self.duration_spin_h)

        self.duration_spin_m = QSpinBox()
        self.duration_spin_m.setRange(0, 59)
        self.duration_spin_m.setValue(minutes)
        duration_layout.addWidget(self.duration_spin_m)

        self.duration_spin_s = QSpinBox()
        self.duration_spin_s.setRange(0, 59)
        self.duration_spin_s.setValue(seconds)
        duration_layout.addWidget(self.duration_spin_s)

        layout.addLayout(duration_layout)

        # OK tlačítko
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def get_values(self):
        variables = [cb.text() for cb in self.var_checks if cb.isChecked()]
        interval = self.interval_spin.value()
        path = self.path_edit.text()
        separator = self.separator_edit.text()
        duration = self.duration_spin_h.value()*60**2 + self.duration_spin_m.value()*60 + self.duration_spin_s.value()
        return variables, interval, path, separator, duration
    
    def open_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Vyberte nový soubor", self.parent().data_log_path, "CSV Files (*.csv);;All Files (*)")
        self.path_edit.setText(file_name)

class CANTableDialog(QMainWindow):
    def __init__(self, csv_path, parent=None):
        super().__init__(parent)

        self.setGeometry(100, 100, 800, 500)  # Nastavení velikosti okna
        self.setWindowTitle(f"Seznam parametrů karty: {os.path.basename(csv_path)}")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        #self.setMinimumSize(800, 400)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        import csv
        try:
            with open(csv_path, newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                if not rows:
                    return
                self.table.setColumnCount(len(rows[0]))
                self.table.setRowCount(len(rows))
                self.table.setHorizontalHeaderLabels(rows[0])
                for row_idx, row in enumerate(rows[1:], start=1):
                    for col_idx, value in enumerate(row):
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(value))
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                self.table.setAlternatingRowColors(True)
                self.table.setStyleSheet("""
                    QTableWidget {
                        color: #04D9FF;
                        background-color: #222222;
                        alternate-background-color: #111111;
                        gridline-color: #333333;
                        border: 2px solid black;                
                    }
                    QHeaderView::section {
                        color: white;
                        background-color: black;
                        font-weight: bold;
                    }

                    QTableWidget::item:selected {
                        background-color: #04D9FF;
                        color: #000000;
                    }
                """)

        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Nelze načíst CSV soubor:\n{e}")

# -----------------------------------------------------
# Hlavní část aplikace
# -----------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = GUI()
    main_window.show()

    sys.exit(app.exec_())
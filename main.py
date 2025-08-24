# main.py
import subprocess
import time
import os
from pynput import mouse
import threading
import sys

class ADBManager:
    def __init__(self):
        self.adb_path = self.get_adb_path()
        
    def get_adb_path(self):
        """Retorna o caminho completo do ADB"""
        adb_path = r"D:\projects\Share Screen\platform-tools\adb.exe"
        
        if os.path.exists(adb_path):
            print(f"✅ ADB encontrado em: {adb_path}")
            return adb_path
        else:
            print(f"❌ ADB não encontrado em: {adb_path}")
            return None
    
    def run_adb(self, command, timeout=8):
        """Executa comando ADB com timeout"""
        if not self.adb_path:
            return None
            
        try:
            full_command = [self.adb_path] + command
            result = subprocess.run(
                full_command, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                shell=True
            )
            return result
        except Exception as e:
            print(f"❌ Erro no ADB: {e}")
            return None

class ScrcpyManager:
    def __init__(self):
        self.scrcpy_path = self.find_scrcpy()
        
    def find_scrcpy(self):
        """Encontra o scrcpy instalado"""
        try:
            subprocess.run(['scrcpy', '--version'], capture_output=True, timeout=5, shell=True)
            return 'scrcpy'
        except:
            pass
        
        possible_paths = [
            r"D:\projects\Share Screen\scrcpy\scrcpy.exe",
            r"C:\Program Files\scrcpy\scrcpy.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Scrcpy encontrado em: {path}")
                return path
        
        print("❌ Scrcpy não encontrado")
        return None
    
    def start_mirroring(self, device_serial=None):
        """Inicia o espelhamento"""
        if not self.scrcpy_path:
            return False
            
        try:
            # Configurações simplificadas
            scrcpy_cmd = [
                self.scrcpy_path,
                '--video-bit-rate', '8M',
                '--max-size', '1280',
                '--window-title', 'Espelhamento Android',
                '--turn-screen-off',
                '--stay-awake',
                '--max-fps', '60',
                '--audio-codec', 'opus',
                '--audio-bit-rate', '128K',
            ]
            
            if device_serial:
                scrcpy_cmd.extend(['--serial', device_serial])
            
            print("🔄 Iniciando espelhamento...")
            
            process = subprocess.Popen(
                scrcpy_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            
            time.sleep(2)
            
            if process.poll() is None:
                print("✅ Scrcpy iniciado com sucesso!")
                return process
            else:
                return False
                
        except Exception as e:
            print(f"❌ Erro ao iniciar scrcpy: {e}")
            return False

class ConnectionManager:
    def __init__(self, adb_manager):
        self.adb = adb_manager
        
    def check_usb_connection(self):
        """Verifica se há dispositivos USB conectados"""
        print("🔍 Verificando conexão USB...")
        
        result = self.adb.run_adb(['devices'])
        if not result or not result.stdout:
            return False
        
        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:
            if 'device' in line and 'offline' not in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    serial = parts[0]
                    if ':' not in serial:
                        print(f"✅ USB conectado: {serial}")
                        return serial
        
        print("❌ Nenhum dispositivo USB encontrado")
        return False
    
    def check_wifi_connection(self):
        """Verifica se há dispositivos WiFi conectados"""
        result = self.adb.run_adb(['devices'])
        if not result or not result.stdout:
            return False
        
        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:
            if 'device' in line and 'offline' not in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    serial = parts[0]
                    if ':' in serial:
                        print(f"✅ WiFi conectado: {serial}")
                        return serial
        
        return False

class AndroidGestureController:
    def __init__(self, adb_manager, device_serial):
        self.adb = adb_manager
        self.device_serial = device_serial
        self.mouse_listener = None
        
        # Configurações do dispositivo (ajuste conforme seu celular)
        self.device_width = 1080   # Largura do display
        self.device_height = 1920  # Altura do display
        self.pc_width = 1920       # Largura da tela do PC
        self.pc_height = 1080      # Altura da tela do PC
        
        # Para clique duplo
        self.last_click_time = 0
        self.last_click_pos = None
        
    def run_adb_command(self, command):
        """Executa comando ADB"""
        if self.device_serial:
            command = ['-s', self.device_serial] + command
        return self.adb.run_adb(command, timeout=3)
        
    def convert_coordinates(self, x, y):
        """Converte coordenadas do PC para coordenadas do dispositivo"""
        device_x = int(x * self.device_width / self.pc_width)
        device_y = int(y * self.device_height / self.pc_height)
        return device_x, device_y
        
    def send_tap(self, x, y):
        """Envia toque simples"""
        self.run_adb_command(['shell', 'input', 'tap', str(x), str(y)])
        
    def send_double_tap(self, x, y):
        """Envia clique duplo para like"""
        # Primeiro clique
        self.send_tap(x, y)
        # Pequeno delay
        time.sleep(0.15)
        # Segundo clique
        self.send_tap(x, y)
        
    def send_swipe(self, x1, y1, x2, y2, duration=300):
        """Envia comando de swipe para gestos"""
        self.run_adb_command([
            'shell', 'input', 'swipe',
            str(x1), str(y1),
            str(x2), str(y2),
            str(duration)
        ])
    
    def go_back(self):
        """Volta para tela anterior (gesto de voltar)"""
        self.run_adb_command(['shell', 'input', 'keyevent', '4'])
        
    def go_home(self):
        """Vai para a home (gesto de home)"""
        self.run_adb_command(['shell', 'input', 'keyevent', '3'])
        
    def open_recent_apps(self):
        """Abre apps recentes"""
        self.run_adb_command(['shell', 'input', 'keyevent', '187'])
    
    def gesture_swipe_left(self):
        """Gesto de swipe left (mudar de app/voltar)"""
        start_x = self.device_width - 100
        end_x = 100
        y = self.device_height // 2
        self.send_swipe(start_x, y, end_x, y, 200)
    
    def gesture_swipe_right(self):
        """Gesto de swipe right (avançar)"""
        start_x = 100
        end_x = self.device_width - 100
        y = self.device_height // 2
        self.send_swipe(start_x, y, end_x, y, 200)
    
    def gesture_swipe_up(self):
        """Gesto de swipe up (home)"""
        x = self.device_width // 2
        start_y = self.device_height - 100
        end_y = self.device_height // 3
        self.send_swipe(x, start_y, x, end_y, 250)
    
    def gesture_swipe_down(self):
        """Gesto de swipe down (notifications)"""
        x = self.device_width // 2
        start_y = 100
        end_y = self.device_height // 2
        self.send_swipe(x, start_y, x, end_y, 250)

    def on_click(self, x, y, button, pressed):
        """Handle clique do mouse - SIMPLIFICADO"""
        device_x, device_y = self.convert_coordinates(x, y)
        
        if button == mouse.Button.left:
            current_time = time.time()
            
            if pressed:
                # Detecta clique duplo
                if (current_time - self.last_click_time < 0.3 and 
                    self.last_click_pos and 
                    abs(device_x - self.last_click_pos[0]) < 50 and 
                    abs(device_y - self.last_click_pos[1]) < 50):
                    
                    # Clique duplo - like no Instagram
                    threading.Thread(target=self.send_double_tap, 
                                   args=(device_x, device_y), daemon=True).start()
                    self.last_click_time = 0  # Reseta para evitar triple click
                else:
                    # Clique simples normal
                    threading.Thread(target=self.send_tap, 
                                   args=(device_x, device_y), daemon=True).start()
                    self.last_click_time = current_time
                    self.last_click_pos = (device_x, device_y)
                    
        elif button == mouse.Button.right and pressed:
            # Botão direito = voltar
            threading.Thread(target=self.go_back, daemon=True).start()
            
        elif button == mouse.Button.middle and pressed:
            # Botão do meio = home
            threading.Thread(target=self.go_home, daemon=True).start()

    def on_scroll(self, x, y, dx, dy):
        """Handle scroll do mouse"""
        if dy > 0:  # Scroll down
            self.gesture_swipe_down()
        elif dy < 0:  # Scroll up
            self.gesture_swipe_up()

    def start(self):
        """Inicia controle com gestos"""
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.mouse_listener.start()
        print("🎮 Controle com Gestos Ativado!")
        print("   🖱️  Clique esquerdo: Toque simples")
        print("   🖱️🖱️  Clique duplo rápido: Like no Instagram")
        print("   🖱️  Botão direito: Voltar (Back)")
        print("   🖱️  Botão do meio: Home")
        print("   🎯 Scroll: Notificações (↓) ou Home (↑)")
        
    def stop(self):
        """Para controle"""
        if self.mouse_listener:
            self.mouse_listener.stop()

class ScreenMirror:
    def __init__(self, adb_manager, scrcpy_manager):
        self.adb = adb_manager
        self.scrcpy = scrcpy_manager
        self.connection = ConnectionManager(adb_manager)
        self.mirror_process = None
        
    def show_instructions(self):
        """Mostra instruções"""
        print("=" * 70)
        print("📋 INSTRUÇÕES - CONTROLE SIMPLIFICADO")
        print("=" * 70)
        print("🎮 USE GESTOS NATIVOS DO ANDROID:")
        print("   🖱️  Clique: Toque normal")
        print("   🖱️🖱️  Clique DUPLO RÁPIDO: Like no Instagram")
        print("   🖱️  Botão DIREITO: Voltar (Back)")
        print("   🖱️  Botão DO MEIO: Home")
        print("   🎯 Scroll ↓: Abrir notificações")
        print("   🎯 Scroll ↑: Fechar notificações/Home")
        print("   🔊 Áudio: Ativado no computador")
        print("=" * 70)
        print("💡 DICA: Use os BOTÕES do mouse em vez de arrastar!")
        print("=" * 70)

    def setup_connection(self):
        """Configura a conexão"""
        print("🔄 Detectando conexão...")
        
        usb_serial = self.connection.check_usb_connection()
        if usb_serial:
            return usb_serial
        
        wifi_serial = self.connection.check_wifi_connection()
        if wifi_serial:
            return wifi_serial
        
        print("❌ Nenhum dispositivo encontrado")
        return None

    def start_mirroring(self, device_serial):
        """Inicia espelhamento"""
        return self.scrcpy.start_mirroring(device_serial)

    def stop_mirroring(self):
        """Para o espelhamento"""
        if self.mirror_process:
            try:
                self.mirror_process.terminate()
            except:
                pass

def main():
    print("=" * 60)
    print("           📱 ESPELHADOR ANDROID - GESTOS 📺")
    print("=" * 60)
    print("✨ Clique duplo + Gestos nativos + Sem arrasto bugado")
    print("=" * 60)
    
    adb_manager = ADBManager()
    scrcpy_manager = ScrcpyManager()
    
    if not adb_manager.adb_path:
        print("❌ ADB não encontrado")
        return
    
    mirror = ScreenMirror(adb_manager, scrcpy_manager)
    
    try:
        device_serial = mirror.setup_connection()
        if not device_serial:
            print("💡 Conecte o dispositivo via USB ou WiFi primeiro")
            return
        
        mirror.show_instructions()
        
        input("⏎ Pressione Enter para iniciar o espelhamento...")
        
        mirror_process = mirror.start_mirroring(device_serial)
        
        if mirror_process:
            mirror.mirror_process = mirror_process
            
            controller = AndroidGestureController(adb_manager, device_serial)
            controller.start()
            
            print("\n🎉 ESPELHAMENTO ATIVO!")
            print("💡 Use os BOTÕES do mouse:")
            print("   - DIREITO para Voltar")
            print("   - DO MEIO para Home") 
            print("   - DUPLO CLIQUE para Like")
            print("⏹️  Feche a janela do scrcpy para sair")
            print("=" * 60)
            
            try:
                mirror_process.wait()
            except KeyboardInterrupt:
                print("\n👋 Encerrando...")
            finally:
                controller.stop()
                mirror.stop_mirroring()
        else:
            print("❌ Falha ao iniciar espelhamento")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    finally:
        print("✅ Programa finalizado")

if __name__ == "__main__":
    main()
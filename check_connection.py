# check_connection.py
import subprocess
import time

def check_network_status():
    """Verifica status da rede e dispositivos"""
    print("🌐 Verificando status da rede...")
    
    # Verifica dispositivos ADB
    try:
        result = subprocess.run(['adb', 'devices'], 
                              capture_output=True, text=True, timeout=10)
        print("📋 Dispositivos ADB:")
        print(result.stdout)
    except:
        print("❌ ADB não disponível")
    
    # Verifica rede WiFi
    try:
        result = subprocess.run(['ipconfig'], 
                              capture_output=True, text=True, timeout=10)
        print("📶 Configuração de rede:")
        lines = result.stdout.split('\n')
        for line in lines:
            if 'IPv4' in line or 'Wi-Fi' in line:
                print(f"   {line.strip()}")
    except:
        print("❌ Não foi possível verificar rede")

if __name__ == "__main__":
    check_network_status()
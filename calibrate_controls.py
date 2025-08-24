# calibrate_controls.py
import subprocess
import time

def calibrate_controls():
    """Script para calibrar os controles"""
    print("🎯 Calibração de Controles")
    print("=" * 50)
    
    # Testa diferentes configurações
    configs = [
        {"threshold": 10, "interval": 0.03, "duration": 50},
        {"threshold": 15, "interval": 0.05, "duration": 100},
        {"threshold": 20, "interval": 0.08, "duration": 150},
        {"threshold": 25, "interval": 0.10, "duration": 200},
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n🔧 Configuração {i}:")
        print(f"   Threshold: {config['threshold']}px")
        print(f"   Interval: {config['interval']}s")
        print(f"   Duration: {config['duration']}ms")
        
        # Testa comando
        cmd = f'adb shell input swipe 100 100 300 300 {config["duration"]}'
        try:
            result = subprocess.run(cmd, shell=True, timeout=3, capture_output=True)
            if result.returncode == 0:
                print("   ✅ Funcionou")
            else:
                print("   ❌ Falhou")
        except:
            print("   ⚠️  Erro")

if __name__ == "__main__":
    calibrate_controls()
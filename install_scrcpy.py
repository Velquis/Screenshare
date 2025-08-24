# install_scrcpy.py
import subprocess
import os

def install_scrcpy():
    """Instala scrcpy automaticamente"""
    print("📦 Instalando scrcpy...")
    
    try:
        # Tenta instalar via Scoop
        print("🚀 Instalando via Scoop...")
        
        # Instala Scoop se não tiver
        try:
            subprocess.run(['scoop', '--version'], capture_output=True, check=True)
        except:
            print("⬇️  Instalando Scoop...")
            subprocess.run([
                'powershell', '-Command', 
                'irm get.scoop.sh | iex'
            ], shell=True, timeout=300)
        
        # Instala scrcpy
        print("⬇️  Instalando scrcpy...")
        result = subprocess.run([
            'powershell', '-Command',
            'scoop install scrcpy'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Scrcpy instalado com sucesso!")
            return True
        else:
            print("❌ Falha na instalação automática")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    install_scrcpy()
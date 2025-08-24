# test_adb.py
import subprocess
import os

def test_adb():
    """Testa se o ADB está funcionando"""
    adb_path = r"D:\projects\Share Screen\platform-tools\adb.exe"
    
    if not os.path.exists(adb_path):
        print("❌ ADB não encontrado no caminho especificado")
        return False
    
    try:
        # Testa versão do ADB
        result = subprocess.run(
            [adb_path, '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            shell=True
        )
        
        if result.returncode == 0:
            print("✅ ADB funciona perfeitamente!")
            print(f"📋 Versão: {result.stdout}")
            return True
        else:
            print("❌ ADB retornou erro")
            print(f"Erro: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar ADB: {e}")
        return False

if __name__ == "__main__":
    test_adb()
# test_performance.py
import subprocess
import time

def test_connection_speed(ip_address):
    """Testa velocidade da conexão WiFi"""
    print(f"🧪 Testando conexão com {ip_address}...")
    
    # Testa ping
    try:
        result = subprocess.run(['ping', '-n', '4', ip_address], 
                              capture_output=True, text=True, timeout=10)
        print(f"📶 Resultado ping:\n{result.stdout}")
    except:
        print("❌ Falha no teste de ping")

def test_scrcpy_performance():
    """Testa performance do scrcpy com diferentes configurações"""
    configs = [
        ['scrcpy', '--video-bit-rate', '2M', '--max-size', '800'],
        ['scrcpy', '--video-bit-rate', '4M', '--max-size', '960'],
        ['scrcpy', '--video-bit-rate', '6M', '--max-size', '1024'],
    ]
    
    for config in configs:
        print(f"\n🚀 Testando: {' '.join(config)}")
        try:
            start_time = time.time()
            process = subprocess.Popen(config, 
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL,
                                     shell=True)
            
            time.sleep(5)  # Testa por 5 segundos
            
            if process.poll() is None:
                print("✅ Estável")
                process.terminate()
            else:
                print("❌ Instável")
                
            print(f"⏱️  Tempo: {time.time() - start_time:.1f}s")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("📊 Teste de Performance")
    test_scrcpy_performance()
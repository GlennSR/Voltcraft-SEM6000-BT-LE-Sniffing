import subprocess

def capturar_pacotes(interface=10, duracao=10):
    try:
        comando = ["tshark", "-i", str(interface), "-a", f"duration:{duracao}"]
        print(f"Executando: {' '.join(comando)}\n")

        processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for linha in processo.stdout:
            print(linha.strip())

        processo.wait()
        print("\nCaptura finalizada.")

    except FileNotFoundError:
        print("Erro: o tshark não está instalado ou não está no PATH.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    capturar_pacotes()

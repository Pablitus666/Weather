from ui.app_window import WeatherApp
from utils.logger import logger

def main():
    try:
        logger.info("Iniciando aplicación Weather Report...")
        app = WeatherApp()
        app.mainloop()
        logger.info("Aplicación cerrada correctamente.")
    except Exception as e:
        logger.critical(f"Fallo catastrófico al iniciar la aplicación: {e}", exc_info=True)

if __name__ == "__main__":
    main()

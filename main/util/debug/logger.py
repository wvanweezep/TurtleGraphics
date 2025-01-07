class Logger:
    @staticmethod
    def log(origin: str, msg: str, error: bool = False, warning: bool = False) -> None:
        print(f"[{origin}] -{"\033[31m" if error else ""}"
              f"{"\033[33m" if warning else ""} {msg}\033[0m")
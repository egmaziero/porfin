import logging


class Logger:
    def __init__(self, name, level=logging.INFO):
        """
        Inicializa o logger com o nome especificado, arquivo de log e nível de log.

        Args:
            name (str): Nome do logger.
            level (int): Nível de log.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Formatação do log
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_logger(self):
        """
        Retorna o logger configurado.

        Returns:
            logging.Logger: Logger configurado.
        """
        return self.logger

import logging
from enum import Enum

"""
Classe criada para facilitar a escrita de logs em arquivos .log
Classe utiliza o tipo ENUM para definir o tipo de log que sera escrito no arquivo .log
Classe utiliza o padrão de projeto Singleton para garantir que apenas uma instancia do log seja criada.

Criada por: Pedro Motta - Desenvolvedor da Bluetape
Todos os direitos reservados a Bluetape.

"""


class LogLevel(Enum):
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._log = logging.getLogger(__name__)
            self.initialized = True

    def criarLogPrint(self, frase, tipo: LogLevel, classe='Null'):

        """
        Metodo que cria um print e escreve esse print dentro do log, para facilitar a lida em codigos que rodam sozinhos
        e necessitam de manutencao de vez em quando. Basta apenas abrir o arquivo .log e tera as informaoes sobre a execucao
        do programa de forma detalhada.

        :param classe: nome da classe.
        :param frase: e a frase que ira ser escrita no terminal e tambem no arquivo .log
        :param tipo: esse parametro e utilizado para que ao ler o log da execucao, possamos identificar facilmente a informacao descrita. Os tipos de log sao: 'debug', 'info', 'warning', 'error' e 'critical'.
        """

        print(frase)

        frase = f'Classe: {classe} - {frase}'

        if tipo == LogLevel.INFO:
            self._log.info(frase)
        elif tipo == LogLevel.DEBUG:
            self._log.debug(frase)
        elif tipo == LogLevel.WARNING:
            self._log.warning(frase)
        elif tipo == LogLevel.ERROR:
            self._log.error(frase)
            raise Exception(frase)
        elif tipo == LogLevel.CRITICAL:
            self._log.critical(frase)
            raise Exception(frase)
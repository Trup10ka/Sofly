from src.config.pyhocon_config_loader import PyhoconConfigLoader
from src.sofly_server import SoflyServer

def main():

    config = PyhoconConfigLoader("config.conf").load_config()

    server = (SoflyServer.builder()
              .set_host(config.server.host)
              .set_port(config.server.port)
              .build())

    if server is None:
        raise RuntimeError("SoflyServer not initialized, fatal error, exiting...")

    server.init()
    server.run()

if __name__ == '__main__':
    main()
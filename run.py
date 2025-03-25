from src.sofly_server import SoflyServer

if __name__ == '__main__':
    server = (SoflyServer.builder()
              .set_host('0.0.0.0')
              .set_port(5525)
              .build())

    if server is None:
        raise RuntimeError("SoflyServer not initialized, fatal error, exiting...")

    server.init()
    server.run()
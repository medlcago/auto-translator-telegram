if __name__ == '__main__':
    from handlers import client
    import logging

    logging.basicConfig(level=logging.INFO)

    client.run_until_disconnected()

import logging
import msgpack
import socket
import ssl
import threading

import message


class Transport(object):
    def __init__(self, logger=None):
        """
        :param logging.Logger logger:
        """
        self.logger = logger or logging.getLogger(__name__)

    def connected(self):
        """
        List of connected neighbours
        :rtype: list|str[]
        """
        raise NotImplementedError()

    def is_connected(self, recipient):
        """
        :param str recipient:
        :rtype: bool
        """
        raise NotImplementedError()

    def publish(self, node, msg):
        """
        :param pyraftlog.node.Node node:
        :param pyraftlog.message.Message msg:
        """

    def handle_exception(self, recipient, error):
        """
        :param str recipient:
        :param Error error:
        :return:
        """
        pass

    def subscribe(self, node):
        """
        :param pyraftlog.node.Node node:
        """
        raise NotImplementedError()

    def shutdown(self):
        raise NotImplementedError()


class InMemoryTransport(Transport):
    """
    The In Memory transport is for testing purposes and all nodes should created in the same process.
    """
    def __init__(self, logger=None):
        super(InMemoryTransport, self).__init__(logger)
        self.nodes = {}

    def connected(self):
        return self.nodes.keys()

    def is_connected(self, recipient):
        """
        :param str recipient:
        :rtype: bool
        """
        return recipient in self.nodes

    def publish(self, node, msg):
        """
        :param pyraftlog.node.Node node:
        :param pyraftlog.message.Message msg:
        """
        if self.is_connected(msg.recipient):
            while msg is not None:
                # "Send" the message and get the response
                response = self.nodes[msg.recipient].on_message(msg)

                # Handle the received response
                msg = node.on_message(response)

    def subscribe(self, node):
        """
        :param pyraftlog.node.Node node:
        """
        self.nodes[node.name] = node

    def shutdown(self):
        pass


class SocketTransport(Transport):
    def __init__(self, port, response_timeout=100, logger=None):
        super(SocketTransport, self).__init__(logger)

        self.sub_sock = None
        self.connections = {}
        self.node = None
        self.port = port
        self.response_timeout = response_timeout

    def connected(self):
        return self.connections.keys()

    def is_connected(self, recipient):
        return recipient in self.connections

    def shutdown(self):
        if self.sub_sock:
            self.sub_sock.close()

        for sock in self.connections.values():
            sock.close()

    def _socket(self, server_hostname=None):
        """ Get an instance of socket. """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def _set_socket_options(sock):
        """ Set socket options. """
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.SO_KEEPALIVE, 3)
        sock.settimeout(None)

    def _socket_send(self, sock, msg):
        """
        Send a message to another node. We first send the message length, then the message itself.
        :param socket.socket sock: Socket to send the data through
        :param message.Message msg: Message to be sent
        :return:
        """
        try:
            sock.settimeout(self.response_timeout)
            sock.sendall(msgpack.dumps(msg.__dict__))

        except Exception as e:
            self.logger.error('Failed to send message: %s' % str(e))
        finally:
            sock.settimeout(None)

    def _socket_receive(self, sock):
        """
        Receive a message from another node. We first expect the message length, then the message itself.
        :param socket.socket sock:
        :rtype: message.Message
        """
        try:
            unpacker = msgpack.Unpacker(raw=False)
            sock.settimeout(self.response_timeout)
            while True:
                buf = sock.recv(1024**2)
                if not buf:
                    break
                unpacker.feed(buf)
                try:
                    return message.Message(**unpacker.unpack())
                except Exception as e:
                    self.logger.error('Failed receiving message: %s' % str(e))
        finally:
            sock.settimeout(None)

    def _socket_connect(self, recipient):
        """
        :param str recipient:
        """
        if recipient in self.connections:
            return self.connections[recipient]

        host, port = recipient.split(':')
        sock = self._socket(host)
        self._set_socket_options(sock)
        sock.connect((host, int(port)))
        self.node.log(logging.INFO, "Established connection to %s" % recipient)

        self.connections[recipient] = sock

        return sock

    def handle_exception(self, recipient, error):
        if isinstance(error, socket.error) and error.errno not in (-2, 111):
            self.node.log(logging.WARN, "Connection with %s marked as dead: %d" % (recipient, error.errno))

        # Mark the connection as dead
        if recipient in self.connections:
            self.connections[recipient].close()
        if recipient in self.connections:
            del self.connections[recipient]

        super(SocketTransport, self).handle_exception(recipient, error)

    def publish(self, node, msg):
        """
        :param pyraftlog.node.Node node:
        :param pyraftlog.message.Message msg:
        """
        if not self.node:
            self.node = node
        # Get the connection to the message recipient
        sock = self._socket_connect(msg.recipient)

        # Have a conversation
        while msg is not None:
            # Send the given message
            self._socket_send(sock, msg)

            # Wait for a response
            response = self._socket_receive(sock)
            msg = node.on_message(response)

    def subscribe(self, node):
        """
        :param pyraftlog.node.Node node:
        """
        if not self.node:
            self.node = node
        self.sub_sock = None
        try:
            self.sub_sock = self._socket()
            self.sub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.sub_sock.bind(('0.0.0.0', int(self.port)))
            self.sub_sock.listen(len(node.neighbours))
            while node.active:
                try:
                    client_sock, address = self.sub_sock.accept()
                    self.connections[address] = client_sock
                    self._set_socket_options(client_sock)
                    self.node.log(logging.INFO, "Accepted connection with %s:%d" % (address[0], address[1]))

                    # Move the conversation to a daemon thread
                    thread = threading.Thread(target=self._subscribe_converse, args=[node, client_sock, address])
                    thread.daemon = True
                    thread.start()

                except Exception as e:
                    self.node.log(logging.CRITICAL, "Subscribe Error: %s" % str(e))
                    pass
        except ValueError as e:
            self.node.log(logging.CRITICAL, "Subscribe Value Error: %s" % str(e))
            return
        finally:
            self.node.log(logging.DEBUG, "Unsubscribed")
            if self.sub_sock:
                self.sub_sock.close()

    def _subscribe_converse(self, node, client_sock, address):
        """
        Given a open connection `client_sock` receive messages and send appropriate responses.
        :param socket.socket client_sock:
        :param str address:
        """
        neighbour = None
        try:
            while node.active:
                msg = self._socket_receive(client_sock)
                if not msg:
                    break
                neighbour = msg.sender
                self.connections[neighbour] = client_sock
                response = node.on_message(msg)
                if not response:
                    break

                self._socket_send(client_sock, response)
        except Exception as e:
            self.node.log(logging.CRITICAL, "Subscribe Converse Error: %s" % str(e))
        finally:
            self.connections.pop(address)
            if neighbour and neighbour in self.connections:
                self.connections.pop(neighbour)
            client_sock.close()


class SslSocketTransport(SocketTransport):
    CIPHERS = 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH'

    def __init__(self, port, key_file, crt_file, ca_crt, ciphers=None, response_timeout=100, logger=None):
        super(SslSocketTransport, self).__init__(port, response_timeout, logger)

        self.ciphers = ciphers or SslSocketTransport.CIPHERS
        self.key_file = key_file
        self.crt_file = crt_file
        self.ca_crt = ca_crt

    def _socket(self, server_hostname=None):
        sock = super(SslSocketTransport, self)._socket()
        if server_hostname:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.ca_crt)
        else:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=self.ca_crt)

        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        context.load_cert_chain(self.crt_file, self.key_file)
        context.verify_mode = ssl.CERT_REQUIRED

        if self.ciphers:
            context.set_ciphers(self.ciphers)

        if server_hostname:
            context.check_hostname = True
            sock = context.wrap_socket(sock, server_side=False, server_hostname=server_hostname)
        else:
            sock = context.wrap_socket(sock, server_side=True)

        return sock

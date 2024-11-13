import socket
from datetime import datetime
import threading

class HTTPServer:

    def __init__(self, host='127.0.0.1', port=8000):
        self.host = host
        self.port = port

        # Server socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Allows reusing the address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))


    def start(self):
        """ Starts the HTTP Server """
        try:
            self.server_socket.listen(5)
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                # Accept incoming connections
                client_socket, client_address = self.server_socket.accept()
                print(f"New connection from {client_address}")

                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\nShutting down server...")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server_socket.close()
    

    def handle_client(self, client_socket, client_address):
        """Handle individual client connections"""
        try:
            request_data = client_socket.recv(1024).decode('utf-8')
            print(f"\nReceived request from {client_address}:")
            print(request_data)

            # Parse the request (method, path, HTTP version)
            request_line = request_data.split('\n')[0]
            method, path, protocol = request_line.split(' ')

            # Create a basic response
            response_content = f"""
            <html>
                <head>
                    <title>Python HTTP Server</title>
                </head>
                <body>
                    <h1>Hello from your custom HTTP server!</h1>
                    <p>You requested: {path}</p>
                    <p>Using method: {method}</p>
                </body>
            </html>
            """
            
            # Construct HTTP response
            response_headers = [
                'HTTP/1.1 200 OK',
                'Content-Type: text/html; charset=utf-8',
                f'Content-Length: {len(response_content)}',
                f'Date: {datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}',
                'Server: Python Custom Server',
                'Connection: close'
            ]
            
            response = '\r\n'.join(response_headers) + '\r\n\r\n' + response_content
            
            # Send the response
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = HTTPServer()
    server.start()
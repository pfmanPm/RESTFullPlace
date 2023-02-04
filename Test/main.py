# Main entry point of Test Server for the RESTFull Place

from http.server import HTTPServer
from Test.TestHttpServer import RESTFullServer

hostName = "localhost"
serverPort = 8080

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    theRESTFullServer = HTTPServer((hostName, serverPort), RESTFullServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        theRESTFullServer.serve_forever()
    except KeyboardInterrupt:
        pass

    theRESTFullServer.server_close()
    print("Server stopped.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

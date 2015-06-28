
from server import start_server
import datastore
import chart

WEB_PORT = 8880
TCP_PORT = 8888
PATH_GRAPH = "graph/graph.svg"

def on_data(data):
    print(data)
    datastore.on_data(data)

def main():
    #datastore.do_test()
    chart.update_chart(PATH_GRAPH)
    start_server(WEB_PORT, TCP_PORT, on_data)

if __name__ == "__main__":
    main()

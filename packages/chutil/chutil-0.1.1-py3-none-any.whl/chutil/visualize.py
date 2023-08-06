import pydot
from IPython.display import Image, display


def display_graph(out_dir: str = "./out/") -> None:
    graph = pydot.graph_from_dot_file(out_dir + "cg.dot")  # load from .dot file
    graph[0].write_png("graph.png")
    display(Image("graph.png", width=600, height=600))


def plot_loss_and_accuracy(out_dir: str = "./out/") -> None:
    display(Image(filename=out_dir + "loss.png"))
    display(Image(filename=out_dir + "out/accuracy.png"))

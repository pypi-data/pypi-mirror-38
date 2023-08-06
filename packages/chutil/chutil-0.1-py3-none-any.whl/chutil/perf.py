import chainer
from chainer import extensions
from typing import Any, Iterable


def print_test_performance(
    model: chainer.Chain, test: Iterable[Any], enable_cupy: bool, batchsize: int
) -> None:
    device = -1
    if enable_cupy:
        model.to_gpu()
        device = 0
    test_iter = chainer.iterators.SerialIterator(
        test, batchsize, repeat=False, shuffle=False
    )
    test_evaluator = extensions.Evaluator(test_iter, model, device=device)
    results = test_evaluator()
    print("Test accuracy:", results["main/accuracy"])

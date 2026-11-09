from .giraffe import render_giraffe
from .snowman import render_snowman
from .snake_train import render_snake_train
from .monkey_tree import render_monkey_tree
from .buffalo import render_buffalo

CREATURES = {
    "giraffe": render_giraffe,
    "snowman": render_snowman,
    "snake_train": render_snake_train,
    "monkey_tree": render_monkey_tree,
    "buffalo": render_buffalo,
}


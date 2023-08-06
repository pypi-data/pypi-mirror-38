# TensorBoard Embedding Visualizer

![DEMO](https://github.com/Backalla/tbev/blob/master/media/tbev.gif)

As the name suggests, this tool is made for visualizing high dimensional embeddings into 3D space using TensorBoard Projector tool. It performs PCA and also has an option for T-SNE for doing dimensionality reduction. All you have to do is provide you embeddings data and its corresponding labels and optionally images(paths) in pickle format as a dictionary. The structure of this dictionary is explained below. 

## Getting Started

#### Requirement
- Python3
- Tensorflow > 1.4

#### Install
Install this tool using pip with the following command.  
`pip install tbev`  
Upgrade to the latest version by using the `--upgrade` flag  
This will be installed as a command line tool and you can simply run `tbev` in you command line to get started.

#### Usage

```
Usage:
    tbev demo 
    tbev <pickle_file> [--logdir=<path>]

Options:
    -h --h    Show help screen
    --logdir=<path>  Location to store log files [default: ./logs/]
```
tbev <pickle_file> [--logdir=<path>]
You will need to pass your embeddings in form of a pickle file. The pickle file should contain a dictionary in the following format.
```
{
    "embedding":2D matrix of shape [m embeddings, n dimensions],
    "labels":{
        "label1": List of shape (m,), A label for each embedding,
        "label2": List of shape (m,), A label for each embedding,
        You can put as many labels as you want.
    },
    "sprite_paths":(Optional) List of shape (m,), A path to image to be shown in tensorboard.
}
```

Save this dictionary into a pickle file and use the command `tbev <pickle_file> [--logdir=<path>]`  
This will create a ./logs folder by default where it will store the checkpoints file. You can optionally mention your own name for storing the logs using the --logdir option. If everything works out well. It will start the tensorboard server for you. 

#### Tensorboard
After the Tensorboard is started, it will show you the local URL to view the tensorboard. By default it is `localhost:6006`.
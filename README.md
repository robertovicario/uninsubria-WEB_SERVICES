| <img src="docs/uninsubria.svg" width="128"> |
| - |

# Web Service & AI Interfaces, MSc Course @ uninsubria

This repository contains the seminar presented by me and the related demo project for the Web Service & AI Interfaces course at the University of Insubria, part of the MSc in Computer Science.

## Overview

You can easily download the presented seminar and its demo project below, remember to use it responsibly and cite it if you reference it.

## Prerequisites

> [!IMPORTANT]
>
> - Docker
> - Docker Compose

## Seminar

| <a href="https://raw.githubusercontent.com/robertovicario/uninsubria-WEB_SERVICES/main/dist/Project_Work.pdf"><img src="docs/seminar.png" alt="seminar" height="512"></a> |
| **Seminar: Microservice Architectures and Nanoservice Technologies** |

## Demo

| <a href="https://uninsubria-rvicario-webservices.onrender.com"><img src="docs/demo.png" alt="demo" height="512"></a> |
| **Demo** |

## Instructions

Usage:

```sh
bash cmd.sh {start|stop|setup|debug|clean}
```

### `setup`

If you haven't built the project yet, you can do so by running:

```sh
bash cmd.sh setup
```

Once the setup process is complete, the project will be accessible at `http://localhost/`.

### `debug`

During development, you will often need to recompile the frontend or backend code. The following command is a lightweight version of `setup`: it rebuilds only the essential project resources required to launch the application:

```sh
bash cmd.sh debug
```

### `stop`

To stop the program, simply run:

```sh
bash cmd.sh stop
```

> [!TIP]
> For a quicker way to stop, use `ctrl + C` to force stop the program.

### `start`

To start an already built version of the program, simply run:

```sh
bash cmd.sh start
```

### `clean`

If you need to clean all containers and their orphaned dependencies, you can run:

```sh
bash cmd.sh clean
```

## Credits

> [!WARNING]
>
> Please use this project responsibly, it was created by me for an exam session that I completed at _University of Insubria_. If you use or reference this project, please cite it as follows:
>
> ```bib
> @misc{vicario2026webservices,
>     author = {R. Vicario},
>     title  = {uninsubria-WEB_SERVICES},
>     year   = {2026},
>     url    = {https://github.com/robertovicario/uninsubria-WEB_SERVICES}
> }
> ```

## License

This project is distributed under [GNU General Public License version 3](https://opensource.org/license/gpl-3-0). You can find the complete text of the license in the project repository.

# dirtreegen
Generate directory tree easily.

## Getting Started
### Prerequisites

Install the package by pip

```
pip3 install dirtreegen
```

### How to use
Open interactive command line tool **ipython**, before do that, make sure you have installed the **dirtreegen** package

```
cd yourproject
```
```
ipython3
In [1]: from dirtreegen import treegen
In [2]: treegen()
IN [3]:
.
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.cfg
├── setup.py
└── dirtreegen
    ├── __init__.py
    └── dirtreegen.py
```

Of course, if you don’t want to show some files or directory, you can create a list which include you don’t want to show.

```
IN [4]: treegen([‘.gitignore’, ‘dirtreegen’])
IN [5]:
.
├── LICENSE
├── README.md
├── requirements.txt
├── setup.cfg
└── setup.py
```



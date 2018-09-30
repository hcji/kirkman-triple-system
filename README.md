# Implementation of Kirkman Triple System

Mr. Kirkman posed the following problem

> Fifteen young ladies in a school walk out three abreast for seven days in
succession: it is required to arrange them daily, so that no two will walk
twice abreast. 

This project implements solution described in article [A survey of Kirkman triple systems and related designs](https://www.sciencedirect.com/science/article/pii/0012365X9190294C)

### Usage

```
python3 main.py <order>
```

where `<order>` is order of the solution, e.g. "number of schoolgirls". Regarding the article, the solution is possible only when `order `mod` 6 == 3`.

### Note
The project was created as homework within lessons of Simulation Tools and Techniques at Faculty of Information Technology, Brno University of Technology, 2015.

The project uses library `numbthy`, which is attached in the repository.

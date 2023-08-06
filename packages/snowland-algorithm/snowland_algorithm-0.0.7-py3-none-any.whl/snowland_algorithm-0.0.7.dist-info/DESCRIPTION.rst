=====
slapy
=====
1. install
from pypi:
    pip install snowland-algorithm
or
from source code:
    download code from https://gitee.com/hoops/snowland-algorithm-python, you can choose a release version
    pip install -r requirements.txt
    python setup.py install
#. dirs
    1. graph
        a. dijkstra(v0.0.1+)
        #. spfa(v0.0.1+)
    #. swarm
        a. pso(v0.0.1+)
        #. gso(v0.0.2+)
        #. fa(v0.0.3+)
        #. cso(v0.0.6+)
        #. ba(v0.0.6+)
        #. sfla(v0.0.6+)
        #. bas(v0.0.6+)
        #. sa(v0.0.6+)
        #. fwa(v0.0.6+)
        #. cs(v0.0.7+)
        #. bfo(v0.0.7+)
#. quick use
    1. import package
    >>> from slapy.swarm.package_name import engine_name
    2. define the fitness function
    example:
        >>> fun = lambda x: np.cos(x[0]) + np.sin(x[0]) - x[0] * x[1]
    note: arg need to be 1 X n vector
    3. run the model
    >>> engine = engine_name(your_args)
    >>> engine.run()
    4. show result
    >>> x, y = engine.gbest.chromosome
    >>> print('max value', fun(engine.gbest.chromosome))
    >>> print('x:', x, 'y:', y)
    There is a example for PSO.
        >>> def fun(vars):
        >>>     # fitness function
        >>>     x, y = vars
        >>>     if 1 <= x <= 2 * np.pi and 1 <= y <= np.pi:
        >>>         return np.cos(x) + np.sin(x) - x * y
        >>>     else:
        >>>         return -2 - 4 * np.pi ** 2  # return a small float number can not reach

        >>> if __name__ == '__main__':
        >>>    engine = PSOEngine(vmax=0.01, bound=[[1, 2 * np.pi]], min_fitness_value=-1, dim=2, fitness_function=fun, steps=100)
        >>>    engine.run()
        >>>    x, y = engine.gbest.chromosome
        >>>    print('max value', fun(engine.gbest.chromosome))
        >>>    print('x:', x, 'y:', y)





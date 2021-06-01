from invoke import task


# deleting the generated .so file
@task(aliases=['del'])
def delete(c):
    c.run("rm *mykmeanssp*.so")
    print("Deleted")


@task
def run(c, k=-1, n=-1, Random=True):
    # maximum capacity that our program can process
    maxCapK2 = 16
    maxCapN2 = 420
    maxCapK3 = 16
    maxCapN3 = 400

    # building the extension
    c.run("python3.8.5 setup.py build_ext --inplace")

    # informative message to the user about the capacities
    print("The max capacity for d=2 is k=" + str(maxCapK2) + ", n=" + str(maxCapN2))
    print("The max capacity for d=3 is k=" + str(maxCapK3) + ", n=" + str(maxCapN3))

    # executing the main program
    if Random:
        c.run("python3.8.5 main.py " + str(k) + " " + str(n))
    else:
        c.run("python3.8.5 main.py " + str(k) + " " + str(n) + " --no-Random")

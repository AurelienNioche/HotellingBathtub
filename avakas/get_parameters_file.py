import os


def get_parameters_file(i):

    parameters_files = sorted(
        [os.path.join("tasks", f)
         for f in os.listdir("tasks") if os.path.isfile(os.path.join("tasks", f))])

    return parameters_files[i]

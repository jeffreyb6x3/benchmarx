class Requests:
    def __init__(self, parameters):
        self.parameters = {}

        if parameters:
            try:
                for parameter in parameters:
                    key, value = parameter.split("=", 1)
                    try:
                        corrected_value = int(value)
                    except ValueError:
                        try:
                            corrected_value = float(value)
                        except ValueError:
                            corrected_value = value
                    self.parameters[key] = corrected_value
            except ValueError:
                raise ValueError("Parameters must be in key=value format")


parameters = ["a=1", "b=soup"]
classy = Requests(parameters)

print(classy.parameters)

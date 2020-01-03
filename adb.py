from enum import IntEnum

class AkashaDB:
    def __init__(self):
        self.running = True
        self.data = dict()
        self.status = IntEnum("Status", [
            "success",
            "invalid"
        ])

    def _read(self):
        raw = input("> ")
        return raw.strip()
        
    def _eval(self, line):
        if line.startswith("."):
            return self._meta_exec(line)

        return self._exec(line)

    def _print(self, result):
        status, message =result 
        if status != self.status.success:
            return f"ERROR: {message}"

        return message

    def _meta_exec(self, instruction):
        command, *parameters = instruction.split(" ")

        if command == ".exit":
            self.running = False

        else:
            return self.status.invalid, f"command '{command}' is invalid"

        return self.status.success, instruction

    def _exec(self, instruction):
        keyword, *parameters = instruction.split(" ")
        keyword = keyword.lower()
        if keyword == "insert":
            if len(parameters) < 2:
                message = f"'insert' needs at least two parameters"
                return self.status.invalid, message

            key, *value = parameters
            data_value = self.data.get(key)
            if data_value is not None:
                message = f"'{key}' already exists"
                return self.status.invalid, message

            self.data[key] = value

            message = f"insert '{repr(value)}' into '{key}'"
            return self.status.success, message

        elif keyword == "delete":
            if len(parameters) < 1:
                message = f"'delete' needs at least one parameter"
                return self.status.invalid, message

            for key in parameters:
                self.data.pop(key, None)

            keys = ", ".join(parameters)
            message = f"deleted '{keys}'"
            return self.status.success, message

        elif keyword == "select":
            if len(parameters) < 1:
                message = f"'select' needs at least one parameter"
                return self.status.invalid, message

            result = dict()
            for key in parameters:
                result[key] = self.data.get(key)

            message = f"selected: {repr(result)}"
            return self.status.success, message

        else:
            return self.status.invalid, f"keyword '{keyword}' is invalid"

    def repl(self):
        while self.running:
            output = self._print(self._eval(self._read()))
            if output is None:
                self.running = False
                break

            if len(output) == 0:
                continue

            print(output)

if __name__ == "__main__":
    adb = AkashaDB()
    adb.repl()

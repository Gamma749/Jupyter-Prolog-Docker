from pyswip import Prolog
from pyswip import Functor
from pyswip.prolog import PrologError
from pathlib import Path
import re

DEFAULT_LIMIT = 10

def format_value(value):
    output = ""
    if isinstance(value, list):
        output = "[ " + ", ".join([format_value(val) for val in value]) + " ]"
    elif isinstance(value, Functor) and value.arity == 2:
        output = "{0}{1}{2}".format(value.args[0], value.name, value.args[1])
    else:
        output = "{}".format(value)

    return output

def format_result(result):
    result = list(result)

    if len(result) == 0:
        return "false."

    if len(result) == 1 and len(result[0]) == 0:
        return "true."

    output = ""
    for res in result:
        tmpOutput = []
        for var in res:
            tmpOutput.append(var + " = " + format_value(res[var]))
        output += ", ".join(tmpOutput) + " ;\n"
    output = output[:-3] + " ."

    return output

def run(code):
    prolog = Prolog()

    output = []
    ok = True
    tmp = ""
    clauses = []
    isQuery = False
    cell_files_dir = Path(Path.cwd(), "consulted_cells")
    cell_files_dir.mkdir(mode=755, exist_ok=True)
    cell_file_name = "cell.pl"
    for line in code.split("\n"):
        line = line.strip()
        match = re.fullmatch(r"%\s*[Ff]ile:\s*(\w+.*)", line)
        if match is not None:
            cell_file_name = match.group(1)
            if not cell_file_name.endswith(".pl"):
                cell_file_name += ".pl"
        if line == "" or line[0] == "%":
            continue
        if line[:2] == "?-":
            isQuery = True
            line = line[2:]
            tmp += " " + line
        else:
            clauses.append(line)

        if isQuery and tmp[-1] == ".":
            # End of statement
            tmp = tmp[:-1] # Removes "."
            maxresults = DEFAULT_LIMIT
            # Checks for maxresults
            if tmp[-1] == "}":
                tmp = tmp[:-1] # Removes "}"
                limitStart = tmp.rfind('{')
                if limitStart == -1:
                    ok = False
                    output.append("ERROR: Found '}' before '.' but opening '{' is missing!")
                else:
                    limit = tmp[limitStart+1:]
                    try:
                        maxresults = int(limit)
                    except:
                        ok = False
                        output.append("ERROR: Invalid limit {" + limit + "}!")
                    tmp = tmp[:limitStart]

            try:
                if isQuery:
                    result = prolog.query(tmp, maxresult=maxresults)
                    output.append(format_result(result))
                    result.close()

            except PrologError as error:
                ok = False
                output.append("ERROR: {}".format(error))
            tmp = ""
            isQuery = False
    if len(clauses) > 0:
        try:
            #f = open("foo.pl", 'w+')
            f = open(Path(cell_files_dir, cell_file_name), 'w+')
            f.write('\n'.join(clauses))
        finally:
            f.close()
            prolog.consult(f.name)
    return output, ok

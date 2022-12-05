from rich import print


class MiniTroll:
    def __init__(self, kb_file) -> None:

        self.arths = {"eq": self.eq, "gt": self.gt, "lt": self.lt}
        self.logops = {"or": self.OR, "and": self.AND}

        self.kb_file = open(kb_file, "r").readlines()
        self.kb_file = "".join(self.kb_file)

        self.keys, self.hints = self.parse_keys()
        self.rules = self.parse_rules()

        self.inference()

    def parse_keys(self):
        kb_file = self.kb_file.split("]\n")
        keys = kb_file[0].strip().split("keys[\n")[1].replace(",", "").splitlines()
        keys_dict = {}
        hints = {}
        for i, key in enumerate(keys):
            kk = key.split("(")[0].strip()
            keys_dict[kk] = kk
            if "/" in key.split("(")[1].strip():
                hints[kk] = key.split("(")[1].strip().replace(")", "").split("/")
            else:
                hintt = key.split("(")[1].strip().replace(")", "")
                hints[kk] = f"({hintt})"
        return keys_dict, hints

    def parse_rules(self):
        kb_file = self.kb_file.split("]\n")
        rules = (
            kb_file[1]
            .strip()
            .split("rules[\n")[1]
            .replace(",", "")
            .replace("]", "")
            .splitlines()
        )
        return rules

    def parse_rule(self, rule_text):
        condition = rule_text.split("if")[1].strip().split("then")[0].strip()
        result = rule_text.split("then")[1].strip()
        res = self.eval_rule(condition)
        return {result: res}

    def eval_rule(self, condition):
        if " or " not in condition and " and " in condition:
            con = condition.split(" and ")
            for i, c in enumerate(con):
                if "&" in c or "|" in c:
                    con[i] = self.eval_logsym(c)
            return self.eval_logop(con, "and")
        elif " or " in condition and " and " not in condition:
            con = condition.split(" or ")
            for i, c in enumerate(con):
                if "&" in c or "|" in c:
                    con[i] = self.eval_logsym(c)
            return self.eval_logop(con, "or")
        elif " or " not in condition and " and " not in condition:
            return self.eval_arth(condition.format(**self.runtime_vars))

    def eval_logsym(self, con):
        if "&" in con:
            con = con.replace("&", " and ")
        elif "|" in con:
            con = con.replace("|", " or ")
        res = self.eval_rule(con)
        if res == True:
            return "{_filler}=true"
        elif res == False:
            return "{_filler}=false"

    def eval_logop(self, condition, logop):
        result = []
        for i, con in enumerate(condition):
            if (
                " eq " in condition[i]
                or " gt " in condition[i]
                or " lt " in condition[i]
            ):
                result.append(self.eval_arth(con.format(**self.runtime_vars)))
            elif "=" in condition[i] or ">" in condition[i] or "<" in condition[i]:
                condition[i] = (
                    condition[i]
                    .replace(">", " gt ")
                    .replace("<", " lt ")
                    .replace("=", " eq ")
                )
                result.append(self.eval_arth(condition[i].format(**self.runtime_vars)))
            elif "&" in condition[i] or "|" in condition[i]:
                condition[i] = condition[i].replace("&", " and ").replace("|", " or ")
                if "and" in condition[i]:
                    result.append(
                        self.eval_logop(condition[i].format(**self.runtime_vars), "and")
                    )
                elif "or" in condition[i]:
                    result.append(
                        self.eval_logop(condition[i].format(**self.runtime_vars), "or")
                    )
        print(logop, result)
        if logop == "or":
            for i in result:
                print(type(i))
        return self.logops[logop](result)

    def eval_arth(self, con):
        lhs, op, rhs = con.split()
        if self.is_number(lhs) and self.is_number(rhs):
            lhs = float(lhs)
            rhs = float(rhs)
        elif self.is_bool(rhs):
            lhs = self.str_to_bool(lhs)
            rhs = self.str_to_bool(rhs)
        return self.arths[op](lhs, rhs)

    def eq(self, lhs, rhs):
        return lhs == rhs

    def gt(self, lhs, rhs):
        return lhs > rhs

    def lt(self, lhs, rhs):
        return lhs < rhs

    def OR(self, to_or):
        return any(to_or)

    def AND(self, to_and):
        return all(to_and)

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_bool(self, s):
        if s == "true" or s == "false" or s == "True" or s == "False":
            return True
        else:
            return False

    def str_to_bool(self, s):
        if s == "true" or s == "True":
            return True
        elif s == "false" or s == "False":
            return False

    def inference(self):
        self.runtime_vars = {"_filler": True}
        for i, key in self.keys.items():
            usr_in = input(f"{key} {self.hints[i]}: ")
            if usr_in not in self.hints[i]:
                if self.hints[i] == "(any)":
                    pass
                elif self.hints[i] == "(number)":
                    while not self.is_number(usr_in):
                        if not self.is_number(usr_in):
                            print("[bold red]Please enter a valid number")
                        usr_in = input(f"{key} {self.hints[i]}: ")
                elif self.hints[i] == "(bool)":
                    while not self.is_bool(usr_in):
                        if not self.is_bool(usr_in):
                            print("[bold red]Please enter a boolean value (true/false)")
                        usr_in = input(f"{key} {self.hints[i]}: ")
                else:
                    while usr_in not in self.hints[i]:
                        print(f"[bold red]Please enter one of {self.hints[i]}")
                        usr_in = input(f"{key} {self.hints[i]}: ")
                self.runtime_vars[i] = usr_in
            elif usr_in in self.hints[i]:
                self.runtime_vars[i] = usr_in

        results = []
        for i, rule in enumerate(self.rules):
            res = self.parse_rule(rule)
            res_key = list(res.keys())[0]
            res_val = list(res.values())[0]
            self.runtime_vars[res_key] = res_val
            results.append(res)
        print("==================|RESULTS|=======================")

        for i in results:
            print(i)


es = MiniTroll("kb.trollscript")

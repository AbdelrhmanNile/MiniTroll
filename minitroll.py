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
            return self.eval_logop(con, "and")
        elif " or " in condition and " and " not in condition:
            con = condition.split(" or ")
            return self.eval_logop(con, "or")
        elif " or " not in condition and " and " not in condition:
            return self.eval_arth(condition.format(**self.runtime_vars))

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
        return self.logops[logop](*result)

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

    def OR(*args):
        return any(args)

    def AND(*args):
        return all(args)

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
        self.runtime_vars = {}
        for i, key in self.keys.items():
            usr_in = input(f"{key} {self.hints[i]}: ")
            if usr_in not in self.hints[i]:
                if self.hints[i] == "(any)":
                    self.runtime_vars[i] = usr_in
                elif self.hints[i] == "(number)":
                    print("Please enter a number")
                    if self.is_number(usr_in):
                        self.runtime_vars[i] = float(usr_in)
                    else:
                        print("Please enter valid a number")
                        return
                elif self.hints[i] == "(bool)":
                    if self.is_bool(usr_in):
                        self.runtime_vars[i] = self.str_to_bool(usr_in)
            elif usr_in in self.hints[i]:
                self.runtime_vars[i] = usr_in
        results = []
        for i, rule in enumerate(self.rules):
            res = self.parse_rule(rule)
            res_key = list(res.keys())[0]
            res_val = list(res.values())[0]
            self.runtime_vars[res_key] = res_val
            results.append(res)
        print("=========================================")

        for i in results:
            print(i)


es = MiniTroll("kb.trollscript")

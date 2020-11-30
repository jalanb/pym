class Grammar(OMeta):
    def rule_opt(self):
        _locals = {"self": self}
        self.locals["opt"] = _locals

        def _G__or_19():
            def _G_listpattern_3():
                self.exactly("Apply")
                _locals["ruleName"] = self.apply(
                    "anything",
                )
                _locals["ruleName"]
                _locals["codeName"] = self.apply(
                    "anything",
                )
                _locals["codeName"]

                def _G_listpattern_2():
                    def _G_many_1():
                        return self.apply(
                            "anything",
                        )

                    _locals["exprs"] = self.many(_G_many_1)
                    return _locals["exprs"]

                return self.listpattern(_G_listpattern_2)

            self.listpattern(_G_listpattern_3)
            return eval(
                "self.builder.apply(ruleName, codeName, *exprs)", self.globals, _locals
            )

        def _G__or_20():
            def _G_listpattern_4():
                self.exactly("Exactly")
                _locals["expr"] = self.apply(
                    "anything",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_4)
            return eval("self.builder.exactly(expr)", self.globals, _locals)

        def _G__or_21():
            def _G_listpattern_5():
                self.exactly("Many")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_5)
            return eval("self.builder.many(expr)", self.globals, _locals)

        def _G__or_22():
            def _G_listpattern_6():
                self.exactly("Many1")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_6)
            return eval("self.builder.many1(expr)", self.globals, _locals)

        def _G__or_23():
            def _G_listpattern_7():
                self.exactly("Optional")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_7)
            return eval("self.builder.optional(expr)", self.globals, _locals)

        def _G__or_24():
            def _G_listpattern_9():
                self.exactly("Or")

                def _G_many_8():
                    return self.apply(
                        "opt",
                    )

                _locals["exprs"] = self.many(_G_many_8)
                return _locals["exprs"]

            self.listpattern(_G_listpattern_9)
            return eval("self.builder._or(exprs)", self.globals, _locals)

        def _G__or_25():
            def _G_listpattern_11():
                self.exactly("And")

                def _G_many_10():
                    return self.apply(
                        "opt",
                    )

                _locals["exprs"] = self.many(_G_many_10)
                return _locals["exprs"]

            self.listpattern(_G_listpattern_11)
            return eval("self.builder.sequence(exprs)", self.globals, _locals)

        def _G__or_26():
            def _G_listpattern_12():
                self.exactly("Not")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_12)
            return eval("self.builder._not(expr)", self.globals, _locals)

        def _G__or_27():
            def _G_listpattern_13():
                self.exactly("Lookahead")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_13)
            return eval("self.builder.lookahead(expr)", self.globals, _locals)

        def _G__or_28():
            def _G_listpattern_14():
                self.exactly("Bind")
                _locals["name"] = self.apply(
                    "anything",
                )
                _locals["name"]
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_14)
            return eval("self.builder.bind(expr, name)", self.globals, _locals)

        def _G__or_29():
            def _G_listpattern_15():
                self.exactly("Predicate")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_15)
            return eval("self.builder.pred(expr)", self.globals, _locals)

        def _G__or_30():
            def _G_listpattern_16():
                self.exactly("Action")
                _locals["expr"] = self.apply(
                    "opt",
                )
                return _locals["expr"]

            self.listpattern(_G_listpattern_16)
            return eval("self.builder.action(expr)", self.globals, _locals)

        def _G__or_31():
            def _G_listpattern_17():
                self.exactly("Python")
                _locals["name"] = self.apply(
                    "anything",
                )
                _locals["name"]
                _locals["code"] = self.apply(
                    "anything",
                )
                return _locals["code"]

            self.listpattern(_G_listpattern_17)
            return eval(
                "self.builder.compilePythonExpr(name, code)", self.globals, _locals
            )

        def _G__or_32():
            def _G_listpattern_18():
                self.exactly("List")
                _locals["exprs"] = self.apply(
                    "opt",
                )
                return _locals["exprs"]

            self.listpattern(_G_listpattern_18)
            return eval("self.builder.listpattern(exprs)", self.globals, _locals)

        return self._or(
            [
                _G__or_19,
                _G__or_20,
                _G__or_21,
                _G__or_22,
                _G__or_23,
                _G__or_24,
                _G__or_25,
                _G__or_26,
                _G__or_27,
                _G__or_28,
                _G__or_29,
                _G__or_30,
                _G__or_31,
                _G__or_32,
            ]
        )

    def rule_grammar(self):
        _locals = {"self": self}
        self.locals["grammar"] = _locals

        def _G_listpattern_35():
            self.exactly("Grammar")

            def _G_listpattern_34():
                def _G_many_33():
                    return self.apply(
                        "rulePair",
                    )

                _locals["rs"] = self.many(_G_many_33)
                return _locals["rs"]

            return self.listpattern(_G_listpattern_34)

        self.listpattern(_G_listpattern_35)
        return eval("self.builder.makeGrammar(rs)", self.globals, _locals)

    def rule_rulePair(self):
        _locals = {"self": self}
        self.locals["rulePair"] = _locals

        def _G_listpattern_36():
            _locals["name"] = self.apply(
                "anything",
            )
            _locals["name"]
            _locals["rule"] = self.apply(
                "opt",
            )
            return _locals["rule"]

        self.listpattern(_G_listpattern_36)
        return eval("(name, rule)", self.globals, _locals)

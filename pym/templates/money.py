from decimal import Decimal


class Money(Decimal):
    pass


class PriceRule(object):
    def __init__(self, oid, product, price):
        self.oid = oid
        self.product = product
        self.price = price


class PriceSet(list):
    pass


class Organization(object):
    def __init__(self, name):
        self.name = name
        self.price_rules = PriceSet()


######
# Imperative approach: simple, but inflexible


def render_org_prices__imperative(org):
    return (
        div[
            h1["Custom Prices For ", org.name],
            div[ul[(li[render_price(pr)] for pr in org.price_rules)]],
        ]
        if org.price_rules
        else h1["No Custom Prices For ", org.name]
    )


def render_price(pr):
    return span("price_rule", id=("rule", pr.oid))[
        pr.product, ": $%0.2f" % pr.price
    ]


customer1 = Organization(name="Smith and Sons")
customer1.price_rules.extend(
    [
        PriceRule(
            oid=i,
            product="Product %i" % i,
            price=Money(str("%0.2f" % (i * 1.5))),
        )
        for i in xrange(10)
    ]
)

Example(
    "Customer pricing printout, imperative",
    render_org_prices__imperative(customer1),
)

######
# Declarative approach: cleaner, modular and flexible
# Delegates as many choices as possible to visitors, with each visitor
# doing one thing only:

new_vmap = examples_vmap.copy()


class UIScreen(object):
    "Abstract declarations of ui screens"

    def __init__(self, title, content=None):
        self.title = title
        self.content = content


@new_vmap.register(UIScreen)
def visit_screen(screen, w):
    w.walk(
        HTML5Doc(
            body=body[h1[screen.title], div("content")[screen.content]],
            head=head[title[screen.title]],
        )
    )


@new_vmap.register(PriceSet)
def visit_priceset(pset, w):
    w.walk(ul[(li[pr] for pr in pset)])


@new_vmap.register(Money)
def visit_money(m, w):
    w.walk("$%0.2f" % m)


@new_vmap.register(PriceRule)
def visit_pricerule(pr, w):
    w.walk(span("price_rule", id=("rule", pr.oid))[pr.product, ": ", pr.price])


def render_org_prices__declarative(org):
    return UIScreen(
        title=("Custom Prices For ", org.name),
        content=(
            org.price_rules
            if org.price_rules
            else "No custom prices assigned."
        ),
    )


Example(
    "Customer pricing printout, declarative",
    render_org_prices__declarative(customer1),
    visitor_map=new_vmap,
)

################################################################################
if __name__ == "__main__":
    for example in Example.all_examples:
        example.show()

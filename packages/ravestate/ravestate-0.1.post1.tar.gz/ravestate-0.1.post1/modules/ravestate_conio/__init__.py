
from ravestate import registry
from ravestate.state import state
from ravestate.receptor import receptor
import ravestate_rawio


@state(read="rawio:in")
def console_shutdown(ctx):
    rawin = ctx["rawio:in"]
    if "bye" in rawin:
        ctx.shutdown()


@state(triggers=":startup")
def console_input(ctx):

    @ctx.receptor(write="rawio:in")
    def write_console_input(*, ctx, value: str):
        ctx["rawio:in"] = value

    while not ctx.shutting_down():
        input_value = input("> ")
        write_console_input(value=input_value)


@state(read="rawio:out")
def console_output(ctx):
    print(ctx["rawio:out"])


registry.register(
    name="consoleio",
    states=(console_shutdown, console_input, console_output)
)

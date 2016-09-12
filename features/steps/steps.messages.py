from behave import *



SUCCESS_MESSAGE = '.gritter-success'
ERROR_MESSAGE = '.gritter-error'

@then("I expect a success message")
def step_impl(context):
    context.execute_steps(u"""then expect {selector}""".format(selector=SUCCESS_MESSAGE))
    context.execute_steps(u"""then don't expect {selector}""".format(selector=ERROR_MESSAGE))



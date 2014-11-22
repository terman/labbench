labbench
========

usage: <labbench tool="tname" src="URL" width="100%" height="300"/>

tname is used as a key to select the appropriate shared tool_state

URL referes to an HTML file to be loaded into the iframe used to
display the design tool.

The labbench XBlock provides persistent storage and grade reporting
for virtual labs running in their own iframe.  Persistent storage is
scoped by the current course.  There are two types of persistent storage:

1) problem_state -- student state associated with the current instance
of the labbench.

2) tool_state -- student state shared by all instances of labbench
with the same value for their "tool" attribute.  Useful for allowing
virtual labs to be cummulative, where a student can use their
designs from an earlier assignment (as stored in tool_state)
in later assignments.

This XBlock provides the following handlers:

get_problem_state()  [default value {}]
  returns JSON state for the current student and labbench instance.

put_problem_state(s)
  save the JSON state s as the current problem state

get_tool_state()     [default value {}]
  returns JSON state for the current student and tool specified
  by the "tool" attribute.

put_tool_state(s)
  save the JSON state s as the current tool state for the tool specified
  by the "tool" attribute.

publish({event_type: X, event: Y})
  publish an event of the specified type and event dictionary

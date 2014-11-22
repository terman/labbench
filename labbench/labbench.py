"TO-DO: Write a description of what this XBlock is."""

import pkg_resources,json

from xblock.core import XBlock
from xblock.fields import Scope, UserScope, BlockScope, String, Dict
from xblock.fragment import Fragment

class LabBenchXBlock(XBlock):
    """
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

    get_problem_state()  [default value ""]
      returns JSON state for the current student and labbench instance.

    put_problem_state(s)
      save the JSON state s as the current problem state

    get_tool_state()     [default value ""]
      returns JSON state for the current student and tool specified
      by the "tool" attribute.

    put_tool_state(s)
      save the JSON state s as the current tool state for the tool specified
      by the "tool" attribute.

    publish({event_type: X, event: Y})
      publish an event of the specified type and event dictionary
    """

    has_score = True         # lab benches are graded
    icon_class = 'problem'   # icon to use in the sequence header

    # attributes from the labbench tag
    src = String(default="", scope=Scope.content, help="URL for iframe content")
    tool = String(default="tool", scope=Scope.content, help="used as key for tool_state")
    width = String(default="100%", scope=Scope.content, help="width of enclosing iframe")
    height = String(default="300", scope=Scope.content, help="height of enclosing iframe")

    # two types of persistent storage
    problem_state = String(default="{}", scope=Scope.user_state,
                           help="student's JSON state for this problem")
    tool_state = Dict(default={}, scope=Scope(user=UserScope.ONE,block=BlockScope.TYPE),
                      help="student's JSON state for this tool")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # build what the user sees on the web page
    def student_view(self, context=None):
        """
        The primary view of the LabBenchXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/labbench.html")
        frag = Fragment(html.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/labbench.js"))
        frag.add_javascript(self.resource_string("static/js/src/jschannel.js"))
        frag.initialize_js('LabBenchXBlock')
        return frag

    @XBlock.json_handler
    def get_problem_state(self, data, suffix=''):
        """
        returns state string for the current student and labbench instance
        """
        return json.loads(self.problem_state);

    @XBlock.json_handler
    def put_problem_state(self, data, suffix=''):
        """
        save data as the current problem state
        """
        self.problem_state = json.dumps(data);
        return "okay"

    @XBlock.json_handler
    def get_tool_state(self, data, suffix=''):
        """
        returns state string for the current student and tool specified
        by the "tool" attribute.
        """
        return self.tool_state.get(self.tool,{})

    @XBlock.json_handler
    def put_tool_state(self, data, suffix=''):
        """
        save data as the current tool state for the tool specified
        by the "tool attribute.
        """
        self.tool_state[self.tool] = data
        return "okay"

    @XBlock.json_handler
    def publish(self, data, suffix=''):
        """
        publish an event of the specified type and event dictionary
        """
        self.publish(self,data.event_type,data.event)
        return "okay"

    # scenarios for XBlock SDK
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("LabBenchXBlock",
             """<vertical_demo>
                <labbench tool="jade" src="/resource/labbench/public/test.html"/>
                <labbench tool="jade" src="/resource/labbench/public/test.html"/>
                </vertical_demo>
             """),
        ]

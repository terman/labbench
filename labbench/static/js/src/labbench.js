// Javascript for LabBenchXBlock
// uses jquery.js and jschannel.js
function LabBenchXBlock(runtime, element) {
    // establish a communication channel with iframe and set up
    // functions to handle XBlock handler requests.
    $('iframe',element).each(function (index,iframe) {
        // establish communication with content in iframe
        var chan = Channel.build({window: iframe.contentWindow,
                                  origin: "*",
                                  scope: "labbench"
                                 });

        // these are the labbench handlers we want to access
        var handlers = ['get_problem_state',
                        'put_problem_state',
                        'get_tool_state',
                        'put_tool_state'];

        // set up a function for each labbench handler that
        // communicates with edX server, passing along parameters
        // and returning results
        $.each(handlers,function (index,handler) {
            var url = runtime.handlerUrl(element, handler);
            chan.bind(handler,function(trans,params) {
                $.ajax({
                    type: "POST",
                    url: url,
                    data: JSON.stringify(params || ''),
                    success: function(result) {
                        // return result to caller in iframe
                        trans.complete(result);
                    }
                });
                // we'll be returning value when ajax call completes
                trans.delayReturn(true);
            });
        });
    });
}

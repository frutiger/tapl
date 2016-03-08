AWS.config.update({
    accessKeyId:     'AKIAIWOTH7ZGXSZ3JWZA',
    secretAccessKey: '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',
});
AWS.config.region = 'us-east-1';
AWS.config.sslEnabled = true;

var lambda = new AWS.Lambda();

function run(interpreter, input, handler) {
    lambda.invoke({
        FunctionName: 'tapl_interpret',
        Payload: JSON.stringify({
            interpreter: interpreter,
            input: input,
        }),
    }, function (error, result) {
        if (error) {
            error = 'Internal error: ' + error;
        }
        else if (200 != result.StatusCode) {
            error = 'Internal error: code ' + result.StatusCode;
        }
        else {
            result = JSON.parse(result.Payload);
            if (result.errorType === 'IncompleteParseError') {
                error = 'Unexpected end of input';
            }
            else if (result.errorType === 'UnknownToken' ||
                     result.errorType === 'ParserError') {
                error = result.errorMessage;
            }
            else if (result.errorMessage) {
                error = 'Internal error: ' + result.errorMessage;
            }
        }
        if (error) {
            error += '\n';
        }
        handler(error, result);
    });
}

function addContent(content, isError) {
    var elem = document.createElement('span');
    elem.innerText = content;
    if (isError) {
        elem.classList.add('error');
    }
    results.appendChild(elem);
    elem.scrollIntoView();
}

var interpreter;
function setInterpreter(hash) {
    interpreter = hash || window.location.hash.slice(1) || 'untyped';
    addContent('Current language: ' + interpreter + '\n');
    document.getElementById('input').focus();
}

function onInputChange() {
    var results = document.getElementById('results');
    var elem    = document.getElementById('input');

    elem.readOnly = true;
    addContent('> ' + elem.value + '\n');
    run(interpreter, elem.value, function (error, result) {
        addContent(error || result, !!error);
        elem.value    = '';
        elem.readOnly = false;
    });
}

function hookupEvents() {
    document.getElementById('input').addEventListener('change', function (e) {
        onInputChange();
    });
}

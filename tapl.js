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
                     result.errorType === 'ParserError'  ||
                     result.errorType === 'EvaluationError') {
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
function setInterpreter(name) {
    interpreter = name;
    addContent('Current language: ' + interpreter + '\n');
    document.getElementById('input').focus();
    document.getElementById('rules').src = 'syntax/' + name + '.html';
}

function getInterpreterHistory() {
    var history = JSON.parse(window.localStorage.getItem('lineHistory'));
    if (!history[interpreter]) {
        history[interpreter] = [''];
    }
    window.localStorage.setItem('lineHistory', JSON.stringify(history));
    return history[interpreter];
}

function setInterpreterHistory(interpreterHistory) {
    var history = JSON.parse(window.localStorage.getItem('lineHistory'));
    history[interpreter] = interpreterHistory;
    window.localStorage.setItem('lineHistory', JSON.stringify(history));
}

function appendToHistory(input) {
    var history = getInterpreterHistory();
    history.splice(1, null, input);
    setInterpreterHistory(history);
}

function execute() {
    var results = document.getElementById('results');
    var elem    = document.getElementById('input');

    elem.readOnly = true;
    addContent('> ' + elem.value + '\n');
    appendToHistory(elem.value);
    run(interpreter, elem.value, function (error, result) {
        addContent(error || result, !!error);
        elem.value    = '';
        elem.readOnly = false;
    });
}

function initHistory() {
    var history = window.localStorage.getItem('lineHistory');
    if (!history) {
        window.localStorage.clear();
        window.localStorage.setItem('lineHistory', JSON.stringify({}));
    }
}

var historyCursor = 0;
function onInputKeydown(e) {
    var history = getInterpreterHistory();

    switch (e.keyCode) {
      case 38: {
        ++historyCursor;
      } break;

      case 40: {
        --historyCursor;
      } break;

      case 13: {
        execute();
        historyCursor = 0;
      } break;

      default:
        return;
    }

    if (historyCursor < 0) {
        historyCursor = 0;
    }

    if (historyCursor > (history.length - 1)) {
        historyCursor = history.length - 1;
    }

    var input = document.getElementById('input');
    input.value = history[historyCursor];
}

function hookupEvents() {
    var input = document.getElementById('input');
    input.addEventListener('keydown', onInputKeydown);
}


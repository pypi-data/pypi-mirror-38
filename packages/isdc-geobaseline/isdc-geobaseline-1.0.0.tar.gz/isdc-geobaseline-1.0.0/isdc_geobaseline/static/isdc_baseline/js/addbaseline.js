function addDivPackage(DOM_ID) {
    var getID = document.getElementById('immap-package');
    var div = document.createElement('div');
    div.setAttribute('id', DOM_ID);
    getID.appendChild(div);
}

function getBundle(JSBUNDLE, API, DOM_ID){
    $.getScript(JSBUNDLE, function(data, textStatus, jqxhr){
        var options = { urlBaseline: API }
        var viewer = new window[DOM_ID](DOM_ID, options);
        viewer.view();
    });
}
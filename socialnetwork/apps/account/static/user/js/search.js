var request
var x = 0

function len() {
    if (x === 0) {
        window.open("","_self")

    } else {
        x+=1;
        var url_mask = "{% url 'result_search' document.getElementById('search_bux').value  %}"
        var input = parseInt(document.getElementById('search_bux').value);
        return "{% url 'result_search' input %}"

    }
}


if (window.XMLHttpRequest) {
    request = new XMLHttpRequest()
} else {
    request = new ActiveXObject('Microsoft.XMLHTTP')
}

request.open('GET', 'email_list.json')
request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
        var items = JSON.parse(request.responseText);
        console.log(items);
    }
}
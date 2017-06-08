var apiUrl = window.location + "api/";

//update interface with portfolios and risk factors
function updateText() {

    console.log("apiUrl: " + apiUrl)
    //update portfolio lists
    var portfolioLists;
    $.get(apiUrl + 'portfolionames', function(data) {
        $('.enter-portfolio select').html(function() {
            var str = '<option value="" disabled="" selected="">[pick portfolio]</option>';
            var parsed = JSON.parse(data)
            console.log("data in get portfolionames" + data);
            for (var i = 0; i < parsed.length; i++) {
                str = str + '<option>' + parsed[i] + '</option>';
            }
            portfolioLists = parsed;
            console.log("str: " + str)
            return str;
        });
    });

    //update risk factors
    $.get(apiUrl + 'getriskfactors', function(data) {
        $('.risk-factor select').html(function() {
            var str = '<option value="" disabled="" selected="">[choose risk factor]</option>';
            console.log("risk factors: " + data);
            for (var i = 0; i < data.length; i++) {
                for (var key in data[i]) {
                    str = str + '<option risk-factor-id=' + key + '> ' + data[i][key] + '</option>';
                }
            }
            riskfactors = data;
            return str;
        });
    });

}

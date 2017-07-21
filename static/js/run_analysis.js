var apiUrl = location.protocol + '//' + location.host + location.pathname + "api/";

//check user input and process, generate result in tables
$('.run-analysis.Button').click(function(){

        console.log("Run Analysis");

        //retrieve user input
        var formPortfolio = $('.enter-portfolio select').find(":selected").text();
        var formShockMag = $('.enter-scenario input').val();
        var formRiseFall = $('.rise-fall select').find(":selected").text();
        var formRiskFactor = $('.risk-factor select').find(":selected").attr('risk-factor-id');
        var formRiskFactorName = $('.risk-factor select').find(":selected").text();

        console.log("formPortfolio: " + formPortfolio);
        console.log("formShockMag: " + formShockMag);
        console.log("formRiseFall: " + formRiseFall);
        console.log("formRiskFactor: " + formRiskFactor);
        console.log("formRiskFactorName: " + formRiskFactorName);

        //verify input otherwise display an informative message
        if(formPortfolio.includes('Loading...')) {
          alert("Load a portfolio first using Investment Portfolio service");
          return;
        } else if(formPortfolio.includes('[pick portfolio]')) {
          alert("Select a portfolio");
          return;
        } else if (formShockMag === "") {
          alert("Enter Shock value");
          return;
        } else if ((isNaN(formShockMag)) || (formShockMag < 0 || formShockMag > 200)) {
          alert("Enter a valid Shock");
          return;
        } else if(formRiseFall === undefined || formRiseFall.includes('[rise/fall]')) {
          alert("Select rise/fall");
          return;
        } else if(formRiskFactor === undefined || formRiskFactor.includes('[choose risk factor]')) {
          alert("Select a risk factor");
          return;
        } else {
          $('.sandboxtwo').toggleClass('loading');
          Process(formPortfolio, formRiskFactor, formRiskFactorName, formShockMag, formRiseFall, function(){
          });
        }
});

//create the output tables
function Process(formPortfolio, formRiskFactor, formRiskFactorName, formShockMag, formRiseFall) {
      //process input into server to create output json
      $('.loader').addClass('active');

      //calculate shock magnitude
      var ShockMag;
      if (formRiseFall === "rise") {
        ShockMag = 1+(formShockMag/100);
      } else {
        ShockMag = 1-(formShockMag/100);
      }

      //create json data
      var run_data = '{' + '"portfolio" : "' + formPortfolio + '", ' + '"riskfactor" : "' + formRiskFactor + '", ' + '"shockmag" : ' + ShockMag + '}';
      console.log("run data: " + run_data);

      //make ajax call to run services and populate table
      $.ajax({
      type: 'POST',
      url: apiUrl + 'analyze',
      data: run_data,
      dataType: 'json',
      contentType: 'application/json',
      beforeSend: function() {
          //alert('Fetching....');
      },
      success: function(data) {
          console.log(data);
          $('.sandboxtwo').removeClass('loading');

          //check for error in data
          if ('error' in data) {
            alert("Error: " + data.error);
            return;
          } else {
            $('.sandboxtwo').addClass('analysis');
            $('.loader').removeClass('active');
          }

          //display today date
          var today = new Date();
          var dd = today.getDate();
          var mm = today.getMonth()+1;
          var yyyy = today.getFullYear();
          if(dd<10) {
              dd='0'+dd
          }
          if(mm<10) {
              mm='0'+mm
          }
          today = mm+'/'+dd+'/'+yyyy;
          console.log(today);
          $('.date a').text(today);

          //update header
          var holdings_title = 'Projected impact on your portfolio resulting from a ' + formShockMag + '% ' + formRiseFall + ' in the ' + formRiskFactorName;
          $('.title1 h3').text(holdings_title);

          //display holdings data
          var holdings_data = data.holdingsInfo;
          var holdingsDataLength = holdings_data.length;
          console.log("Number of objects: " + holdingsDataLength);
          var tr = "";
          var SumCurrent = 0;
	        var SumStressed = 0;
          var totalPL = 0;

          for (var i = 0; i < holdingsDataLength; i++) {
              //console.log("asset: " + holdings_data[i].Asset + " BaseVal: " + holdings_data[i].BaseVal + " newVal: " + holdings_data[i].NewVal);
              var Name = holdings_data[i].Asset;
              var Company = holdings_data[i].CompanyName;
              var Quantiy = holdings_data[i].Quantity;

              //assign values
              var BaseVal_Orig = holdings_data[i].BaseVal;
              var NewVal_Orig = holdings_data[i].NewVal;
              var BaseVal_Array = holdings_data[i].BaseVal.split(" ");
              var NewVal_Array = holdings_data[i].NewVal.split(" ");
              var BaseVal = parseFloat(BaseVal_Array[0]);
              var NewVal = parseFloat(NewVal_Array[0]);

              //calculate total values
              SumCurrent += (Quantiy * BaseVal)
              SumStressed += (Quantiy * NewVal)

              //calculate change
              var Change = (((NewVal - BaseVal) / BaseVal) * 100).toFixed(2);
              BaseVal = BaseVal.toFixed(2);
              NewVal = NewVal.toFixed(2);
              console.log("Change: " + Change);

              //display change in values wtth red or green color
              var ChangeStr = '';
              if (Change < 0) {
                  ChangeStr = '<td class="red">' + Change + '%</td>';
              } else if (Change > 0) {
                  ChangeStr = '<td class="green">' + Change + '%</td>';
              } else if (Change == 0) {
                  ChangeStr = '<td class="">' + Change + '%</td>';
              }
              console.log("changeStr: " + ChangeStr);
              tr += "<tr tabindex='0' aria-label=" + Name + "><td>" + Name + "</td><td>" + Company + "</td><td>" + Quantiy + "</td><td>" + BaseVal + " " + BaseVal_Array[1] + "</td><td>" + NewVal + " " + NewVal_Array[1] + "</td>" + ChangeStr + "</tr>";
          }
          $('.port-table tbody').html(tr);

          //round and calulate total P&L
          totalPL = (((SumStressed - SumCurrent) / SumCurrent) * 100).toFixed(2);
          SumCurrent = SumCurrent.toFixed(2);
          SumStressed = SumStressed.toFixed(2);

          //display total P&L in values with red or green color
          var totalPLStr = '';
          if (totalPL < 0) {
              totalPLStr = '<td class="red"><strong>' + totalPL + '%</strong></td>';
          } else if (totalPL > 0) {
              totalPLStr = '<td class="green"><strong>' + totalPL + '%</strong></td>';
          } else if (totalPL == 0) {
              totalPLStr = '<td class=""><strong>' + totalPL + '%</strong></td>';
          }

          //display table footer
          var tf = "";
          tf += "<tr tabindex='0' aria-label=Portfolio Table><td><strong>Portfolio Total</strong></td><td></td><td></td><td>" + SumCurrent  +  " " + BaseVal_Array[1] +"</td><td align='left'>" + SumStressed + " " + NewVal_Array[1] + "</td>" + totalPLStr +"</tr>";
          $('.port-table tfoot').html(tf);

          //display market conditions table
          var mc_data = data.marketConditions;
          mc_data = sortByKey(mc_data, 'Stress_shift');
          var mcDataLength = mc_data.length;
          console.log("Number of mc objects: " + mcDataLength);
          var tr2 = "";
          for (var i = 0; i < mcDataLength; i++) {
              var RiskFactorName = mc_data[i].Risk_factor;
              var StressShift = mc_data[i].Stress_shift
              var StressShift_val = parseFloat(StressShift);
              StressShift_val = ((StressShift_val - 1)*100).toFixed(2)
              tr2 += "<tr tabindex='0' aria-label=" + RiskFactorName + "><td>" + RiskFactorName + "</td><td>" + StressShift_val + "%</td></tr>";
          }
          console.log(tr)
          $('.port-table2 tbody').html(tr2);
      },
      error: function(jqXHR, textStatus, errorThrown) {
          //reload on error
          $('.sandboxtwo').removeClass('loading');
          $('.sandboxtwo').addClass('analysis');
          $('.loader').removeClass('active');

          alert("Error: Try again")
          console.log(errorThrown);
          console.log(textStatus);
          console.log(jqXHR);

          location.reload();
      },
      complete: function() {
          //alert('Complete')
      }
    });
}

//sort the objects on key
function sortByKey(array, key) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
    });
}

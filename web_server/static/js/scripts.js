$(document).ready(function() {
    
    $.getJSON("initvals", function(init) {
        $.each(init, function(key, value){
            if (key !== 'thresh') {
                $("#"+key).val(value);
            }
        });
        th = init["thresh"]
        $("#thresh").prop("value", th);
        $("#showthresh").text(th);
        $("#showselect").val(th);
    });

    $('#light_06_state').change(function() {
        if (($(this).val() == "on")) {
            $("#light_06_int").prop("disabled", false);
        } else {
            $("#light_06_int").val("50");
            $("#light_06_int").prop("disabled", true);
        }
    });

    $('#light_07_state').change(function() {
        if (($(this).val() == "on")) {
            $("#light_07_int").prop("disabled", false);
        } else {
            $("#light_07_int").val("50");
            $("#light_07_int").prop("disabled", true);
        }
    });




    $('#txtsub').click(function() {
        //alert('asdf');
        /* setting currently changed option value to option variable */
        /*var option = $(this).find('#txtval').val();
        /* setting input box value to selected option value */
        /*$('#showtime').val(option);
        alert( "asdf");


        $.get("/test.py?thresh="+option, function(data) {
            alert( "Data Loaded: ");*/
        thresh = $("#thresh").val();
        //alert(thresh);
        if ($.isNumeric(thresh)) {
            $('#showthresh').text(thresh);
        } else {
            thresh = "";
        }
        

        light_06_state = $("#light_06_state").val();

        light_06_int = $("#light_06_int").val();

        light_07_state = $("#light_07_state").val();

        light_07_int = $("#light_07_int").val();

        $.post("/setvals",
            {thresh: thresh,
            light_06_state: light_06_state,
            light_06_int: light_06_int,
            light_07_state: light_07_state,
            light_07_int: light_07_int
        });
    });

    $('#realtime').click(function() {

        //var MQTTbroker = 'broker.mqttdashboard.com';
        //var MQTTport = 8000;
        var MQTTbroker = '147.102.7.186';
        var MQTTport = 9001;
        var MQTTsubTopic1 = 'thesis/power/08'; //works with wildcard # and + topics dynamically now
        var MQTTsubTopic2 = 'thesis/power/09'; //works with wildcard # and + topics dynamically now
        //settings END

        var chart_h; // global variuable for chart
        var chart_r;
        var dataTopics = new Array();

    //mqtt broker 
        var client = new Messaging.Client(MQTTbroker, MQTTport,
                    "myclientid_" + parseInt(Math.random() * 100, 10));
        client.onMessageArrived = onMessageArrived;
        client.onConnectionLost = onConnectionLost;
        //connect to broker is at the bottom of the init() function !!!!
        

    //mqtt connecton options including the mqtt broker subscriptions
        var options = {
            timeout: 3,
            onSuccess: function () {
                console.log("mqtt connected");
                // Connection succeeded; subscribe to our topics
                client.subscribe(MQTTsubTopic1, {qos: 1});
                client.subscribe(MQTTsubTopic2, {qos: 1});
                },
            onFailure: function (message) {
                console.log("Connection failed, ERROR: " + message.errorMessage);
                //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
            }
        };

    //can be used to reconnect on connection lost
        function onConnectionLost(responseObject) {
            console.log("connection lost: " + responseObject.errorMessage);
            //window.setTimeout(location.reload(),20000); //wait 20seconds before trying to connect again.
        };

    //what is done when a message arrives from the broker
        function onMessageArrived(message) {
            console.log(message.destinationName, '',message.payloadString);

            //check if it is a new topic, if not add it to the array
            if (dataTopics.indexOf(message.destinationName) < 0){
                
                dataTopics.push(message.destinationName); //add new topic to array
                var y = dataTopics.indexOf(message.destinationName); //get the index no
                
                //create new data series for the chart
                if (message.destinationName === 'thesis/power/09'){
                    var color = '#EB6881';
                }
                else {
                    var color;
                }
                var newseries = {
                        id: y,
                        name: message.destinationName,
                        data: [],
                        color: color
                        };

                chart_r.addSeries(newseries); //add the series
                
                };
            
            var y = dataTopics.indexOf(message.destinationName); //get the index no of the topic from the array
            var myEpoch = new Date().getTime();
            var timezone = new Date().getTimezoneOffset();
            var thenum = message.payloadString.replace( /^\D+/g, ''); //remove any text spaces from the message
            var plotMqtt = [myEpoch-timezone*60000, Number(thenum)]; //create the array
            if (isNumber(thenum)) { //check if it is a real number and not text
                console.log('is a propper number, will send to chart.')
                plot(plotMqtt, y);  //send it to the plot function
            };
        };

    //check if a real number    
        function isNumber(n) {
          return !isNaN(parseFloat(n)) && isFinite(n);
        };

    //function that is called once the document has loaded
        function init() {

            //i find i have to set this to false if i have trouble with timezones.
            Highcharts.setOptions({
                global: {
                    //useUTC: false
                }
            });

            // Connect to MQTT broker
            client.connect(options);

        };


    //this adds the plots to the chart  
        function plot(point, chartno) {
            console.log(point);
            
                var series = chart_r.series[0],
                    shift = series.data.length > 20; // shift if the series is 
                                                     // longer than 20
                // add the point
                chart_r.series[chartno].addPoint(point, true, shift);  

        };
                init();
                //$('#showtime').val("Real time data");
                chart_r = new Highcharts.Chart({
                    chart: {
                        renderTo: 'chart_hist',
                        defaultSeriesType: 'spline'
                    },
                    title: {
                        text: 'Power consumption (live data)'
                    },
                    subtitle: {
                                        text: 'myMQTTbroker: ' + MQTTbroker + ' | port: ' + MQTTport
                                },
                    xAxis: {
                        type: 'datetime',
                        tickPixelInterval: 150,
                        maxZoom: 20 * 1000
                    },
                    yAxis: {
                        minPadding: 0.2,
                        maxPadding: 0.2,
                        title: {
                            text: 'Value',
                            margin: 80
                        }
                    },
                    series: []
                });        
            });
        

    $('#timeinterval').change(function() {
        /* setting currently changed option value to option variable */
        var option = $(this).find('option:selected').val();
        var name = $(this).find('option:selected').attr("name");
        /* setting input box value to selected option value */
        //$('#showtime').val(option);

            var datetime = [];
            var sensor_one = [];
            var sensor_two = [];
            var series;
            var sensornum;
            var sensorval;
            var timestamp;
            var assoc_sens = {};
            

            $.getJSON("?time="+option, function(data) {
            //data = data.split('/');
            //console.log(data[0]);
            timezone = new Date().getTimezoneOffset();
            //console.log(timezone);
            $.each(data, function( index, value ) {
                //console.log(value[0], value[1], value[2]);
                //timestamp = parseFloat(value[0])*1000 + 10800000;
                timestamp = parseFloat(value[0])*1000 - timezone*60*1000;
                sensornum = value[1];
                sensorval = parseFloat(value[2]);
                if (sensornum == 8) {sensor_one.push({
                                            x: timestamp,
                                            y: sensorval
                                        });
                                    }
                if (sensornum == 9) {sensor_two.push({
                                            x: timestamp,
                                            y: sensorval
                                        });
                                    }

            });

            
            //datetime.pop();

            chart_h = new Highcharts.Chart({
            chart : {
            renderTo: 'chart_hist',
            type : 'spline'
            },
            title : {
            text : 'Power consumption (' + name + ')'
            },
            subtitle : {
            text : 'thesis'
            },
            xAxis : {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                        month: '%e. %b',
                        year: '%b'
            },
            title : {
            text : 'Date and time'
            },
            //categories : datetime,
            //tickInterval: 24* 10
            },
            yAxis : {
            title : {
            text : 'Sensor Value'
            },
            labels : {
            formatter : function() {
            return this.value
            }
            }
            },
            tooltip : {
            crosshairs : true,
            shared : true,
            valueSuffix : ''
            },
            plotOptions : {
            spline : {
            turboThreshold: 0,
            marker : {
            radius : 4,
            lineColor : '#666666',
            lineWidth : 1,
            }
            }
            },
            series : [{

            name : 'Sensor 08',
            data : sensor_one
            },{

            name : 'Sensor 09',
            data : sensor_two,
            color: '#EB6881'

            }]
            });
        });
    });

$("#realtime").click()
});

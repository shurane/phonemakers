(function(window, undefined){
    source = $("#entry-template").html(); // TODO remove global
    template = Handlebars.compile(source); // TODO remove global
    $.getJSON("mdict.json", function(data){
        dundun = data; // XXX remove later
        phoneystump = dundun["Acer"][0]; // XXX remove later
        //console.log(template(phoneystump));

        var listum = document.getElementById("hacker-list");
        var listumine = $("#hacker-list");

        var count = 0;
        for(var makerName in data){
            var maker = data[makerName];
            for (var phoneName in maker){
                count +=1;
                if ( count % 300 === 0 ){
                    var phone = maker[phoneName];
                    var phoneHTML = template(phone);
                    listumine.append(phoneHTML);
                    console.log(phone.url);
                    //console.log(phoneHTML);
                    //console.log($.parseHTML(phoneHTML));

                }
            }
        }
        console.log(count);

    });
}());


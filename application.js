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
                if ( count % 500 === 0 ){
                    var phone = maker[phoneName];
                    var phoneHTML = template(phone);
                    listumine.append(phoneHTML);
                    if (phone.description !== null)
                        console.log(phone.description);
                    //console.log(phoneHTML);
                    //console.log($.parseHTML(phoneHTML));

                }
            }
        }
        console.log(count);

    });
}());


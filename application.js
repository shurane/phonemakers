(function(window, undefined){
    //var document = window.document;
    //dundun = {};  // XXX remove later
    source = $("#entry-template").html();
    template = Handlebars.compile(source);
    $.getJSON("mdict.json", function(data){
        //var options = { item: 'hacker-item' };
        //var hackerList = new List('hacker-list', options, data["ZTE"]);
        dundun = data; // XXX remove later
        phoneystump = dundun["Acer"][0];
        console.log(template(phoneystump));

        //var listum = document.getElementById("hacker-list");

        var count = 0;
        for(var makerName in data){
            var maker = data[makerName];
            for (var phoneName in maker){
                count +=1;
                if ( count % 1200 === 0 ){
                    var phone = maker[phoneName];
                    var phoneHTML = template(phone);
                    console.log(phoneHTML);

                    //var element = document.createElement("div");

                    //console.log("========================================");
                    //var okayFields = [ "Dimensions", "Body", "OS", "CPU", "SIZE"];
                    //for (var fieldName in phone.fields){
                        //var fieldElem = document.createElement("p");
                        //console.log("====");
                        //console.log("Field::"+ fieldName);
                        //for (var sectionName in phone.fields[fieldName]){
                            //var sectionElem = document.createElement("p");
                            //console.log("Section::" + sectionName + "::" + phone.fields[fieldName][sectionName]);
                        //}
                    //}
                }
            }
        }
        console.log(count);

    });
}());


(function(window, undefined){
    //var document = window.document;
    //dundun = {};  // XXX remove later
    $.getJSON("mdict.json", function(data){
        //var options = { item: 'hacker-item' };
        //var hackerList = new List('hacker-list', options, data["ZTE"]);
        dundun = data;
        phoneystump = dundun["Acer"][0];

        var listum = document.getElementById("hacker-list");

        var count = 0;
        for(var makerName in data){
            console.log(makerName);
            var maker = data[makerName];
            for (var phoneName in maker){
                var phone = maker[phoneName];

                var element = document.createElement("div");
                var para = document.createElement("p");
                var anchor = document.createElement("a");
                var dimensions = document.createElement("p");

                dimensions.innerHTML = phone.fields.Body.Dimensions;
                anchor.innerHTML = phone.url;
                para.innerHTML = phone.canonical_name;

                element.appendChild(para);
                element.appendChild(anchor);
                element.appendChild(dimensions);

                listum.appendChild(element);
                count +=1;
                if ( count % 50 === 0 ){
                    //console.log(count, phone);
                    console.log(element)
                }
            }
        }
        console.log(count);

    });
}());


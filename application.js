(function(window, undefined){
    //source = $("#entry-template").html(); // TODO remove global
    //template = Handlebars.compile(source); // TODO remove global

    var Phone = Backbone.Model.extend({
        defaults: {
            name: 'voidthis',
            maker: 'voidtech',
            fields: {}
        },
        initialize: function(){  
            
        }
    });

    var PhoneList = Backbone.Collection.extend({
        model: Phone,
        url: "/phones.json",

        byMaker: function(maker) {
            return this.where({maker: maker});
        },
        byName: function(name) {
            return this.filter(function(phone){
                return _.str.include(phone.get('name'), name);
            });
        },
        comparator: 'name'
    });

    nexusone = new Phone({ name:"Google Nexus One", maker: "Google"});
    Phones = new PhoneList();
    Phones.fetch();

    //$.getJSON("phones.json", function(data){
    //});

}());
// IIFE http://benalman.com/news/2010/11/immediately-invoked-function-expression/

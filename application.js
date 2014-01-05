(function(window, undefined){
    phoneSource = $("#phoneTemplate").html(); // TODO remove global
    phoneTemplate = Handlebars.compile(phoneSource); // TODO remove global

    var Phone = Backbone.Model.extend({
        defaults: {
            name: 'voidthis',
            maker: 'voidtech',
            fields: {}
        }
    });

    var PhoneCollection = Backbone.Collection.extend({
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
        comparator: 'name',


        // https://gist.github.com/io41/838460
        parse: function(resp) {
            this.page = 0;
            this.perPage = 20;
            this.total = resp.length;
            return resp;
        },

        pageInfo: function() {
            var info = {
                total: this.total,
                page: this.page,
                perPage: this.perPage,
                pages: Math.ceil(this.total / this.perPage),
                prev: false,
                next: false
            };

            var max = Math.min(this.total, this.page * this.perPage);

            if (this.total == this.pages * this.perPage) {
                max = this.total;
            }

            info.range = [(this.page - 1) * this.perPage + 1, max];

            if (this.page > 1) {
                info.prev = this.page - 1;
            }

            if (this.page < info.pages) {
                info.next = this.page + 1;
            }

            return info;
        },
        nextPage: function() {
            if (!this.pageInfo().next) {
                return false;
            }
            this.page = this.page + 1;
            return this.fetch();
        },
        previousPage: function() {
            if (!this.pageInfo().prev) {
                return false;
            }
            this.page = this.page - 1;
            return this.fetch();
        }

    });

    // // William Saunders mentions typing a View to typeahead
    //var SearchView = Backbone.View.extend({
        //render: function() {
            ////this.$el.clear();
            //this.$el.html( this.searchTemplate( someContext ) );
            //this.$('.example-phones .typeahead').typeahead({                                
                //name: 'countries',                                                          
                //prefetch: '../data/countries.json',                                         
                //limit: 10                                                                   
            //});
            //return this;
        //},
        //searchTemplate: _.template( $( "script#typeAheadBox" ) )
    //});

    var PhoneView = Backbone.View.extend({
        tagName : "div",
        template : phoneTemplate,
        render : function (){
            // use mustache templates here
            
            this.$el.html(this.template(this.model.attributes));
        }
    });

    var ApplicationView = Backbone.View.extend({
        el : "#phoneapp"
    });

    phoneapp = new ApplicationView();
    phoneapp.render();
    phoneCollection = new PhoneCollection();
    phoneCollection.fetch();

    setTimeout(function(){
        phonesumine = phoneCollection.at(0);
        phonesumineView = new PhoneView({model:phonesumine});
        phonesumineView.render();

        $("#phonecollection").html(phonesumineView.$el);

    }, 2000);

}());
// IIFE http://benalman.com/news/2010/11/immediately-invoked-function-expression/

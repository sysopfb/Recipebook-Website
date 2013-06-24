 var NavView = Backbone.View.extend({
    el: '#navigation',
    events: {
        'click #AllButton': 'getAll',
        'click #Search': 'searchFunc',
        'click #Create': 'createFunc',
    },
    initialize: function() {
        users = new UsersCollection();
        recipes = new RecipeCollection();
        searchlist = new RecipeCollection();
    },
    /*
    getAll: function(event) {
        var rtemplate = _.template($('#recipe-template').html());
        //var users = new UsersCollection();
        //var recipes = new RecipeCollection();
        recipes.fetch().done(function() {
            $('#recipe-list').html('');
            recipes.forEach(function(model) {
                $('#recipe-list').append(rtemplate(model.toJSON()));
            });
        });
    },
*/
    getAll: function(even) {
        recipes.fetch().done(function() {
            var view = new RecipeView({collection: recipes});
            view.render();
        });
    },
    
    searchFunc : function(event) {
        var name = $('#sname');
        var type = $('#stype');
        $('#dialog-search').dialog({
            modal: 'true',
            buttons: {
                "Search": function() {
                    searchlist.fetch({data: $.param({'data': name.val(), 'type': type.val()})}).done(function () {
                        var view = new RecipeView({collection: searchlist});
                        view.render();
                    });
                    $(this).dialog("close");
                },
                Cancel: function () {
                    $(this).dialog("close");
                }
            },
            //turns off submitting with the enter key
            open: function() {
                $(this).keypress(function(e) {
                    if (e.keyCode == $.ui.keyCode.ENTER) {
                        e.preventDefault();
                        e.stopPropagation();
                    }
                });
            }
        });
    },

    createFunc : function(event) {
        var rname = $('#name');
        var ringredients = $('textarea#ingredients');
        var rinstructions = $('textarea#instructions');
        var rauthor = $('#author');
        $('#dialog-create').dialog({
            modal: 'true',
            buttons: {
                "Create": function() {
                    var lines = ringredients.val().replace(/\r\n/g, "\n").split("\n");
                    var lines2 = rinstructions.val().replace(/\r\n/g, "\n").split("\n");
                    recipes.create({name: rname.val(),
                                    ingredients: lines,
                                    instructions: lines2,
                                    author: rauthor.val()
                                    });
                },
                Clear: function() {
                    rname.val("");
                    ringredients.val("");
                    rinstructions.val("");
                },
                Close: function() {
                    $(this).dialog("close");
                }
            }
        });
    }
});

RecipeView = Backbone.View.extend({
    el: "#recipe-list",
    tagName: "ul",
    events: {
        "click li": "clicked"
    },

    clicked: function(e){
        e.preventDefault();
        var r_id = $(e.currentTarget).data("id");
        var item = this.collection.get(r_id);
        //var name = item.get("name");
        var rname = $('#name').val(item.get("name"));
        ilist = item.get("ingredients");
        instruct_list = item.get("instructions");
        var ringredients = $('textarea#ingredients').val(ilist.join("\n"));
        var rinstructions = $('textarea#instructions').val(instruct_list.join("\n"));
        var rauthor = $('#author').val(item.get("author"));
        $('#dialog-create').dialog({
            modal: 'true',
            buttons: {
                "Update": function() {
                    var lines = ringredients.val().replace(/\r\n/g, "\n").split("\n");
                    var lines2 = rinstructions.val().replace(/\r\n/g, "\n").split("\n");
                    item.save({id: r_id,
                               name: rname.val(),
                               ingredients: lines,
                               instructions: lines2,
                               author: rauthor.val()
                               });
                },
                "Delete": function() {
                    item.destroy();
                },
                Clear: function() {
                    rname.val("");
                    ringredients.val("");
                    rinstructions.val("");
                },
                Cancel: function() {
                    $(this).dialog("close");
                }
            }
        });
        
    },

     render: function(){
        var rtemplate = _.template($('#recipe-template').html());
        var el = $(this.el);
        el.html('');
        this.collection.each(function(model){
            var html = rtemplate(model.toJSON());
            el.append(html);
        });
    }
});

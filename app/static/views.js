 var View = Backbone.View.extend({
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

    searchFunc : function(event) {
        var name = $('#sname');
        var rtemplate = _.template($('#recipe-template').html());
        $('#dialog-search').dialog({
            modal: 'true',
            buttons: {
                "Search": function() {
                    searchlist.fetch({data: $.param({'data': name.val()})}).done(function () {
                        $('#recipe-list').html('');
                        searchlist.forEach(function(model) {
                            $('#recipe-list').append(rtemplate(model.toJSON()));
                        });
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
                    recipes.create({name: rname.val(),
                                    ingredients: lines,
                                    instructions: rinstructions.val(),
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

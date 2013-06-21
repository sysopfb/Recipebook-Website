 var View = Backbone.View.extend({
    el: '#navigation',
    events: {
        'click #AllButton': 'getAll',
        'click #Search': 'searchFunc',
    },
    initialize: function() {
        users = new UsersCollection();
        recipes = new RecipeCollection();
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
        var name = $('#name');
        $('#dialog-search').dialog({
            modal: 'true',
            buttons: {
                "Search": function() {
                    console.log(name.val())
                },
                Cancel: function () {
                    $(this).dialog("close");
                }
            }
        });
    }
        
});

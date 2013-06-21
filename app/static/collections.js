var UsersCollection = Backbone.Collection.extend({
    model: User,
    url: '/users',
    parse : function(resp) {
        //console.log(resp.items);
        return resp.items;
    }

});
var RecipeCollection = Backbone.Collection.extend({
    model: Recipe,
    url: '/recipes',
    parse: function(resp) {
        return resp.items;
    }
});


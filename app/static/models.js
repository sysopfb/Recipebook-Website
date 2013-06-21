 var User = Backbone.Model.extend({
    defaults: {
        name: '',
        email: ''
    }
});
var Recipe = Backbone.Model.extend({
    defaults: {
        name: '',
        ingredients: '',
        instructions: '',
        author: ''
    }
});

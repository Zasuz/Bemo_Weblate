odoo.define('estate.ButtonNotify', function (require) {
    "use strict";

    const ListController = require('web.ListController');
    const viewRegistry = require('web.view_registry');
    const ListView = require('web.ListView');

    const ButtonNotifyListController = ListController.extend({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                const $button = $('<button type="button" class="btn btn-primary">Click Tui</button>');
                $button.on('click', this._onButtonClick.bind(this));
                this.$buttons.prepend($button);
            }
        },

        _onButtonClick: function () {
            this.do_notify('Notification', 'Hello!');
        },
    });

    const ButtonNotifyListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: ButtonNotifyListController,
        }),
    });
    viewRegistry.add('button_notify', ButtonNotifyListView);

    return {
        ButtonNotifyListController: ButtonNotifyListController,
        ButtonNotifyListView: ButtonNotifyListView
    };
});

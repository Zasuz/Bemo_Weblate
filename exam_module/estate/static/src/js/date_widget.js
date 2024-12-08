odoo.define('estate.DatePickerWidget', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');

    var DatePickerWidget = AbstractField.extend({

        events: {
            'change .o_date_picker': '_onDateChange',
        },

        init: function() {
            console.log("init");
            this._super.apply(this, arguments);
        },

        /**
         * Hàm này được gọi khi widget ở chế độ readonly.
         */
        _renderReadonly: function() {
            console.log("readonly");
            let formattedDate = ''
            if (this.value) {
                let date = new Date(this.value);
                let month = ('0' + (date.getMonth() + 1)).slice(-2); // Get month and pad with leading zero if needed
                let year = date.getFullYear();
                formattedDate = `${month}/${year}`;
            }

            this.$el.append($('<text>', {
                'class': 'o_date_picker',
            }).text(formattedDate));
        },

        /**
         * Hàm này được gọi khi widget ở chế độ edit.
         */
        _renderEdit: function () {
            console.log("edit");
            this.$el.empty();

            let formattedDate = ''
            if (this.value) {
                let date = new Date(this.value);
                formattedDate = date.toISOString().split('T')[0];
            }
            this.$el.append($('<input>', {
                'type': 'date',
                'class': 'o_date_picker',
                'value': formattedDate,
            }));
        },

        _onDateChange: function (event) {
            console.log("Date change" + event.target.value);
            this._setValue(event.target.value);
        },

    });

    fieldRegistry.add('date_widget', DatePickerWidget);

    return DatePickerWidget;
});

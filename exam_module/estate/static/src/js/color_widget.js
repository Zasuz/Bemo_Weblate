odoo.define('estate.ColorPickerWidget', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var rpc = require('web.rpc');

    var ColorPickerWidget = AbstractField.extend({

        events: {
            'click .o_color_pill': 'clickColorPill',
        },

        init: function () {
            this.totalColors = 10;
            this.totalRecords = 0;
            this._super.apply(this, arguments);
        },

        // Hàm RPC để lấy tổng số bản ghi
        _getTotalRecords: function () {
            var self = this;
            return rpc.query({
                model: 'estate.widget',
                method: 'count_records',
                args: []
            }).then(function (result) {
                self.totalRecords = result;
            });
        },

        _renderColorReadonly: function () {
            this.$el.empty();
            var className = 'o_color_pill active readonly o_color_' + this.value
            if (this.value == 0) {
                className += ' empty-color'
            }
            // if (this.value == 0 ) {
            //     <span></span>
            // }
            this.$el.append($('<span>', {
                'class': className,
            }));
            if (this.viewType !== 'list') {
                this.$el.append($('<h6>', { 'class': 'total-records' }).text("Total of record have color: " + this.totalRecords));
            }
        },
        _renderReadonly: function () {

            if (this.viewType !== 'list') {
                this._getTotalRecords().then(() => {
                    this._renderColorReadonly();
                });
            } else {
                this._renderColorReadonly();
            }
        },

        isSet : function () {
            return true;
        },

        _renderEdit: function () {
            var self = this;

            this._getTotalRecords().then(function () {
                self.$el.empty();

                for (let i = 0; i < self.totalColors; i++) {
                    var className = 'o_color_pill o_color_' + i;
                    if (self.value === i) {
                        className += ' active';
                    }
                    self.$el.append($('<span>', {
                        'class': className,
                        'data-val': i,
                    }));
                }
                self.$el.append($('<h6>', {'class': 'total-records'}).text("Total of record have color: " + self.totalRecords));
            });
        },

        clickColorPill: function (ev) {
            var $target = $(ev.currentTarget);
            var data = $target.data();
            this._setValue(data?.val?.toString());
        }
    });

    fieldRegistry.add('color_picker_widget', ColorPickerWidget);

    return ColorPickerWidget;
});

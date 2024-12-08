odoo.define("estate.CheckBoxWidget", function (require) {
    'use strict';

    const ButtonNotifyListController = require('estate.ButtonNotify').ButtonNotifyListController
    const ListView = require('web.ListView');
    const viewRegistry = require('web.view_registry');


    const CheckBoxListController = ButtonNotifyListController.extend({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.isHideColorChecked = false;
            this.isHideDateChecked = false;
            this.currentStageHideDateApply = false;
            this.currentStageHideColorApply = false;
            this.isClearing = false
            console.log("init");
        },
        update: function (params, options) {
            // Lưu trạng thái ẩn hiện của các Checkbox
            params.columnInvisibleFields = params.columnInvisibleFields || {};
            params.columnInvisibleFields['color'] = this.currentStageHideColorApply;
            params.columnInvisibleFields['date'] = this.currentStageHideDateApply;
            this.$buttons.find('#hideColor').prop('checked', this.currentStageHideColorApply);
            this.$buttons.find('#hideDate').prop('checked', this.currentStageHideDateApply);

            return this._super(params, options);
        },
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            console.log("renderer button");
            if (this.$buttons) {
                const input = '<input class="ml-2" type="checkbox" id="hideColor" name="hideColor" value="HideColor">\n' +
                    '<label for="hideColor"> Hide Color</label>\n' +
                    '<input class="ml-2" type="checkbox" id="hideDate" name="hideDate" value="HideDate">\n' +
                    '<label for="hideDate"> Hide Date</label>\n' +
                    '<button id="applyButton" type="button" class="mx-2 btn btn-primary">Apply</button>'+
                    '<button id="clearButton" type="button" class="btn btn-secondary">Clear</button>';

                this.$buttons.append(input);
                // Event buttons
                this.$buttons.find('#hideColor').on('change', this._onHideColorChange.bind(this));
                this.$buttons.find('#hideDate').on('change', this._onHideDateChange.bind(this));
                this.$buttons.find('#applyButton').on('click', this._onApplyButtonClick.bind(this));
                this.$buttons.find('#clearButton').on('click', this._onClearButtonClick.bind(this));

                this.$buttons.find('#applyButton').hide();
                this.$buttons.find('#clearButton').hide();
            }
        },

        _onApplyButtonClick: function () {
            this.currentStageHideDateApply = this.isHideDateChecked;
            this.currentStageHideColorApply = this.isHideColorChecked;
            this.renderer._processColumns(this.renderer.columnInvisibleFields);
            this.renderer._render();
        },

        _onClearButtonClick: function () {
            // Set cac stage về giá trị ban đầu
            this.$buttons.find('#hideColor').prop('checked', false).change();
            this.$buttons.find('#hideDate').prop('checked', false).change();
            this.currentStageHideDateApply = false;
            this.currentStageHideColorApply = false;
            this.renderer._processColumns(this.renderer.columnInvisibleFields);
            this.renderer._render();
        },

        _onHideColorChange: function (event) {
            // Ngăn chặn tạo vòng lap vô hạn
            if (this.isClearing) return;
            this.isHideColorChecked = event.target.checked;
            this.renderer.columnInvisibleFields['color'] = this.isHideColorChecked;
            this._toggleButton()

        },

        _onHideDateChange: function (event) {
            // Ngăn chặn tạo vòng lap vô hạn
            if (this.isClearing) return;
            this.isHideDateChecked = event.target.checked;
            this.renderer.columnInvisibleFields['date'] = this.isHideDateChecked;
            this._toggleButton()
        },
        _toggleButton: function () {
            const applyButton = this.$buttons.find('#applyButton');
            const clearButton = this.$buttons.find('#clearButton');

            if (this.isHideColorChecked || this.isHideDateChecked) {
                applyButton.show();
                clearButton.show();

            } else {
                // Bât flag isClearing để tránh gọi lại hàm _onChange của 2 checkBox
                this.isClearing = true;
                this._onClearButtonClick();
                this.isClearing = false;

                applyButton.hide();
                clearButton.hide();

            }
        }



    })
    // const CheckboxRenderer = ListRenderer.extend({
    //     // init: function (parent, state, params) {
    //     //     params.columnInvisibleFields = params.columnInvisibleFields || {};
    //     //     this.renderer.columnInvisibleFields['date'] = true;
    //     //     this._super(parent, state, params);
    //     // },
    //     updateState: function (state) {
    //
    //         this._super.apply(this, arguments);
    //         console.log("update state");
    //     }
    //
    // });

    const CheckBoxListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CheckBoxListController,
            // Renderer: CheckboxRenderer,
        }),
    });

    viewRegistry.add('inherit_button_notify', CheckBoxListView);


});
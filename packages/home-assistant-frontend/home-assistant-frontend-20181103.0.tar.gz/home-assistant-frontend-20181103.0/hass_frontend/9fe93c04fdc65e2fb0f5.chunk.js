(window.webpackJsonp=window.webpackJsonp||[]).push([[58],{651:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_paper_dialog_scrollable_paper_dialog_scrollable__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(210),_polymer_paper_dialog_paper_dialog__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(207),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(0),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_resources_ha_style__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(120),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(16);class HaLoadedComponents extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_5__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_3__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_2__.a`
    <style include="ha-style-dialog">
      paper-dialog {
        max-width: 500px;
      }
    </style>
    <paper-dialog id="dialog" with-backdrop="" opened="{{_opened}}">
      <h2>Loaded Components</h2>
      <paper-dialog-scrollable id="scrollable">
       <p>The following components are currently loaded:</p>
       <ul>
        <template is='dom-repeat' items='[[_components]]'>
          <li>[[item]]</li>
        </template>
       </ul>
      </paper-dialog-scrollable>
    </paper-dialog>
    `}static get properties(){return{_hass:Object,_components:Array,_opened:{type:Boolean,value:!1}}}ready(){super.ready()}showDialog({hass}){this.hass=hass;this._opened=!0;this._components=this.hass.config.components.sort();setTimeout(()=>this.$.dialog.center(),0)}}customElements.define("ha-loaded-components",HaLoadedComponents)}}]);
//# sourceMappingURL=9fe93c04fdc65e2fb0f5.chunk.js.map
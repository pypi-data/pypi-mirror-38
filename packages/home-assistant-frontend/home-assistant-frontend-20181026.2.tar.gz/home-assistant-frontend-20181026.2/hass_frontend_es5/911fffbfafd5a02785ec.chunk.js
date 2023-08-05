(window.webpackJsonp=window.webpackJsonp||[]).push([[15],{217:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(26),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(42),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(129),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(3),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(0),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(99);function _templateObject(){var data=_taggedTemplateLiteral(["\n    <style include=\"paper-item-shared-styles\"></style>\n    <style>\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n        @apply --paper-icon-item;\n      }\n\n      .content-icon {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n\n        width: var(--paper-item-icon-width, 56px);\n        @apply --paper-item-icon;\n      }\n    </style>\n\n    <div id=\"contentIcon\" class=\"content-icon\">\n      <slot name=\"item-icon\"></slot>\n    </div>\n    <slot></slot>\n"]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:Object(_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a)(_templateObject()),is:"paper-icon-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a]})},648:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_app_layout_app_toolbar_app_toolbar_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(122),_polymer_iron_flex_layout_iron_flex_layout_classes_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(31),_polymer_paper_icon_button_paper_icon_button_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(62),_polymer_paper_item_paper_icon_item_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(217),_polymer_paper_item_paper_item_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(120),_polymer_paper_listbox_paper_listbox_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(123),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(0),_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(4),_ha_icon_js__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(87),_util_hass_translation_js__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(56),_mixins_localize_mixin_js__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(9),_common_config_is_component_loaded_js__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(136);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n    <style include=\"iron-flex iron-flex-alignment iron-positioning\">\n      :host {\n        --sidebar-text: {\n          color: var(--sidebar-text-color);\n          font-weight: 500;\n          font-size: 14px;\n        };\n        height: 100%;\n        display: block;\n        overflow: auto;\n        -ms-user-select: none;\n        -webkit-user-select: none;\n        -moz-user-select: none;\n        border-right: 1px solid var(--divider-color);\n        background-color: var(--sidebar-background-color, var(--primary-background-color));\n      }\n\n      app-toolbar {\n        font-weight: 400;\n        color: var(--primary-text-color);\n        border-bottom: 1px solid var(--divider-color);\n        background-color: var(--primary-background-color);\n      }\n\n      app-toolbar a {\n        color: var(--primary-text-color);\n      }\n\n      paper-listbox {\n        padding: 0;\n      }\n\n      paper-listbox > a {\n        @apply --sidebar-text;\n        text-decoration: none;\n\n        --paper-item-icon: {\n          color: var(--sidebar-icon-color);\n        };\n      }\n\n      paper-icon-item {\n        margin: 8px;\n        padding-left: 9px;\n        border-radius: 4px;\n        --paper-item-min-height: 40px;\n      }\n\n      .iron-selected paper-icon-item:before {\n        border-radius: 4px;\n        position: absolute;\n        top: 0;\n        right: 0;\n        bottom: 0;\n        left: 0;\n        pointer-events: none;\n        content: \"\";\n        background-color: var(--sidebar-selected-icon-color);\n        opacity: 0.12;\n        transition: opacity 15ms linear;\n        will-change: opacity;\n      }\n\n      .iron-selected paper-icon-item[pressed]:before {\n        opacity: 0.37;\n      }\n\n      paper-icon-item span {\n        @apply --sidebar-text;\n      }\n\n      a.iron-selected {\n        --paper-item-icon: {\n          color: var(--sidebar-selected-icon-color);\n        };\n      }\n\n      a.iron-selected .item-text {\n        color: var(--sidebar-selected-text-color);\n      }\n\n      paper-icon-item.logout {\n        margin-top: 16px;\n      }\n\n      .divider {\n        height: 1px;\n        background-color: var(--divider-color);\n        margin: 4px 0;\n      }\n\n      .subheader {\n        @apply --sidebar-text;\n        padding: 16px;\n      }\n\n      .dev-tools {\n        padding: 0 8px;\n      }\n\n      .dev-tools a {\n        color: var(--sidebar-icon-color);\n      }\n\n      .profile-badge {\n        /* for ripple */\n        position: relative;\n        box-sizing: border-box;\n        width: 40px;\n        line-height: 40px;\n        border-radius: 50%;\n        text-align: center;\n        background-color: var(--light-primary-color);\n        text-decoration: none;\n        color: var(--primary-text-color);\n      }\n\n      .profile-badge.long {\n        font-size: 80%;\n      }\n    </style>\n\n    <app-toolbar>\n      <div main-title=>Home Assistant</div>\n      <template is='dom-if' if='[[hass.user]]'>\n        <a href='/profile' class$='[[_computeBadgeClass(_initials)]]'>\n          <paper-ripple></paper-ripple>\n          [[_initials]]\n        </a>\n      </template>\n    </app-toolbar>\n\n    <paper-listbox attr-for-selected=\"data-panel\" selected=\"[[hass.panelUrl]]\">\n      <a href='[[_computeUrl(defaultPage)]]' data-panel$=\"[[defaultPage]]\" tabindex=\"-1\">\n        <paper-icon-item>\n          <ha-icon slot=\"item-icon\" icon=\"hass:apps\"></ha-icon>\n          <span class=\"item-text\">[[localize('panel.states')]]</span>\n        </paper-icon-item>\n      </a>\n\n      <template is=\"dom-repeat\" items=\"[[panels]]\">\n        <a href='[[_computeUrl(item.url_path)]]' data-panel$='[[item.url_path]]' tabindex=\"-1\">\n          <paper-icon-item>\n            <ha-icon slot=\"item-icon\" icon=\"[[item.icon]]\"></ha-icon>\n            <span class=\"item-text\">[[_computePanelName(localize, item)]]</span>\n          </paper-icon-item>\n        </a>\n      </template>\n\n      <template is='dom-if' if='[[!hass.user]]'>\n        <paper-icon-item on-click='_handleLogOut' class=\"logout\">\n          <ha-icon slot=\"item-icon\" icon=\"hass:exit-to-app\"></ha-icon>\n          <span class=\"item-text\">[[localize('ui.sidebar.log_out')]]</span>\n        </paper-icon-item>\n      </template>\n    </paper-listbox>\n\n    <div>\n      <div class=\"divider\"></div>\n\n      <div class=\"subheader\">[[localize('ui.sidebar.developer_tools')]]</div>\n\n      <div class=\"dev-tools layout horizontal justified\">\n        <a href=\"/dev-service\" tabindex=\"-1\">\n          <paper-icon-button\n            icon=\"hass:remote\"\n            alt=\"[[localize('panel.dev-services')]]\"\n            title=\"[[localize('panel.dev-services')]]\"\n          ></paper-icon-button>\n        </a>\n        <a href=\"/dev-state\" tabindex=\"-1\">\n          <paper-icon-button\n            icon=\"hass:code-tags\"\n            alt=\"[[localize('panel.dev-states')]]\"\n            title=\"[[localize('panel.dev-states')]]\"\n\n          ></paper-icon-button>\n        </a>\n        <a href=\"/dev-event\" tabindex=\"-1\">\n          <paper-icon-button\n            icon=\"hass:radio-tower\"\n            alt=\"[[localize('panel.dev-events')]]\"\n            title=\"[[localize('panel.dev-events')]]\"\n\n          ></paper-icon-button>\n        </a>\n        <a href=\"/dev-template\" tabindex=\"-1\">\n          <paper-icon-button\n            icon=\"hass:file-xml\"\n            alt=\"[[localize('panel.dev-templates')]]\"\n            title=\"[[localize('panel.dev-templates')]]\"\n\n          ></paper-icon-button>\n          </a>\n        <template is=\"dom-if\" if=\"[[_mqttLoaded(hass)]]\">\n          <a href=\"/dev-mqtt\" tabindex=\"-1\">\n            <paper-icon-button\n              icon=\"hass:altimeter\"\n              alt=\"[[localize('panel.dev-mqtt')]]\"\n              title=\"[[localize('panel.dev-mqtt')]]\"\n\n            ></paper-icon-button>\n          </a>\n        </template>\n        <a href=\"/dev-info\" tabindex=\"-1\">\n          <paper-icon-button\n            icon=\"hass:information-outline\"\n            alt=\"[[localize('panel.dev-info')]]\"\n            title=\"[[localize('panel.dev-info')]]\"\n          ></paper-icon-button>\n        </a>\n      </div>\n    </div>\n"]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var HaSidebar=function(_LocalizeMixin){_inherits(HaSidebar,_LocalizeMixin);function HaSidebar(){_classCallCheck(this,HaSidebar);return _possibleConstructorReturn(this,_getPrototypeOf(HaSidebar).apply(this,arguments))}_createClass(HaSidebar,[{key:"_computeUserInitials",value:function(name){if(!name)return"user";return name.trim().split(" ").slice(0,3).map(function(s){return s.substr(0,1)}).join("")}},{key:"_computeBadgeClass",value:function(initials){return"profile-badge ".concat(2<initials.length?"long":"")}},{key:"_mqttLoaded",value:function(hass){return Object(_common_config_is_component_loaded_js__WEBPACK_IMPORTED_MODULE_11__.a)(hass,"mqtt")}},{key:"_computeUserName",value:function(user){return user&&(user.name||"Unnamed User")}},{key:"_computePanelName",value:function(localize,panel){return localize("panel.".concat(panel.title))||panel.title}},{key:"computePanels",value:function(hass){var panels=hass.panels,sortValue={map:1,logbook:2,history:3},result=[];Object.keys(panels).forEach(function(key){if(panels[key].title){result.push(panels[key])}});result.sort(function(a,b){var aBuiltIn=a.component_name in sortValue,bBuiltIn=b.component_name in sortValue;if(aBuiltIn&&bBuiltIn){return sortValue[a.component_name]-sortValue[b.component_name]}if(aBuiltIn){return-1}if(bBuiltIn){return 1}if(a.title<b.title){return-1}if(a.title>b.title){return 1}return 0});return result}},{key:"_computeUrl",value:function(urlPath){return"/".concat(urlPath)}},{key:"_handleLogOut",value:function(){this.fire("hass-logout")}}],[{key:"template",get:function(){return Object(_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_6__.a)(_templateObject())}},{key:"properties",get:function(){return{hass:{type:Object},menuShown:{type:Boolean},menuSelected:{type:String},narrow:Boolean,panels:{type:Array,computed:"computePanels(hass)"},defaultPage:String,_initials:{type:String,computed:"_computeUserInitials(hass.user.name)"}}}}]);return HaSidebar}(Object(_mixins_localize_mixin_js__WEBPACK_IMPORTED_MODULE_10__.a)(_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_7__.a));customElements.define("ha-sidebar",HaSidebar)}}]);
//# sourceMappingURL=911fffbfafd5a02785ec.chunk.js.map
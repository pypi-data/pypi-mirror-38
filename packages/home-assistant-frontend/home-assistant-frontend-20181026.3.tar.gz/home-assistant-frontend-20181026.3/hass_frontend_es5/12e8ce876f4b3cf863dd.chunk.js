(window.webpackJsonp=window.webpackJsonp||[]).push([[39],{665:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_paper_card_paper_card_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(143),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(0),_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(4),_common_auth_token_storage_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(80),_mixins_localize_mixin_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(9),_resources_ha_style_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(121);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n      <style include='ha-style'>\n        paper-card {\n          position: fixed;\n          padding: 8px 0;\n          bottom: 16px;\n          right: 16px;\n        }\n\n        .card-actions {\n          text-align: right;\n          border-top: 0;\n          margin-right: -4px;\n        }\n\n        :host(.small) paper-card {\n          bottom: 0;\n          left: 0;\n          right: 0;\n        }\n      </style>\n      <paper-card elevation=\"4\">\n        <div class='card-content'>\n          [[localize('ui.auth_store.ask')]]\n        </div>\n        <div class='card-actions'>\n          <paper-button on-click='_done'>[[localize('ui.auth_store.decline')]]</paper-button>\n          <paper-button primary on-click='_save'>[[localize('ui.auth_store.confirm')]]</paper-button>\n        </div>\n      </paper-card>\n    "]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _get(target,property,receiver){if("undefined"!==typeof Reflect&&Reflect.get){_get=Reflect.get}else{_get=function(target,property,receiver){var base=_superPropBase(target,property);if(!base)return;var desc=Object.getOwnPropertyDescriptor(base,property);if(desc.get){return desc.get.call(receiver)}return desc.value}}return _get(target,property,receiver||target)}function _superPropBase(object,property){while(!Object.prototype.hasOwnProperty.call(object,property)){object=_getPrototypeOf(object);if(null===object)break}return object}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var HaStoreAuth=function(_LocalizeMixin){_inherits(HaStoreAuth,_LocalizeMixin);function HaStoreAuth(){_classCallCheck(this,HaStoreAuth);return _possibleConstructorReturn(this,_getPrototypeOf(HaStoreAuth).apply(this,arguments))}_createClass(HaStoreAuth,[{key:"ready",value:function(){_get(_getPrototypeOf(HaStoreAuth.prototype),"ready",this).call(this);this.classList.toggle("small",600>window.innerWidth)}},{key:"_save",value:function(){Object(_common_auth_token_storage_js__WEBPACK_IMPORTED_MODULE_3__.b)();this._done()}},{key:"_done",value:function(){var _this=this,card=this.shadowRoot.querySelector("paper-card");card.style.transition="bottom .25s";card.style.bottom="-".concat(card.offsetHeight+8,"px");setTimeout(function(){return _this.parentNode.removeChild(_this)},300)}}],[{key:"template",get:function(){return Object(_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_1__.a)(_templateObject())}},{key:"properties",get:function(){return{hass:Object}}}]);return HaStoreAuth}(Object(_mixins_localize_mixin_js__WEBPACK_IMPORTED_MODULE_4__.a)(_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_2__.a));customElements.define("ha-store-auth-card",HaStoreAuth)}}]);
//# sourceMappingURL=12e8ce876f4b3cf863dd.chunk.js.map
(window.webpackJsonp=window.webpackJsonp||[]).push([[42],{335:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var iron_a11y_announcer=__webpack_require__(71),iron_overlay_behavior=__webpack_require__(53),polymer_fn=__webpack_require__(3),html_tag=__webpack_require__(0),polymer_legacy=__webpack_require__(2);function _templateObject(){var data=_taggedTemplateLiteral(["\n    <style>\n      :host {\n        display: block;\n        position: fixed;\n        background-color: var(--paper-toast-background-color, #323232);\n        color: var(--paper-toast-color, #f1f1f1);\n        min-height: 48px;\n        min-width: 288px;\n        padding: 16px 24px;\n        box-sizing: border-box;\n        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.26);\n        border-radius: 2px;\n        margin: 12px;\n        font-size: 14px;\n        cursor: default;\n        -webkit-transition: -webkit-transform 0.3s, opacity 0.3s;\n        transition: transform 0.3s, opacity 0.3s;\n        opacity: 0;\n        -webkit-transform: translateY(100px);\n        transform: translateY(100px);\n        @apply --paper-font-common-base;\n      }\n\n      :host(.capsule) {\n        border-radius: 24px;\n      }\n\n      :host(.fit-bottom) {\n        width: 100%;\n        min-width: 0;\n        border-radius: 0;\n        margin: 0;\n      }\n\n      :host(.paper-toast-open) {\n        opacity: 1;\n        -webkit-transform: translateY(0px);\n        transform: translateY(0px);\n      }\n    </style>\n\n    <span id=\"label\">{{text}}</span>\n    <slot></slot>\n"]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/var currentToast=null;Object(polymer_fn.a)({_template:Object(html_tag.a)(_templateObject()),is:"paper-toast",behaviors:[iron_overlay_behavior.a],properties:{fitInto:{type:Object,value:window,observer:"_onFitIntoChanged"},horizontalAlign:{type:String,value:"left"},verticalAlign:{type:String,value:"bottom"},duration:{type:Number,value:3e3},text:{type:String,value:""},noCancelOnOutsideClick:{type:Boolean,value:!0},noAutoFocus:{type:Boolean,value:!0}},listeners:{transitionend:"__onTransitionEnd"},get visible(){polymer_legacy.a._warn("`visible` is deprecated, use `opened` instead");return this.opened},get _canAutoClose(){return 0<this.duration&&this.duration!==Infinity},created:function(){this._autoClose=null;iron_a11y_announcer.a.requestAvailability()},show:function(properties){if("string"==typeof properties){properties={text:properties}}for(var property in properties){if(0===property.indexOf("_")){polymer_legacy.a._warn("The property \""+property+"\" is private and was not set.")}else if(property in this){this[property]=properties[property]}else{polymer_legacy.a._warn("The property \""+property+"\" is not valid.")}}this.open()},hide:function(){this.close()},__onTransitionEnd:function(e){if(e&&e.target===this&&"opacity"===e.propertyName){if(this.opened){this._finishRenderOpened()}else{this._finishRenderClosed()}}},_openedChanged:function(){if(null!==this._autoClose){this.cancelAsync(this._autoClose);this._autoClose=null}if(this.opened){if(currentToast&&currentToast!==this){currentToast.close()}currentToast=this;this.fire("iron-announce",{text:this.text});if(this._canAutoClose){this._autoClose=this.async(this.close,this.duration)}}else if(currentToast===this){currentToast=null}iron_overlay_behavior.b._openedChanged.apply(this,arguments)},_renderOpened:function(){this.classList.add("paper-toast-open")},_renderClosed:function(){this.classList.remove("paper-toast-open")},_onFitIntoChanged:function(fitInto){this.positionTarget=fitInto}});function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _get(target,property,receiver){if("undefined"!==typeof Reflect&&Reflect.get){_get=Reflect.get}else{_get=function(target,property,receiver){var base=_superPropBase(target,property);if(!base)return;var desc=Object.getOwnPropertyDescriptor(base,property);if(desc.get){return desc.get.call(receiver)}return desc.value}}return _get(target,property,receiver||target)}function _superPropBase(object,property){while(!Object.prototype.hasOwnProperty.call(object,property)){object=_getPrototypeOf(object);if(null===object)break}return object}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var PaperToast=customElements.get("paper-toast"),HaToast=function(_PaperToast){_inherits(HaToast,_PaperToast);function HaToast(){_classCallCheck(this,HaToast);return _possibleConstructorReturn(this,_getPrototypeOf(HaToast).apply(this,arguments))}_createClass(HaToast,[{key:"connectedCallback",value:function(){var _this=this;_get(_getPrototypeOf(HaToast.prototype),"connectedCallback",this).call(this);if(!this._resizeListener){this._resizeListener=function(ev){return _this.classList.toggle("fit-bottom",ev.matches)};this._mediaq=window.matchMedia("(max-width: 599px")}this._mediaq.addListener(this._resizeListener);this._resizeListener(this._mediaq)}},{key:"disconnectedCallback",value:function(){_get(_getPrototypeOf(HaToast.prototype),"disconnectedCallback",this).call(this);this._mediaq.removeListener(this._resizeListener)}}]);return HaToast}(PaperToast);customElements.define("ha-toast",HaToast)}}]);
//# sourceMappingURL=1451f706ba29a8f6d646.chunk.js.map
(window.webpackJsonp=window.webpackJsonp||[]).push([[16],{161:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"b",function(){return PaperDialogBehaviorImpl});__webpack_require__.d(__webpack_exports__,"a",function(){return PaperDialogBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(53),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(1),PaperDialogBehaviorImpl={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.__readied=!0},_modalChanged:function(modal,readied){if(!readied){return}if(modal){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.noCancelOnOutsideClick=!0;this.noCancelOnEscKey=!0;this.withBackdrop=!0}else{this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick;this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey;this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop}},_updateClosingReasonConfirmed:function(confirmed){this.closingReason=this.closingReason||{};this.closingReason.confirmed=confirmed},_onDialogClick:function(event){for(var path=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(event).path,i=0,l=path.indexOf(this),target;i<l;i++){target=path[i];if(target.hasAttribute&&(target.hasAttribute("dialog-dismiss")||target.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(target.hasAttribute("dialog-confirm"));this.close();event.stopPropagation();break}}}},PaperDialogBehavior=[_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__.a,PaperDialogBehaviorImpl];/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/},165:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(26),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(30),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(42),_polymer_paper_styles_shadow_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(63),$_documentContainer=document.createElement("template");/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML="<dom-module id=\"paper-dialog-shared-styles\">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>";document.head.appendChild($_documentContainer.content)},283:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_lib_utils_mixin_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(6),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(161),_polymer_polymer_lib_legacy_class_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(55),_events_mixin__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(14);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}__webpack_exports__.a=Object(_polymer_polymer_lib_utils_mixin_js__WEBPACK_IMPORTED_MODULE_0__.a)(function(superClass){return function(_mixinBehaviors){_inherits(_class,_mixinBehaviors);function _class(){_classCallCheck(this,_class);return _possibleConstructorReturn(this,_getPrototypeOf(_class).apply(this,arguments))}_createClass(_class,null,[{key:"properties",get:function(){return{withBackdrop:{type:Boolean,value:!0}}}}]);return _class}(Object(_polymer_polymer_lib_legacy_class_js__WEBPACK_IMPORTED_MODULE_2__.b)([_events_mixin__WEBPACK_IMPORTED_MODULE_3__.a,_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_1__.a],superClass))})},649:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_iron_icon_iron_icon_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(75),_polymer_paper_dialog_behavior_paper_dialog_shared_styles_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(165),_polymer_paper_icon_button_paper_icon_button_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(62),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(0),_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(4),_mixins_dialog_mixin_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(283);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n    <style include=\"paper-dialog-shared-styles\">\n      iron-icon {\n        margin-right: 8px;\n      }\n\n      .content {\n        width: 450px;\n        min-height: 80px;\n        font-size: 18px;\n        padding: 16px;\n      }\n\n      .messages {\n        max-height: 50vh;\n        overflow: auto;\n      }\n\n      .messages::after {\n        content: \"\";\n        clear: both;\n        display: block;\n      }\n\n      .message {\n        clear: both;\n        margin: 8px 0;\n        padding: 8px;\n        border-radius: 15px;\n      }\n\n      .message.user {\n        margin-left: 24px;\n        float: right;\n        text-align: right;\n        border-bottom-right-radius: 0px;\n        background-color: var(--light-primary-color);\n        color: var(--primary-text-color);\n      }\n\n      .message.hass {\n        margin-right: 24px;\n        float: left;\n        border-bottom-left-radius: 0px;\n        background-color: var(--primary-color);\n        color: var(--text-primary-color);\n      }\n\n      .message.error {\n        background-color: var(--google-red-500);\n        color: var(--text-primary-color);\n      }\n\n      .icon {\n        text-align: center;\n      }\n\n      .icon paper-icon-button {\n        height: 52px;\n        width: 52px;\n      }\n\n      .interimTranscript {\n        color: darkgrey;\n      }\n\n      [hidden] {\n        display: none;\n      }\n\n      :host {\n        border-radius: 2px;\n      }\n\n      @media all and (max-width: 450px) {\n        :host {\n          margin: 0;\n          width: 100%;\n          max-height: calc(100% - 64px);\n\n          position: fixed !important;\n          bottom: 0px;\n          left: 0px;\n          right: 0px;\n          overflow: scroll;\n          border-bottom-left-radius: 0px;\n          border-bottom-right-radius: 0px;\n        }\n\n        .content {\n          width: auto;\n        }\n\n        .messages {\n          max-height: 68vh;\n        }\n      }\n    </style>\n\n    <div class=\"content\">\n      <div class=\"messages\" id=\"messages\">\n        <template is=\"dom-repeat\" items=\"[[_conversation]]\" as=\"message\">\n          <div class$=\"[[_computeMessageClasses(message)]]\">[[message.text]]</div>\n        </template>\n      </div>\n      <template is=\"dom-if\" if=\"[[results]]\">\n        <div class=\"messages\">\n          <div class=\"message user\">\n            <span>{{results.final}}</span>\n            <span class=\"interimTranscript\">[[results.interim]]</span>\n            \u2026\n          </div>\n        </div>\n      </template>\n      <div class=\"icon\" hidden$=\"[[results]]\">\n        <paper-icon-button icon=\"hass:text-to-speech\" on-click=\"startListening\"></paper-icon-button>\n      </div>\n    </div>\n"]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var HaVoiceCommandDialog=function(_DialogMixin){_inherits(HaVoiceCommandDialog,_DialogMixin);function HaVoiceCommandDialog(){_classCallCheck(this,HaVoiceCommandDialog);return _possibleConstructorReturn(this,_getPrototypeOf(HaVoiceCommandDialog).apply(this,arguments))}_createClass(HaVoiceCommandDialog,[{key:"initRecognition",value:function(){this.recognition=new webkitSpeechRecognition;this.recognition.onstart=function(){this.results={final:"",interim:""}}.bind(this);this.recognition.onerror=function(){this.recognition.abort();var text=this.results.final||this.results.interim;this.results=null;if(""===text){text="<Home Assistant did not hear anything>"}this.push("_conversation",{who:"user",text:text,error:!0})}.bind(this);this.recognition.onend=function(){if(null==this.results){return}var text=this.results.final||this.results.interim;this.results=null;this.push("_conversation",{who:"user",text:text});this.hass.callApi("post","conversation/process",{text:text}).then(function(response){this.push("_conversation",{who:"hass",text:response.speech.plain.speech})}.bind(this),function(){this.set(["_conversation",this._conversation.length-1,"error"],!0)}.bind(this))}.bind(this);this.recognition.onresult=function(event){for(var oldResults=this.results,finalTranscript="",interimTranscript="",ind=event.resultIndex;ind<event.results.length;ind++){if(event.results[ind].isFinal){finalTranscript+=event.results[ind][0].transcript}else{interimTranscript+=event.results[ind][0].transcript}}this.results={interim:interimTranscript,final:oldResults.final+finalTranscript}}.bind(this)}},{key:"startListening",value:function(){if(!this.recognition){this.initRecognition()}this.results={interim:"",final:""};this.recognition.start()}},{key:"_scrollMessagesBottom",value:function(){var _this=this;setTimeout(function(){_this.$.messages.scrollTop=_this.$.messages.scrollHeight;if(0!==_this.$.messages.scrollTop){_this.$.dialog.fire("iron-resize")}},10)}},{key:"dialogOpenChanged",value:function(newVal){if(newVal){this.startListening()}else if(!newVal&&this.results){this.recognition.abort()}}},{key:"_computeMessageClasses",value:function(message){return"message "+message.who+(message.error?" error":"")}}],[{key:"template",get:function(){return Object(_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_3__.a)(_templateObject())}},{key:"properties",get:function(){return{hass:Object,results:{type:Object,value:null,observer:"_scrollMessagesBottom"},_conversation:{type:Array,value:function(){return[{who:"hass",text:"How can I help?"}]},observer:"_scrollMessagesBottom"}}}},{key:"observers",get:function(){return["dialogOpenChanged(opened)"]}}]);return HaVoiceCommandDialog}(Object(_mixins_dialog_mixin_js__WEBPACK_IMPORTED_MODULE_5__.a)(_polymer_polymer_polymer_element_js__WEBPACK_IMPORTED_MODULE_4__.a));customElements.define("ha-voice-command-dialog",HaVoiceCommandDialog)}}]);
//# sourceMappingURL=3e3d64d61e90046a0f3c.chunk.js.map
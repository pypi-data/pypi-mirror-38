(window.webpackJsonp=window.webpackJsonp||[]).push([[44],{259:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"default",function(){return ExternalAuth});var home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(21);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function asyncGeneratorStep(gen,resolve,reject,_next,_throw,key,arg){try{var info=gen[key](arg),value=info.value}catch(error){reject(error);return}if(info.done){resolve(value)}else{Promise.resolve(value).then(_next,_throw)}}function _asyncToGenerator(fn){return function(){var self=this,args=arguments;return new Promise(function(resolve,reject){var gen=fn.apply(self,args);function _next(value){asyncGeneratorStep(gen,resolve,reject,_next,_throw,"next",value)}function _throw(err){asyncGeneratorStep(gen,resolve,reject,_next,_throw,"throw",err)}_next(void 0)})}}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var CALLBACK_SET_TOKEN="externalAuthSetToken",CALLBACK_REVOKE_TOKEN="externalAuthRevokeToken";if(!window.externalApp&&!window.webkit){throw new Error("External auth requires either externalApp or webkit defined on Window object.")}var ExternalAuth=function(_Auth){_inherits(ExternalAuth,_Auth);function ExternalAuth(hassUrl){var _this;_classCallCheck(this,ExternalAuth);_this=_possibleConstructorReturn(this,_getPrototypeOf(ExternalAuth).call(this));_this.data={hassUrl:hassUrl,access_token:"",expires:0};return _this}_createClass(ExternalAuth,[{key:"refreshAccessToken",value:function(){var _refreshAccessToken=_asyncToGenerator(regeneratorRuntime.mark(function _callee(){var responseProm,callbackPayload,tokens;return regeneratorRuntime.wrap(function(_context){while(1){switch(_context.prev=_context.next){case 0:responseProm=new Promise(function(resolve,reject){window[CALLBACK_SET_TOKEN]=function(success,data){return success?resolve(data):reject(data)}});_context.next=3;return 0;case 3:callbackPayload={callback:CALLBACK_SET_TOKEN};if(window.externalApp){window.externalApp.getExternalAuth(callbackPayload)}else{window.webkit.messageHandlers.getExternalAuth.postMessage(callbackPayload)}_context.next=7;return responseProm;case 7:tokens=_context.sent;this.data.access_token=tokens.access_token;this.data.expires=1e3*tokens.expires_in+Date.now();case 10:case"end":return _context.stop();}}},_callee,this)}));return function(){return _refreshAccessToken.apply(this,arguments)}}()},{key:"revoke",value:function(){var _revoke=_asyncToGenerator(regeneratorRuntime.mark(function _callee2(){var responseProm,callbackPayload;return regeneratorRuntime.wrap(function(_context2){while(1){switch(_context2.prev=_context2.next){case 0:responseProm=new Promise(function(resolve,reject){window[CALLBACK_REVOKE_TOKEN]=function(success,data){return success?resolve(data):reject(data)}});_context2.next=3;return 0;case 3:callbackPayload={callback:CALLBACK_REVOKE_TOKEN};if(window.externalApp){window.externalApp.revokeExternalAuth(callbackPayload)}else{window.webkit.messageHandlers.revokeExternalAuth.postMessage(callbackPayload)}_context2.next=7;return responseProm;case 7:case"end":return _context2.stop();}}},_callee2,this)}));return function(){return _revoke.apply(this,arguments)}}()}]);return ExternalAuth}(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.a)}}]);
//# sourceMappingURL=6430762a4faef5ae6b6c.chunk.js.map
(function(modules){function webpackJsonpCallback(data){var chunkIds=data[0],moreModules=data[1],moduleId,chunkId,i=0,resolves=[];for(;i<chunkIds.length;i++){chunkId=chunkIds[i];if(installedChunks[chunkId]){resolves.push(installedChunks[chunkId][0])}installedChunks[chunkId]=0}for(moduleId in moreModules){if(Object.prototype.hasOwnProperty.call(moreModules,moduleId)){modules[moduleId]=moreModules[moduleId]}}if(parentJsonpFunction)parentJsonpFunction(data);while(resolves.length){resolves.shift()()}}var installedModules={},installedChunks={11:0};function jsonpScriptSrc(chunkId){return __webpack_require__.p+""+{44:"4bab686f269e1936731e"}[chunkId]+".chunk.js"}function __webpack_require__(moduleId){if(installedModules[moduleId]){return installedModules[moduleId].exports}var module=installedModules[moduleId]={i:moduleId,l:!1,exports:{}};modules[moduleId].call(module.exports,module,module.exports,__webpack_require__);module.l=!0;return module.exports}__webpack_require__.e=function(chunkId){var promises=[],installedChunkData=installedChunks[chunkId];if(0!==installedChunkData){if(installedChunkData){promises.push(installedChunkData[2])}else{var promise=new Promise(function(resolve,reject){installedChunkData=installedChunks[chunkId]=[resolve,reject]});promises.push(installedChunkData[2]=promise);var head=document.getElementsByTagName("head")[0],script=document.createElement("script"),onScriptComplete;script.charset="utf-8";script.timeout=120;if(__webpack_require__.nc){script.setAttribute("nonce",__webpack_require__.nc)}script.src=jsonpScriptSrc(chunkId);onScriptComplete=function(event){script.onerror=script.onload=null;clearTimeout(timeout);var chunk=installedChunks[chunkId];if(0!==chunk){if(chunk){var errorType=event&&("load"===event.type?"missing":event.type),realSrc=event&&event.target&&event.target.src,error=new Error("Loading chunk "+chunkId+" failed.\n("+errorType+": "+realSrc+")");error.type=errorType;error.request=realSrc;chunk[1](error)}installedChunks[chunkId]=void 0}};var timeout=setTimeout(function(){onScriptComplete({type:"timeout",target:script})},12e4);script.onerror=script.onload=onScriptComplete;head.appendChild(script)}}return Promise.all(promises)};__webpack_require__.m=modules;__webpack_require__.c=installedModules;__webpack_require__.d=function(exports,name,getter){if(!__webpack_require__.o(exports,name)){Object.defineProperty(exports,name,{enumerable:!0,get:getter})}};__webpack_require__.r=function(exports){if("undefined"!==typeof Symbol&&Symbol.toStringTag){Object.defineProperty(exports,Symbol.toStringTag,{value:"Module"})}Object.defineProperty(exports,"__esModule",{value:!0})};__webpack_require__.t=function(value,mode){if(1&mode)value=__webpack_require__(value);if(8&mode)return value;if(4&mode&&"object"===typeof value&&value&&value.__esModule)return value;var ns=Object.create(null);__webpack_require__.r(ns);Object.defineProperty(ns,"default",{enumerable:!0,value:value});if(2&mode&&"string"!=typeof value)for(var key in value)__webpack_require__.d(ns,key,function(key){return value[key]}.bind(null,key));return ns};__webpack_require__.n=function(module){var getter=module&&module.__esModule?function(){return module["default"]}:function(){return module};__webpack_require__.d(getter,"a",getter);return getter};__webpack_require__.o=function(object,property){return Object.prototype.hasOwnProperty.call(object,property)};__webpack_require__.p="/frontend_es5/";__webpack_require__.oe=function(err){console.error(err);throw err};var jsonpArray=window.webpackJsonp=window.webpackJsonp||[],oldJsonpFunction=jsonpArray.push.bind(jsonpArray);jsonpArray.push=webpackJsonpCallback;jsonpArray=jsonpArray.slice();for(var i=0;i<jsonpArray.length;i++)webpackJsonpCallback(jsonpArray[i]);var parentJsonpFunction=oldJsonpFunction;return __webpack_require__(__webpack_require__.s=186)})({104:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return subscribeUser});var home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(22),subscribeUser=function(conn,onChange){return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.d)("_usr",function(conn_){return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.g)(conn_)},null,conn,onChange)}},105:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return subscribeThemes});var home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(22),fetchThemes=function(conn){return conn.sendMessagePromise({type:"frontend/get_themes"})},subscribeUpdates=function(conn,store){return conn.subscribeEvents(function(event){return store.setState(event.data,!0)},"themes_updated")},subscribeThemes=function(conn,onChange){return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.d)("_thm",fetchThemes,subscribeUpdates,conn,onChange)}},106:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return subscribePanels});var home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(22),subscribePanels=function(conn,onChange){return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.d)("_pnl",function(conn_){return conn_.sendMessagePromise({type:"get_panels"})},null,conn,onChange)}},186:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(22),_common_auth_token_storage__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(81),_data_ws_panels__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(106),_data_ws_themes__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(105),_data_ws_user__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(104);function asyncGeneratorStep(gen,resolve,reject,_next,_throw,key,arg){try{var info=gen[key](arg),value=info.value}catch(error){reject(error);return}if(info.done){resolve(value)}else{Promise.resolve(value).then(_next,_throw)}}function _asyncToGenerator(fn){return function(){var self=this,args=arguments;return new Promise(function(resolve,reject){var gen=fn.apply(self,args);function _next(value){asyncGeneratorStep(gen,resolve,reject,_next,_throw,"next",value)}function _throw(err){asyncGeneratorStep(gen,resolve,reject,_next,_throw,"throw",err)}_next(void 0)})}}var hassUrl="".concat(location.protocol,"//").concat(location.host),isExternal=location.search.includes("external_auth=1"),authProm=isExternal?function(){return __webpack_require__.e(44).then(__webpack_require__.bind(null,192)).then(function(mod){return new mod.default(hassUrl)})}:function(){return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.f)({hassUrl:hassUrl,saveTokens:_common_auth_token_storage__WEBPACK_IMPORTED_MODULE_1__.d,loadTokens:function(){return Promise.resolve(Object(_common_auth_token_storage__WEBPACK_IMPORTED_MODULE_1__.c)())}})},connProm=function(){var _ref=_asyncToGenerator(regeneratorRuntime.mark(function _callee(auth){var conn,_conn;return regeneratorRuntime.wrap(function(_context){while(1){switch(_context.prev=_context.next){case 0:_context.prev=0;_context.next=3;return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.e)({auth:auth});case 3:conn=_context.sent;if(location.search.includes("auth_callback=1")){history.replaceState(null,null,location.pathname)}return _context.abrupt("return",{auth:auth,conn:conn});case 8:_context.prev=8;_context.t0=_context["catch"](0);if(!(_context.t0!==home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.b)){_context.next=12;break}throw _context.t0;case 12:if(!isExternal)Object(_common_auth_token_storage__WEBPACK_IMPORTED_MODULE_1__.d)(null);_context.next=15;return authProm();case 15:auth=_context.sent;_context.next=18;return Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.e)({auth:auth});case 18:_conn=_context.sent;return _context.abrupt("return",{auth:auth,conn:_conn});case 20:case"end":return _context.stop();}}},_callee,this,[[0,8]])}));return function(){return _ref.apply(this,arguments)}}();window.hassConnection=authProm().then(connProm);window.hassConnection.then(function(_ref2){var conn=_ref2.conn,noop=function(){};Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.i)(conn,noop);Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.h)(conn,noop);Object(home_assistant_js_websocket__WEBPACK_IMPORTED_MODULE_0__.j)(conn,noop);Object(_data_ws_panels__WEBPACK_IMPORTED_MODULE_2__.a)(conn,noop);Object(_data_ws_themes__WEBPACK_IMPORTED_MODULE_3__.a)(conn,noop);Object(_data_ws_user__WEBPACK_IMPORTED_MODULE_4__.a)(conn,noop)});window.addEventListener("error",function(e){var homeAssistant=document.querySelector("home-assistant");if(homeAssistant&&homeAssistant.hass&&homeAssistant.hass.callService){homeAssistant.hass.callService("system_log","write",{logger:"frontend.".concat("js",".").concat("es5",".").concat("20181103.0".replace(".","")),message:"".concat(e.filename,":").concat(e.lineno,":").concat(e.colno," ").concat(e.message)})}})},22:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"e",function(){return M});__webpack_require__.d(__webpack_exports__,"a",function(){return l});__webpack_require__.d(__webpack_exports__,"f",function(){return d});__webpack_require__.d(__webpack_exports__,"d",function(){return v});__webpack_require__.d(__webpack_exports__,"h",function(){return E});__webpack_require__.d(__webpack_exports__,"j",function(){return P});__webpack_require__.d(__webpack_exports__,"i",function(){return I});__webpack_require__.d(__webpack_exports__,"b",function(){return r});__webpack_require__.d(__webpack_exports__,"g",function(){return y});__webpack_require__.d(__webpack_exports__,"c",function(){return k});function e(e,t,n,r){return new(n||(n=Promise))(function(s,i){function o(e){try{a(r.next(e))}catch(e){i(e)}}function c(e){try{a(r.throw(e))}catch(e){i(e)}}function a(e){e.done?s(e.value):new n(function(t){t(e.value)}).then(o,c)}a((r=r.apply(e,t||[])).next())})}function t(e,t){var n,r,s,i,o={label:0,sent:function(){if(1&s[0])throw s[1];return s[1]},trys:[],ops:[]};return i={next:c(0),throw:c(1),return:c(2)},"function"==typeof Symbol&&(i[Symbol.iterator]=function(){return this}),i;function c(i){return function(c){return function(i){if(n)throw new TypeError("Generator is already executing.");for(;o;){try{if(n=1,r&&(s=2&i[0]?r.return:i[0]?r.throw||((s=r.return)&&s.call(r),0):r.next)&&!(s=s.call(r,i[1])).done)return s;switch(r=0,s&&(i=[2&i[0],s.value]),i[0]){case 0:case 1:s=i;break;case 4:return o.label++,{value:i[1],done:!1};case 5:o.label++,r=i[1],i=[0];continue;case 7:i=o.ops.pop(),o.trys.pop();continue;default:if(!(s=0<(s=o.trys).length&&s[s.length-1])&&(6===i[0]||2===i[0])){o=0;continue}if(3===i[0]&&(!s||i[1]>s[0]&&i[1]<s[3])){o.label=i[1];break}if(6===i[0]&&o.label<s[1]){o.label=s[1],s=i;break}if(s&&o.label<s[2]){o.label=s[2],o.ops.push(i);break}s[2]&&o.ops.pop(),o.trys.pop();continue;}i=t.call(e,o)}catch(e){i=[6,e],r=0}finally{n=s=0}}if(5&i[0])throw i[1];return{value:i[0]?i[1]:void 0,done:!0}}([i,c])}}}var r=2,i=4,a=function(){function n(e,t){this.options=t,this.commandId=1,this.commands={},this.eventListeners={},this.closeRequested=!1,this.setSocket(e)}return n.prototype.setSocket=function(e){var t=this,n=this.socket;if(this.socket=e,e.addEventListener("message",function(e){return t._handleMessage(e)}),e.addEventListener("close",function(e){return t._handleClose(e)}),n){var r=this.commands;this.commandId=1,this.commands={},Object.keys(r).forEach(function(e){var n=r[e];"eventCallback"in n&&t.subscribeEvents(n.eventCallback,n.eventType).then(function(e){n.unsubscribe=e,n.resolve()})}),this.fireEvent("ready")}},n.prototype.addEventListener=function(e,t){var n=this.eventListeners[e];n||(n=this.eventListeners[e]=[]),n.push(t)},n.prototype.removeEventListener=function(e,t){var n=this.eventListeners[e];if(n){var r=n.indexOf(t);-1!==r&&n.splice(r,1)}},n.prototype.fireEvent=function(e,t){var n=this;(this.eventListeners[e]||[]).forEach(function(e){return e(n,t)})},n.prototype.close=function(){this.closeRequested=!0,this.socket.close()},n.prototype.subscribeEvents=function(n,r){return e(this,void 0,void 0,function(){var s,i,o=this;return t(this,function(c){switch(c.label){case 0:return s=this._genCmdId(),[4,new Promise(function(c,a){i=o.commands[s]={resolve:c,reject:a,eventCallback:n,eventType:r,unsubscribe:function(){return e(o,void 0,void 0,function(){return t(this,function(e){switch(e.label){case 0:return[4,this.sendMessagePromise((t=s,{type:"unsubscribe_events",subscription:t}))];case 1:return e.sent(),delete this.commands[s],[2];}var t})})}};try{o.sendMessage(function(e){var t={type:"subscribe_events"};return e&&(t.event_type=e),t}(r),s)}catch(e){}})];case 1:return c.sent(),[2,function(){return i.unsubscribe()}];}})})},n.prototype.ping=function(){return this.sendMessagePromise({type:"ping"})},n.prototype.sendMessage=function(e,t){t||(t=this._genCmdId()),e.id=t,this.socket.send(JSON.stringify(e))},n.prototype.sendMessagePromise=function(e){var t=this;return new Promise(function(n,r){var s=t._genCmdId();t.commands[s]={resolve:n,reject:r},t.sendMessage(e,s)})},n.prototype._handleMessage=function(e){var t=JSON.parse(e.data);switch(t.type){case"event":this.commands[t.id].eventCallback(t.event);break;case"result":if(t.id in this.commands){var n=this.commands[t.id];t.success?(n.resolve(t.result),"eventCallback"in n||delete this.commands[t.id]):(n.reject(t.error),delete this.commands[t.id])}break;case"pong":this.commands[t.id].resolve(),delete this.commands[t.id];}},n.prototype._handleClose=function(){var s=this;if(Object.keys(this.commands).forEach(function(e){var t=s.commands[e];"reject"in t&&t.reject({type:"result",success:!1,error:{code:3,message:"Connection lost"}})}),!this.closeRequested){this.fireEvent("disconnected");var i=Object.assign({},this.options,{setupRetry:0}),o=function o(n){setTimeout(function(){return e(s,void 0,void 0,function(){var e,s;return t(this,function(t){switch(t.label){case 0:t.label=1;case 1:return t.trys.push([1,3,,4]),[4,i.createSocket(i)];case 2:return e=t.sent(),this.setSocket(e),[3,4];case 3:return(s=t.sent())===r?this.fireEvent("reconnect-error",s):o(n+1),[3,4];case 4:return[2];}})})},1e3*Math.min(n,5))};o(0)}},n.prototype._genCmdId=function(){return++this.commandId},n}();function u(e,t,n,r){n+=(n.includes("?")?"&":"?")+"auth_callback=1",document.location.href=function(e,t,n,r){var s=e+"/auth/authorize?response_type=code&client_id="+encodeURIComponent(t)+"&redirect_uri="+encodeURIComponent(n);return r&&(s+="&state="+encodeURIComponent(r)),s}(e,t,n,r)}function h(n,s,i){return e(this,void 0,void 0,function(){var e,o,c;return t(this,function(t){switch(t.label){case 0:return(e=new FormData).append("client_id",s),Object.keys(i).forEach(function(t){e.append(t,i[t])}),[4,fetch(n+"/auth/token",{method:"POST",credentials:"same-origin",body:e})];case 1:if(!(o=t.sent()).ok)throw 400===o.status||403===o.status?r:new Error("Unable to fetch tokens");return[4,o.json()];case 2:return(c=t.sent()).hassUrl=n,c.clientId=s,c.expires=1e3*c.expires_in+Date.now(),[2,c];}})})}var l=function(){function n(e,t){this.data=e,this._saveTokens=t}return Object.defineProperty(n.prototype,"wsUrl",{get:function(){return"ws"+this.data.hassUrl.substr(4)+"/api/websocket"},enumerable:!0,configurable:!0}),Object.defineProperty(n.prototype,"accessToken",{get:function(){return this.data.access_token},enumerable:!0,configurable:!0}),Object.defineProperty(n.prototype,"expired",{get:function(){return Date.now()>this.data.expires},enumerable:!0,configurable:!0}),n.prototype.refreshAccessToken=function(){return e(this,void 0,void 0,function(){var e;return t(this,function(t){switch(t.label){case 0:return[4,h(this.data.hassUrl,this.data.clientId,{grant_type:"refresh_token",refresh_token:this.data.refresh_token})];case 1:return(e=t.sent()).refresh_token=this.data.refresh_token,this.data=e,this._saveTokens&&this._saveTokens(e),[2];}})})},n.prototype.revoke=function(){return e(this,void 0,void 0,function(){var e;return t(this,function(t){switch(t.label){case 0:return(e=new FormData).append("action","revoke"),e.append("token",this.data.refresh_token),[4,fetch(this.data.hassUrl+"/auth/token",{method:"POST",credentials:"same-origin",body:e})];case 1:return t.sent(),this._saveTokens&&this._saveTokens(null),[2];}})})},n}();function d(n){return void 0===n&&(n={}),e(this,void 0,void 0,function(){var e,r,s,o,c,a,d;return t(this,function(t){switch(t.label){case 0:if(!("auth_callback"in(r=function(e){for(var t={},n=e.split("&"),r=0;r<n.length;r++){var s=n[r].split("="),i=decodeURIComponent(s[0]),o=1<s.length?decodeURIComponent(s[1]):void 0;t[i]=o}return t}(location.search.substr(1)))))return[3,4];s=JSON.parse(atob(r.state)),t.label=1;case 1:return t.trys.push([1,3,,4]),[4,function(e,t,n){return h(e,t,{code:n,grant_type:"authorization_code"})}(s.hassUrl,s.clientId,r.code)];case 2:return e=t.sent(),n.saveTokens&&n.saveTokens(e),[3,4];case 3:return o=t.sent(),console.log("Unable to fetch access token",o),[3,4];case 4:return e||!n.loadTokens?[3,6]:[4,n.loadTokens()];case 5:e=t.sent(),t.label=6;case 6:if(e)return[2,new l(e,n.saveTokens)];if(void 0===(c=n.hassUrl))throw i;return"/"===c[c.length-1]&&(c=c.substr(0,c.length-1)),a=n.clientId||location.protocol+"//"+location.host+"/",d=n.redirectUrl||location.protocol+"//"+location.host+location.pathname+location.search,u(c,a,d,function(e){return btoa(JSON.stringify(e))}({hassUrl:c,clientId:a})),[2,new Promise(function(){})];}})})}var f=function(){function e(e){this._noSub=e,this.listeners=[]}return e.prototype.action=function(e){var t=this,n=function(e){return t.setState(e,!1)};return function(){for(var r=[],s=0;s<arguments.length;s++){r[s]=arguments[s]}var i=e.apply(void 0,[t.state].concat(r));if(null!=i)return"then"in i?i.then(n):n(i)}},e.prototype.setState=function(e,t){this.state=t?e:Object.assign({},this.state,e);for(var n=this.listeners,r=0;r<n.length;r++){n[r](this.state)}},e.prototype.subscribe=function(e){var t=this;return this.listeners.push(e),void 0!==this.state&&e(this.state),function(){t.unsubscribe(e)}},e.prototype.unsubscribe=function(e){for(var t=e,n=[],r=this.listeners,s=0;s<r.length;s++){r[s]===t?t=null:n.push(r[s])}this.listeners=n,0===n.length&&this._noSub()},e}();function v(n,r,s,i,o){var c,a=this;if(n in i)return i[n](o);var u=new f(function(){c&&c.then(function(e){return e()}),i.removeEventListener("ready",h),delete i[n]});i[n]=function(e){return u.subscribe(e)},s&&(c=s(i,u));var h=function(){return e(a,void 0,void 0,function(){var e,n,s;return t(this,function(t){switch(t.label){case 0:return t.trys.push([0,2,,3]),n=(e=u).setState,[4,r(i)];case 1:return n.apply(e,[t.sent(),!0]),[3,3];case 2:if(s=t.sent(),i.socket.readyState==i.socket.OPEN)throw s;return[3,3];case 3:return[2];}})})};return i.addEventListener("ready",h),h(),u.subscribe(o)}var p=function(e){return e.sendMessagePromise({type:"get_states"})},b=function(e){return e.sendMessagePromise({type:"get_services"})},m=function(e){return e.sendMessagePromise({type:"get_config"})},y=function(e){return e.sendMessagePromise({type:"auth/current_user"})},k=function(e,t,n,r){return e.sendMessagePromise(function(e,t,n){var r={type:"call_service",domain:e,service:t};return n&&(r.service_data=n),r}(t,n,r))};function g(e,t){return void 0===e?null:{components:e.components.concat(t.data.component)}}var _=function(e){return m(e)},w=function(e,t){return e.subscribeEvents(t.action(g),"component_loaded")},E=function(e,t){return v("_cnf",_,w,e,t)};function S(e,t){var n,r;if(void 0===e)return null;var s=t.data,i=s.domain,o=Object.assign({},e[i],((n={})[s.service]={description:"",fields:{}},n));return(r={})[i]=o,r}function O(e,t){var n;if(void 0===e)return null;var r=t.data,s=r.domain,i=r.service,o=e[s];if(!(o&&i in o))return null;var c={};return Object.keys(o).forEach(function(e){e!==i&&(c[e]=o[e])}),(n={})[s]=c,n}var T=function(e){return b(e)},L=function(e,t){return Promise.all([e.subscribeEvents(t.action(S),"service_registered"),e.subscribeEvents(t.action(O),"service_removed")]).then(function(e){return function(){return e.forEach(function(e){return e()})}})},P=function(e,t){return v("_srv",T,L,e,t)};function j(n){return e(this,void 0,void 0,function(){var e,r,s,i;return t(this,function(t){switch(t.label){case 0:return[4,p(n)];case 1:for(e=t.sent(),r={},s=0;s<e.length;s++){r[(i=e[s]).entity_id]=i}return[2,r];}})})}var C=function(e,t){return e.subscribeEvents(function(e){return function(e,t){var n,r=e.state;if(void 0!==r){var s=t.data,i=s.entity_id,o=s.new_state;if(o)e.setState(((n={})[o.entity_id]=o,n));else{var c=Object.assign({},r);delete c[i],e.setState(c,!0)}}}(t,e)},"state_changed")},I=function(e,t){return v("_ent",j,C,e,t)},U={setupRetry:0,createSocket:function(s){if(!s.auth)throw i;var a=s.auth,u=a.wsUrl;return new Promise(function(i,h){return function s(i,h,l){var d=this,f=new WebSocket(u),v=!1,p=function p(){if(f.removeEventListener("close",p),v)l(r);else if(0!==i){var e=-1===i?-1:i-1;setTimeout(function(){return s(e,h,l)},1e3)}else l(1)},b=function(){return e(d,void 0,void 0,function(){var e;return t(this,function(t){switch(t.label){case 0:return t.trys.push([0,3,,4]),a.expired?[4,a.refreshAccessToken()]:[3,2];case 1:t.sent(),t.label=2;case 2:return f.send(JSON.stringify({type:"auth",access_token:a.accessToken})),[3,4];case 3:return e=t.sent(),v=e===r,f.close(),[3,4];case 4:return[2];}})})};f.addEventListener("open",b),f.addEventListener("message",function m(n){return e(d,void 0,void 0,function(){return t(this,function(){switch(JSON.parse(n.data).type){case"auth_invalid":v=!0,f.close();break;case"auth_ok":f.removeEventListener("open",b),f.removeEventListener("message",m),f.removeEventListener("close",p),f.removeEventListener("error",p),h(f);}return[2]})})}),f.addEventListener("close",p),f.addEventListener("error",p)}(s.setupRetry,i,h)})}};function M(n){return e(this,void 0,void 0,function(){var e,r;return t(this,function(t){switch(t.label){case 0:return[4,(e=Object.assign({},U,n)).createSocket(e)];case 1:return r=t.sent(),[2,new a(r,e)];}})})}},81:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return askWrite});__webpack_require__.d(__webpack_exports__,"d",function(){return saveTokens});__webpack_require__.d(__webpack_exports__,"b",function(){return enableWrite});__webpack_require__.d(__webpack_exports__,"c",function(){return loadTokens});var storage=window.localStorage||{},tokenCache=window.__tokenCache;if(!tokenCache){tokenCache=window.__tokenCache={tokens:void 0,writeEnabled:void 0}}function askWrite(){return tokenCache.tokens!==void 0&&tokenCache.writeEnabled===void 0}function saveTokens(tokens){tokenCache.tokens=tokens;if(tokenCache.writeEnabled){try{storage.hassTokens=JSON.stringify(tokens)}catch(err){}}}function enableWrite(){tokenCache.writeEnabled=!0;saveTokens(tokenCache.tokens)}function loadTokens(){if(tokenCache.tokens===void 0){try{delete storage.tokens;var tokens=storage.hassTokens;if(tokens){tokenCache.tokens=JSON.parse(tokens);tokenCache.writeEnabled=!0}else{tokenCache.tokens=null}}catch(err){tokenCache.tokens=null}}return tokenCache.tokens}}});
//# sourceMappingURL=core-603fdcf0.js.map
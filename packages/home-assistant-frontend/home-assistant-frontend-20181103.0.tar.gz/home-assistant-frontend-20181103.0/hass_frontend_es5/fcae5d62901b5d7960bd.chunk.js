(window.webpackJsonp=window.webpackJsonp||[]).push([[37],{721:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var app_header_layout=__webpack_require__(155),app_header=__webpack_require__(154),app_toolbar=__webpack_require__(121),paper_listbox=__webpack_require__(122),paper_card=__webpack_require__(153),paper_checkbox=__webpack_require__(156),paper_item=__webpack_require__(119),html_tag=__webpack_require__(0),polymer_element=__webpack_require__(4),moment=__webpack_require__(363),moment_default=__webpack_require__.n(moment),dates=__webpack_require__(205),dates_default=__webpack_require__.n(dates),ha_menu_button=__webpack_require__(134),ha_style=__webpack_require__(120),preact_compat_es=__webpack_require__(194),lib=__webpack_require__(484),lib_default=__webpack_require__.n(lib),events_mixin=__webpack_require__(16);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function(obj){return typeof obj}}else{_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n      <link rel=\"stylesheet\" href=\"/static/panels/calendar/react-big-calendar.css\">\n      <style>\n        div#root {\n          height: 100%;\n          width: 100%;\n        }\n      </style>\n      <div id=\"root\"></div>"]);_templateObject=function(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}lib_default.a.setLocalizer(lib_default.a.momentLocalizer(moment_default.a));var ha_big_calendar_HaBigCalendar=function(_EventsMixin){_inherits(HaBigCalendar,_EventsMixin);function HaBigCalendar(){_classCallCheck(this,HaBigCalendar);return _possibleConstructorReturn(this,_getPrototypeOf(HaBigCalendar).apply(this,arguments))}_createClass(HaBigCalendar,[{key:"_update",value:function(events){var _this=this,allViews=lib_default.a.Views.values,BCElement=preact_compat_es["default"].createElement(lib_default.a,{events:events,views:allViews,popup:!0,onNavigate:function(date,viewName){return _this.fire("navigate",{date:date,viewName:viewName})},onView:function(viewName){return _this.fire("view-changed",{viewName:viewName})},eventPropGetter:this._setEventStyle,defaultView:"month",defaultDate:new Date});Object(preact_compat_es.render)(BCElement,this.$.root)}},{key:"_setEventStyle",value:function(event){var newStyle={};if(event.color){newStyle.backgroundColor=event.color}return{style:newStyle}}}],[{key:"template",get:function(){return Object(html_tag.a)(_templateObject())}},{key:"properties",get:function(){return{events:{type:Array,observer:"_update"}}}}]);return HaBigCalendar}(Object(events_mixin.a)(polymer_element.a));customElements.define("ha-big-calendar",ha_big_calendar_HaBigCalendar);var localize_mixin=__webpack_require__(10);function ha_panel_calendar_typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){ha_panel_calendar_typeof=function(obj){return typeof obj}}else{ha_panel_calendar_typeof=function(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return ha_panel_calendar_typeof(obj)}function ha_panel_calendar_templateObject(){var data=ha_panel_calendar_taggedTemplateLiteral(["\n      <style include=\"iron-flex ha-style\">\n        .content {\n          padding: 16px;\n          @apply --layout-horizontal;\n        }\n\n        ha-big-calendar {\n          min-height: 500px;\n          min-width: 100%;\n        }\n\n        #calendars {\n          padding-right: 16px;\n          width: 15%;\n          min-width: 170px;\n        }\n\n        paper-item {\n          cursor: pointer;\n        }\n\n        div.all_calendars {\n    \uFFFC     height: 20px;\n    \uFFFC     text-align: center;\n        }\n\n        .iron-selected {\n          background-color: #e5e5e5;\n          font-weight: normal;\n        }\n\n        :host([narrow]) .content {\n          flex-direction: column;\n        }\n        :host([narrow]) #calendars {\n          margin-bottom: 24px;\n          width: 100%;\n        }\n      </style>\n\n      <app-header-layout has-scrolling-region>\n        <app-header slot=\"header\" fixed>\n          <app-toolbar>\n            <ha-menu-button narrow='[[narrow]]' show-menu='[[showMenu]]'></ha-menu-button>\n            <div main-title>[[localize('panel.calendar')]]</div>\n          </app-toolbar>\n        </app-header>\n\n        <div class=\"flex content\">\n          <div id=\"calendars\" class=\"layout vertical wrap\">\n            <paper-card heading=\"Calendars\">\n              <paper-listbox\n                id=\"calendar_list\"\n                multi\n                on-selected-items-changed=\"_fetchData\"\n                selected-values=\"{{selectedCalendars}}\"\n                attr-for-selected=\"item-name\"\n              >\n                <template is=\"dom-repeat\" items=\"[[calendars]]\">\n                  <paper-item item-name=\"[[item.entity_id]]\">\n                    <span class=\"calendar_color\" style$=\"background-color: [[item.color]]\"></span>\n                    <span class=\"calendar_color_spacer\"></span>\n                    [[item.name]]\n                  </paper-item>\n                </template>\n              </paper-listbox>\n            </paper-card>\n          </div>\n          <div class=\"flex layout horizontal wrap\">\n            <ha-big-calendar\n              default-date=\"[[currentDate]]\"\n              default-view=\"[[currentView]]\"\n              on-navigate='_handleNavigate'\n              on-view='_handleViewChanged'\n              events=\"[[events]]\">\n            </ha-big-calendar>\n          </div>\n        </div>\n      </app-header-layout>"]);ha_panel_calendar_templateObject=function(){return data};return data}function ha_panel_calendar_taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function ha_panel_calendar_classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function ha_panel_calendar_defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function ha_panel_calendar_createClass(Constructor,protoProps,staticProps){if(protoProps)ha_panel_calendar_defineProperties(Constructor.prototype,protoProps);if(staticProps)ha_panel_calendar_defineProperties(Constructor,staticProps);return Constructor}function ha_panel_calendar_possibleConstructorReturn(self,call){if(call&&("object"===ha_panel_calendar_typeof(call)||"function"===typeof call)){return call}return ha_panel_calendar_assertThisInitialized(self)}function ha_panel_calendar_assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _get(target,property,receiver){if("undefined"!==typeof Reflect&&Reflect.get){_get=Reflect.get}else{_get=function(target,property,receiver){var base=_superPropBase(target,property);if(!base)return;var desc=Object.getOwnPropertyDescriptor(base,property);if(desc.get){return desc.get.call(receiver)}return desc.value}}return _get(target,property,receiver||target)}function _superPropBase(object,property){while(!Object.prototype.hasOwnProperty.call(object,property)){object=ha_panel_calendar_getPrototypeOf(object);if(null===object)break}return object}function ha_panel_calendar_getPrototypeOf(o){ha_panel_calendar_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function(o){return o.__proto__||Object.getPrototypeOf(o)};return ha_panel_calendar_getPrototypeOf(o)}function ha_panel_calendar_inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)ha_panel_calendar_setPrototypeOf(subClass,superClass)}function ha_panel_calendar_setPrototypeOf(o,p){ha_panel_calendar_setPrototypeOf=Object.setPrototypeOf||function(o,p){o.__proto__=p;return o};return ha_panel_calendar_setPrototypeOf(o,p)}var ha_panel_calendar_HaPanelCalendar=function(_LocalizeMixin){ha_panel_calendar_inherits(HaPanelCalendar,_LocalizeMixin);function HaPanelCalendar(){ha_panel_calendar_classCallCheck(this,HaPanelCalendar);return ha_panel_calendar_possibleConstructorReturn(this,ha_panel_calendar_getPrototypeOf(HaPanelCalendar).apply(this,arguments))}ha_panel_calendar_createClass(HaPanelCalendar,[{key:"connectedCallback",value:function(){_get(ha_panel_calendar_getPrototypeOf(HaPanelCalendar.prototype),"connectedCallback",this).call(this);this._fetchCalendars()}},{key:"_fetchCalendars",value:function(){var _this=this;this.hass.callApi("get","calendars").then(function(result){_this.calendars=result;_this.selectedCalendars=result.map(function(cal){return cal.entity_id})})}},{key:"_fetchData",value:function(){var _this2=this,start=dates_default.a.firstVisibleDay(this.currentDate).toISOString(),end=dates_default.a.lastVisibleDay(this.currentDate).toISOString(),params=encodeURI("?start=".concat(start,"&end=").concat(end)),calls=this.selectedCalendars.map(function(cal){return _this2.hass.callApi("get","calendars/".concat(cal).concat(params))});Promise.all(calls).then(function(results){var tmpEvents=[];results.forEach(function(res){res.forEach(function(ev){ev.start=new Date(ev.start);if(ev.end){ev.end=new Date(ev.end)}else{ev.end=null}tmpEvents.push(ev)})});_this2.events=tmpEvents})}},{key:"_getDateRange",value:function(){var startDate,endDate;if("day"===this.currentView){startDate=moment_default()(this.currentDate).startOf("day");endDate=moment_default()(this.currentDate).startOf("day")}else if("week"===this.currentView){startDate=moment_default()(this.currentDate).startOf("isoWeek");endDate=moment_default()(this.currentDate).endOf("isoWeek")}else if("month"===this.currentView){startDate=moment_default()(this.currentDate).startOf("month").subtract(7,"days");endDate=moment_default()(this.currentDate).endOf("month").add(7,"days")}else if("agenda"===this.currentView){startDate=moment_default()(this.currentDate).startOf("day");endDate=moment_default()(this.currentDate).endOf("day").add(1,"month")}return[startDate.toISOString(),endDate.toISOString()]}},{key:"_handleViewChanged",value:function(ev){this.currentView=ev.detail.viewName;this._fetchData()}},{key:"_handleNavigate",value:function(ev){this.currentDate=ev.detail.date;this.currentView=ev.detail.viewName;this._fetchData()}}],[{key:"template",get:function(){return Object(html_tag.a)(ha_panel_calendar_templateObject())}},{key:"properties",get:function(){return{hass:Object,currentView:{type:String,value:"month"},currentDate:{type:Object,value:new Date},events:{type:Array,value:[]},calendars:{type:Array,value:[]},selectedCalendars:{type:Array,value:[]},narrow:{type:Boolean,reflectToAttribute:!0},showMenu:{type:Boolean,value:!1}}}}]);return HaPanelCalendar}(Object(localize_mixin.a)(polymer_element.a));customElements.define("ha-panel-calendar",ha_panel_calendar_HaPanelCalendar)}}]);
//# sourceMappingURL=fcae5d62901b5d7960bd.chunk.js.map
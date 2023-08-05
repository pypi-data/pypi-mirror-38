(window.webpackJsonp=window.webpackJsonp||[]).push([[60],{211:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(62),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(61),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(216),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(198),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(0),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(4),_vaadin_vaadin_combo_box_vaadin_combo_box_light__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(238),_state_badge__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(125),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(27),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(10),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(16);class HaEntityPicker extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
      <style>
        paper-input > paper-icon-button {
          width: 24px;
          height: 24px;
          padding: 2px;
          color: var(--secondary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <vaadin-combo-box-light
        items="[[_states]]"
        item-value-path="entity_id"
        item-label-path="entity_id"
        value="{{value}}"
        opened="{{opened}}"
        allow-custom-value="[[allowCustomEntity]]"
        on-change="_fireChanged"
      >
        <paper-input
          autofocus="[[autofocus]]"
          label="[[_computeLabel(label, localize)]]"
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
          value="[[value]]"
          disabled="[[disabled]]"
        >
          <paper-icon-button
            slot="suffix"
            class="clear-button"
            icon="hass:close"
            no-ripple=""
            hidden$="[[!value]]"
            >Clear</paper-icon-button
          >
          <paper-icon-button
            slot="suffix"
            class="toggle-button"
            icon="[[_computeToggleIcon(opened)]]"
            hidden="[[!_states.length]]"
            >Toggle</paper-icon-button
          >
        </paper-input>
        <template>
          <style>
            paper-icon-item {
              margin: -10px;
              padding: 0;
            }
          </style>
          <paper-icon-item>
            <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>
            <paper-item-body two-line="">
              <div>[[_computeStateName(item)]]</div>
              <div secondary="">[[item.entity_id]]</div>
            </paper-item-body>
          </paper-icon-item>
        </template>
      </vaadin-combo-box-light>
    `}static get properties(){return{allowCustomEntity:{type:Boolean,value:!1},hass:{type:Object,observer:"_hassChanged"},_hass:Object,_states:{type:Array,computed:"_computeStates(_hass, domainFilter, entityFilter)"},autofocus:Boolean,label:{type:String},value:{type:String,notify:!0},opened:{type:Boolean,value:!1,observer:"_openedChanged"},domainFilter:{type:String,value:null},entityFilter:{type:Function,value:null},disabled:Boolean}}_computeLabel(label,localize){return label===void 0?localize("ui.components.entity.entity-picker.entity"):label}_computeStates(hass,domainFilter,entityFilter){if(!hass)return[];let entityIds=Object.keys(hass.states);if(domainFilter){entityIds=entityIds.filter(eid=>eid.substr(0,eid.indexOf("."))===domainFilter)}let entities=entityIds.sort().map(key=>hass.states[key]);if(entityFilter){entities=entities.filter(entityFilter)}return entities}_computeStateName(state){return Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(state)}_openedChanged(newVal){if(!newVal){this._hass=this.hass}}_hassChanged(newVal){if(!this.opened){this._hass=newVal}}_computeToggleIcon(opened){return opened?"hass:menu-up":"hass:menu-down"}_fireChanged(ev){ev.stopPropagation();this.fire("change")}}customElements.define("ha-entity-picker",HaEntityPicker)},713:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiGlanceCardEditor",function(){return HuiGlanceCardEditor});var _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(195),_polymer_paper_checkbox_paper_checkbox__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(156),_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(218),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(75),_components_entity_state_badge__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(125),_components_entity_ha_entity_picker__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(211),_components_ha_card__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(108),_components_ha_icon__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(88);class HuiGlanceCardEditor extends Object(_mixins_lit_localize_mixin__WEBPACK_IMPORTED_MODULE_2__.a)(_polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.a){static get properties(){return{hass:{},_config:{}}}setConfig(config){this._config=Object.assign({type:"glance"},config)}render(){if(!this.hass){return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c``}return _polymer_lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
      <paper-input
        label="Title"
        value="${this._config.title}"
        .configValue="${"title"}"
        @value-changed="${this._valueChanged}"
      ></paper-input
      ><br />
      <paper-checkbox
        ?checked="${!1!==this._config.show_name}"
        .configValue="${"show_name"}"
        @change="${this._valueChanged}"
        >Show Entity's Name?</paper-checkbox
      ><br /><br />
      <paper-checkbox
        ?checked="${!1!==this._config.show_state}"
        .configValue="${"show_state"}"
        @change="${this._valueChanged}"
        >Show Entity's State Text?</paper-checkbox
      ><br />
    `}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.target,newValue=target.checked!==void 0?target.checked:target.value;Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_3__.a)(this,"config-changed",{config:Object.assign({},this._config,{[target.configValue]:newValue})})}}customElements.define("hui-glance-card-editor",HuiGlanceCardEditor)}}]);
//# sourceMappingURL=b994404b4095f8d43562.chunk.js.map
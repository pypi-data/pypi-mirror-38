(window.webpackJsonp=window.webpackJsonp||[]).push([[60],{212:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(62),_polymer_paper_input_paper_input__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(61),_polymer_paper_item_paper_icon_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(217),_polymer_paper_item_paper_item_body__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(198),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(0),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(4),_vaadin_vaadin_combo_box_vaadin_combo_box_light__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(240),_state_badge__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(125),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(27),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(10),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(16);class HaEntityPicker extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_10__.a)(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_5__.a)){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_4__.a`
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
    `}static get properties(){return{allowCustomEntity:{type:Boolean,value:!1},hass:{type:Object,observer:"_hassChanged"},_hass:Object,_states:{type:Array,computed:"_computeStates(_hass, domainFilter, entityFilter)"},autofocus:Boolean,label:{type:String},value:{type:String,notify:!0},opened:{type:Boolean,value:!1,observer:"_openedChanged"},domainFilter:{type:String,value:null},entityFilter:{type:Function,value:null},disabled:Boolean}}_computeLabel(label,localize){return label===void 0?localize("ui.components.entity.entity-picker.entity"):label}_computeStates(hass,domainFilter,entityFilter){if(!hass)return[];let entityIds=Object.keys(hass.states);if(domainFilter){entityIds=entityIds.filter(eid=>eid.substr(0,eid.indexOf("."))===domainFilter)}let entities=entityIds.sort().map(key=>hass.states[key]);if(entityFilter){entities=entities.filter(entityFilter)}return entities}_computeStateName(state){return Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(state)}_openedChanged(newVal){if(!newVal){this._hass=this.hass}}_hassChanged(newVal){if(!this.opened){this._hass=newVal}}_computeToggleIcon(opened){return opened?"hass:menu-up":"hass:menu-down"}_fireChanged(ev){ev.stopPropagation();this.fire("change")}}customElements.define("ha-entity-picker",HaEntityPicker)},721:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(194),paper_checkbox=__webpack_require__(156),paper_dropdown_menu=__webpack_require__(123),paper_item=__webpack_require__(119),paper_listbox=__webpack_require__(121);function processEditorEntities(entities){return entities.map(entityConf=>{if("string"===typeof entityConf){return{entity:entityConf}}return entityConf})}var lit_localize_mixin=__webpack_require__(203),fire_event=__webpack_require__(75),state_badge=__webpack_require__(125),paper_button=__webpack_require__(54);class hui_theme_select_editor_HuiThemeSelectionEditor extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},value:{}}}render(){const themes=["Backend-selected","default"].concat(Object.keys(this.hass.themes.themes).sort());return lit_element.c`
      ${this.renderStyle()}
      <paper-dropdown-menu
        label="Theme"
        dynamic-align
        @value-changed="${this._changed}"
      >
        <paper-listbox
          slot="dropdown-content"
          .selected="${this.value||"Backend-selected"}"
          attr-for-selected="theme"
        >
          ${themes.map(theme=>{return lit_element.c`
                <paper-item theme="${theme}">${theme}</paper-item>
              `})}
        </paper-listbox>
      </paper-dropdown-menu>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-dropdown-menu {
          width: 100%;
        }
      </style>
    `}_changed(ev){this.value=ev.target.value;Object(fire_event.a)(this,"change")}}customElements.define("hui-theme-select-editor",hui_theme_select_editor_HuiThemeSelectionEditor);__webpack_require__(212);class hui_entity_editor_HuiEntityEditor extends lit_element.a{static get properties(){return{hass:{},entities:{}}}render(){if(!this.entities){return lit_element.c``}return lit_element.c`
      ${this.renderStyle()}
      <h3>Entities</h3>
      <div class="entities">
        ${this.entities.map((entityConf,index)=>{return lit_element.c`
              <ha-entity-picker
                .hass="${this.hass}"
                .value="${entityConf.entity}"
                .index="${index}"
                @change="${this._valueChanged}"
                allow-custom-entity
              ></ha-entity-picker>
            `})}
      </div>
      <paper-button noink raised @click="${this._addEntity}"
        >Add Entity</paper-button
      >
    `}_addEntity(){const newConfigEntities=this.entities.concat({entity:""});Object(fire_event.a)(this,"change",{entities:newConfigEntities})}_valueChanged(ev){const target=ev.target,newConfigEntities=this.entities.concat();if(""===target.value){newConfigEntities.splice(target.index,1)}else{newConfigEntities[target.index]=Object.assign({},newConfigEntities[target.index],{entity:target.value})}Object(fire_event.a)(this,"change",{entities:newConfigEntities})}renderStyle(){return lit_element.c`
      <style>
        .entities {
          padding-left: 20px;
        }
        paper-button {
          margin: 8px 0;
        }
      </style>
    `}}customElements.define("hui-entity-editor",hui_entity_editor_HuiEntityEditor);var ha_card=__webpack_require__(108),ha_icon=__webpack_require__(88);__webpack_require__.d(__webpack_exports__,"HuiGlanceCardEditor",function(){return hui_glance_card_editor_HuiGlanceCardEditor});class hui_glance_card_editor_HuiGlanceCardEditor extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{hass:{},_config:{},_configEntities:{}}}setConfig(config){this._config=Object.assign({type:"glance"},config);this._configEntities=processEditorEntities(config.entities)}render(){if(!this.hass){return lit_element.c``}return lit_element.c`
      ${this.renderStyle()}
      <paper-input
        label="Title"
        value="${this._config.title}"
        .configValue="${"title"}"
        @value-changed="${this._valueChanged}"
      ></paper-input>
      <hui-theme-select-editor
        .hass="${this.hass}"
        .value="${this._config.theme}"
        .configValue="${"theme"}"
        @change="${this._valueChanged}"
      ></hui-theme-select-editor>
      <paper-input
        label="Columns"
        value="${this._config.columns||""}"
        .configValue="${"columns"}"
        @value-changed="${this._valueChanged}"
      ></paper-input>
      <hui-entity-editor
        .hass="${this.hass}"
        .entities="${this._configEntities}"
        @change="${this._valueChanged}"
      ></hui-entity-editor>
      <paper-checkbox
        ?checked="${!1!==this._config.show_name}"
        .configValue="${"show_name"}"
        @change="${this._valueChanged}"
        >Show Entity's Name?</paper-checkbox
      >
      <paper-checkbox
        ?checked="${!1!==this._config.show_state}"
        .configValue="${"show_state"}"
        @change="${this._valueChanged}"
        >Show Entity's State Text?</paper-checkbox
      >
    `}_valueChanged(ev){if(!this._config||!this.hass){return}const target=ev.target;let newConfig=this._config;if(ev.detail&&ev.detail.entities){newConfig.entities=ev.detail.entities}else{newConfig=Object.assign({},this._config,{[target.configValue]:target.checked!==void 0?target.checked:target.value})}Object(fire_event.a)(this,"config-changed",{config:newConfig})}renderStyle(){return lit_element.c`
      <style>
        paper-checkbox {
          display: block;
          padding-top: 16px;
        }
      </style>
    `}}customElements.define("hui-glance-card-editor",hui_glance_card_editor_HuiGlanceCardEditor)}}]);
//# sourceMappingURL=982973c454255934f80f.chunk.js.map
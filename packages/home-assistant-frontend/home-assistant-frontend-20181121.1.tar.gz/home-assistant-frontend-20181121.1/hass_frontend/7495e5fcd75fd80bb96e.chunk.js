(window.webpackJsonp=window.webpackJsonp||[]).push([[62],{725:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(90),classMap=__webpack_require__(205),js_yaml=__webpack_require__(419),js_yaml_default=__webpack_require__.n(js_yaml),paper_spinner=__webpack_require__(136),paper_dialog=__webpack_require__(176),paper_button=__webpack_require__(57),paper_textarea=__webpack_require__(180),paper_dialog_scrollable=__webpack_require__(182);const getCardConfig=(hass,cardId)=>hass.callWS({type:"lovelace/config/card/get",card_id:cardId}),updateCardConfig=(hass,cardId,config,configFormat)=>hass.callWS({type:"lovelace/config/card/update",card_id:cardId,card_config:config,format:configFormat}),migrateConfig=hass=>hass.callWS({type:"lovelace/config/migrate"});var fire_event=__webpack_require__(81),lit_localize_mixin=__webpack_require__(172);class hui_yaml_editor_HuiYAMLEditor extends lit_element.a{static get properties(){return{_yaml:{},cardId:{}}}set yaml(yaml){if(yaml===void 0){this._loading=!0;this._loadConfig()}else{this._yaml=yaml;if(this._loading){this._loading=!1}}}render(){return lit_element.c`
      ${this.renderStyle()}
      <paper-spinner
        ?active="${this._loading}"
        alt="Loading"
        class="center"
      ></paper-spinner>
      <paper-textarea
        max-rows="10"
        .value="${this._yaml}"
        @value-changed="${this._valueChanged}"
      ></paper-textarea>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-textarea {
          --paper-input-container-shared-input-style_-_font-family: monospace;
        }
        .center {
          margin-left: auto;
          margin-right: auto;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
      </style>
    `}async _loadConfig(){if(!this.hass||!this.cardId){return}this._yaml=await getCardConfig(this.hass,this.cardId);if(this._loading){this._loading=!1}}_valueChanged(ev){const target=ev.target;this._yaml=target.value;Object(fire_event.a)(this,"yaml-changed",{yaml:target.value})}}customElements.define("hui-yaml-editor",hui_yaml_editor_HuiYAMLEditor);var create_card_element=__webpack_require__(300),create_error_card_config=__webpack_require__(221);const CUSTOM_TYPE_PREFIX="custom:";class hui_card_preview_HuiCardPreview extends HTMLElement{set hass(value){this._hass=value;if(this._element){this._element.hass=value}}set error(error){const configValue=Object(create_error_card_config.a)(`${error.type}: ${error.message}`,void 0);this._createCard(configValue)}set config(configValue){if(!configValue){return}if(!this._element){this._createCard(configValue);return}const tag=configValue.type.startsWith(CUSTOM_TYPE_PREFIX)?configValue.type.substr(CUSTOM_TYPE_PREFIX.length):`hui-${configValue.type}-card`;if(tag.toUpperCase()===this._element.tagName){this._element.setConfig(configValue)}else{this._createCard(configValue)}}_createCard(configValue){if(this._element){this.removeChild(this._element)}this._element=Object(create_card_element.a)(configValue);if(this._hass){this._element.hass=this._hass}this.appendChild(this._element)}}customElements.define("hui-card-preview",hui_card_preview_HuiCardPreview);const secretYamlType=new js_yaml_default.a.Type("!secret",{kind:"scalar",construct(data){data=data||"";return"!secret "+data}}),includeYamlType=new js_yaml_default.a.Type("!include",{kind:"scalar",construct(data){data=data||"";return"!include "+data}}),extYamlSchema=js_yaml_default.a.Schema.create([secretYamlType,includeYamlType]),hui_edit_card_CUSTOM_TYPE_PREFIX="custom:";class hui_edit_card_HuiEditCard extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{_hass:{},_cardId:{},_originalConfig:{},_configElement:{},_configValue:{},_configState:{},_uiEditor:{},_saving:{},_loading:{},_isToggleAvailable:{}}}constructor(){super();this._saving=!1}set cardConfig(cardConfig){this._originalConfig=cardConfig;if(cardConfig.id+""!==this._cardId){this._loading=!0;this._uiEditor=!0;this._configElement=void 0;this._configValue={format:"yaml",value:void 0};this._configState="OK";this._isToggleAvailable=!1;this._cardId=cardConfig.id+"";this._loadConfigElement()}}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}get _previewEl(){return this.shadowRoot.querySelector("hui-card-preview")}render(){return lit_element.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.edit.header")}</h2>
        <paper-spinner
          ?active="${this._loading}"
          alt="Loading"
          class="center margin-bot"
        ></paper-spinner>
        <paper-dialog-scrollable
          class="${Object(classMap.a)({hidden:this._loading})}"
        >
          ${this._uiEditor&&null!==this._configElement?lit_element.c`
                  <div class="element-editor">${this._configElement}</div>
                `:lit_element.c`
                  <hui-yaml-editor
                    .hass="${this.hass}"
                    .cardId="${this._cardId}"
                    .yaml="${this._configValue.value}"
                    @yaml-changed="${this._handleYamlChanged}"
                  ></hui-yaml-editor>
                `}
          <hui-card-preview .hass="${this.hass}"></hui-card-preview>
        </paper-dialog-scrollable>
        ${!this._loading?lit_element.c`
                <div class="paper-dialog-buttons">
                  <paper-button
                    ?disabled="${!this._isToggleAvailable}"
                    @click="${this._toggleEditor}"
                    >${this.localize("ui.panel.lovelace.editor.edit.toggle_editor")}</paper-button
                  >
                  <paper-button @click="${this._closeDialog}"
                    >${this.localize("ui.common.cancel")}</paper-button
                  >
                  <paper-button
                    ?disabled="${this._saving}"
                    @click="${this._save}"
                  >
                    <paper-spinner
                      ?active="${this._saving}"
                      alt="Saving"
                    ></paper-spinner>
                    ${this.localize("ui.panel.lovelace.editor.edit.save")}</paper-button
                  >
                </div>
              `:lit_element.c``}
      </paper-dialog>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        .center {
          margin-left: auto;
          margin-right: auto;
        }
        .margin-bot {
          margin-bottom: 24px;
        }
        paper-button paper-spinner {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
        .hidden {
          display: none;
        }
        .element-editor {
          margin-bottom: 16px;
        }
      </style>
    `}_toggleEditor(){if(!this._isToggleAvailable){alert("You can't switch editor.");return}if(this._uiEditor&&"json"===this._configValue.format){if(this._isConfigChanged()){this._configValue={format:"yaml",value:js_yaml_default.a.safeDump(this._configValue.value)}}else{this._configValue={format:"yaml",value:void 0}}this._uiEditor=!this._uiEditor}else if(this._configElement&&"yaml"===this._configValue.format){this._configValue={format:"json",value:js_yaml_default.a.safeLoad(this._configValue.value,{schema:extYamlSchema})};this._configElement.setConfig(this._configValue.value);this._uiEditor=!this._uiEditor}this._resizeDialog()}_save(){this._saving=!0;this._updateConfigInBackend()}_saveDone(){this._saving=!1}async _loadedDialog(){await this.updateComplete;this._loading=!1;this._resizeDialog()}async _resizeDialog(){await this.updateComplete;Object(fire_event.a)(this._dialog,"iron-resize")}_closeDialog(){this._dialog.close()}async _updateConfigInBackend(){if(!this._isConfigValid()){alert("Your config is not valid, please fix your config before saving.");this._saveDone();return}if(!this._isConfigChanged()){this._closeDialog();this._saveDone();return}try{await updateCardConfig(this.hass,this._cardId,this._configValue.value,this._configValue.format);this._closeDialog();this._saveDone();Object(fire_event.a)(this,"reload-lovelace")}catch(err){alert(`Saving failed: ${err.message}`);this._saveDone()}}_handleYamlChanged(ev){this._configValue={format:"yaml",value:ev.detail.yaml};try{const config=js_yaml_default.a.safeLoad(this._configValue.value,{schema:extYamlSchema});this._updatePreview(config);this._configState="OK";if(!this._isToggleAvailable&&null!==this._configElement){this._isToggleAvailable=!0}}catch(err){this._isToggleAvailable=!1;this._configState="YAML_ERROR";this._setPreviewError({type:"YAML Error",message:err})}}_handleUIConfigChanged(value){this._configValue={format:"json",value};this._updatePreview(value)}_updatePreview(config){if(!this._previewEl){return}this._previewEl.config=config;if(this._loading){this._loadedDialog()}else{this._resizeDialog()}}_setPreviewError(error){if(!this._previewEl){return}this._previewEl.error=error;this._resizeDialog()}_isConfigValid(){if(!this._cardId||!this._configValue||!this._configValue.value){return!1}if("OK"===this._configState){return!0}else{return!1}}_isConfigChanged(){const configValue="yaml"===this._configValue.format?js_yaml_default.a.safeDump(this._configValue.value):this._configValue.value;return JSON.stringify(configValue)!==JSON.stringify(this._originalConfig)}async _loadConfigElement(){if(!this._originalConfig){return}const conf=this._originalConfig,tag=conf.type.startsWith(hui_edit_card_CUSTOM_TYPE_PREFIX)?conf.type.substr(hui_edit_card_CUSTOM_TYPE_PREFIX.length):`hui-${conf.type}-card`,elClass=customElements.get(tag);let configElement;try{configElement=await elClass.getConfigElement()}catch(err){this._configElement=null;this._uiEditor=!1;return}this._isToggleAvailable=!0;configElement.setConfig(conf);configElement.hass=this.hass;configElement.addEventListener("config-changed",ev=>this._handleUIConfigChanged(ev.detail.config));this._configValue={format:"json",value:conf};this._configElement=configElement;this._updatePreview(conf)}}customElements.define("hui-edit-card",hui_edit_card_HuiEditCard);class hui_migrate_config_HuiMigrateConfig extends Object(lit_localize_mixin.a)(lit_element.a){static get properties(){return{_hass:{},_migrating:{}}}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}async showDialog(){if(null==this._dialog){await this.updateComplete}this._dialog.open()}render(){return lit_element.c`
      ${this.renderStyle()}
      <paper-dialog with-backdrop>
        <h2>${this.localize("ui.panel.lovelace.editor.migrate.header")}</h2>
        <paper-dialog-scrollable>
          <p>${this.localize("ui.panel.lovelace.editor.migrate.para_no_id")}</p>
          <p>
            ${this.localize("ui.panel.lovelace.editor.migrate.para_migrate")}
          </p>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._closeDialog}"
            >${this.localize("ui.common.cancel")}</paper-button
          >
          <paper-button
            ?disabled="${this._migrating}"
            @click="${this._migrateConfig}"
          >
            <paper-spinner
              ?active="${this._migrating}"
              alt="Saving"
            ></paper-spinner>
            ${this.localize("ui.panel.lovelace.editor.migrate.migrate")}</paper-button
          >
        </div>
      </paper-dialog>
    `}renderStyle(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        paper-spinner {
          display: none;
        }
        paper-spinner[active] {
          display: block;
        }
        paper-button paper-spinner {
          width: 14px;
          height: 14px;
          margin-right: 20px;
        }
      </style>
    `}_closeDialog(){this._dialog.close()}async _migrateConfig(){this._migrating=!0;try{await migrateConfig(this.hass);this._closeDialog();Object(fire_event.a)(this,"reload-lovelace")}catch(err){alert(`Migration failed: ${err.message}`);this._migrating=!1}}}customElements.define("hui-migrate-config",hui_migrate_config_HuiMigrateConfig);__webpack_require__.d(__webpack_exports__,"HuiDialogEditCard",function(){return hui_dialog_edit_card_HuiDialogEditCard});class hui_dialog_edit_card_HuiDialogEditCard extends lit_element.a{static get properties(){return{_hass:{},_cardConfig:{}}}async showDialog({hass,cardConfig,reloadLovelace}){this._hass=hass;this._cardConfig=cardConfig;this._reloadLovelace=reloadLovelace;await this.updateComplete;this.shadowRoot.children[0].showDialog()}render(){return lit_element.c`
      ${this._cardConfig.id?lit_element.c`
              <hui-edit-card
                .cardConfig="${this._cardConfig}"
                .hass="${this._hass}"
                @reload-lovelace="${this._reloadLovelace}"
              >
              </hui-edit-card>
            `:lit_element.c`
              <hui-migrate-config
                .hass="${this._hass}"
                @reload-lovelace="${this._reloadLovelace}"
              ></hui-migrate-config>
            `}
    `}}customElements.define("hui-dialog-edit-card",hui_dialog_edit_card_HuiDialogEditCard)}}]);
//# sourceMappingURL=7495e5fcd75fd80bb96e.chunk.js.map
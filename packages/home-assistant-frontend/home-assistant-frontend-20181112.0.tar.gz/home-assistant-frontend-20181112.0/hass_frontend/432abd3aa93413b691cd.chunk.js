(window.webpackJsonp=window.webpackJsonp||[]).push([[61],{720:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(194),js_yaml=__webpack_require__(415),js_yaml_default=__webpack_require__.n(js_yaml),when=__webpack_require__(680),paper_button=__webpack_require__(54),paper_textarea=__webpack_require__(209),paper_dialog_scrollable=__webpack_require__(211),paper_dialog=__webpack_require__(208);const getCardConfig=(hass,cardId)=>hass.callWS({type:"lovelace/config/card/get",card_id:cardId}),updateCardConfig=(hass,cardId,config)=>hass.callWS({type:"lovelace/config/card/update",card_id:cardId,card_config:config});var fire_event=__webpack_require__(75);class hui_yaml_editor_HuiYAMLEditor extends lit_element.a{static get properties(){return{yaml:{}}}render(){return lit_element.c`
      <style>
        paper-textarea {
          --paper-input-container-shared-input-style_-_font-family: monospace;
        }
      </style>
      <paper-textarea
        max-rows="10"
        value="${this.yaml}"
        @value-changed="${this._valueChanged}"
      ></paper-textarea>
    `}_valueChanged(ev){const target=ev.target;this.yaml=target.value;Object(fire_event.a)(this,"yaml-changed",{yaml:target.value})}}customElements.define("hui-yaml-editor",hui_yaml_editor_HuiYAMLEditor);var create_card_element=__webpack_require__(297),create_error_card_config=__webpack_require__(256);class hui_yaml_card_preview_HuiYAMLCardPreview extends HTMLElement{set hass(value){this._hass=value;if(this.lastChild){this.lastChild.hass=value}}set value(configValue){if(this.lastChild){this.removeChild(this.lastChild)}if(!configValue.value||""===configValue.value){return}let conf;if("yaml"===configValue.format){try{conf=js_yaml_default.a.safeLoad(configValue.value)}catch(err){conf=Object(create_error_card_config.a)(`Invalid YAML: ${err.message}`,void 0)}}else{conf=configValue.value}const element=Object(create_card_element.a)(conf);if(this._hass){element.hass=this._hass}this.appendChild(element)}}customElements.define("hui-yaml-card-preview",hui_yaml_card_preview_HuiYAMLCardPreview);__webpack_require__.d(__webpack_exports__,"HuiDialogEditCard",function(){return hui_dialog_edit_card_HuiDialogEditCard});const CUSTOM_TYPE_PREFIX="custom:";class hui_dialog_edit_card_HuiDialogEditCard extends lit_element.a{static get properties(){return{hass:{},cardId:{type:Number},_dialogClosedCallback:{},_configElement:{},_editorToggle:{}}}async showDialog({hass,cardId,reloadLovelace}){this.hass=hass;this._cardId=cardId;this._reloadLovelace=reloadLovelace;this._editorToggle=!0;this._configElement=void 0;this._configValue={format:"yaml",value:""};this._loadConfig().then(()=>this._loadConfigElement());await this.updateComplete;this._dialog.open()}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}get _previewEl(){return this.shadowRoot.querySelector("hui-yaml-card-preview")}render(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
        .element-editor {
          margin-bottom: 16px;
        }
      </style>
      <paper-dialog with-backdrop>
        <h2>Card Configuration</h2>
        <paper-dialog-scrollable>
          ${this._editorToggle&&null!==this._configElement?lit_element.c`
                  <div class="element-editor">
                    ${Object(when.a)(this._configElement,()=>this._configElement,()=>lit_element.c`
                            Loading...
                          `)}
                  </div>
                `:lit_element.c`
                  <hui-yaml-editor
                    .yaml="${this._configValue.value}"
                    @yaml-changed="${this._handleYamlChanged}"
                  ></hui-yaml-editor>
                `}
          <hui-yaml-card-preview
            .hass="${this.hass}"
            .value="${this._configValue}"
          ></hui-yaml-card-preview>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._toggleEditor}"
            >Toggle Editor</paper-button
          >
          <paper-button @click="${this._closeDialog}">Cancel</paper-button>
          <paper-button @click="${this._updateConfigInBackend}"
            >Save</paper-button
          >
        </div>
      </paper-dialog>
    `}_handleYamlChanged(ev){this._configValue={format:"yaml",value:ev.detail.yaml};this._updatePreview(this._configValue)}_handleJSConfigChanged(value){this._configElement.setConfig(value);this._configValue={format:"js",value};this._updatePreview(this._configValue)}_updatePreview(value){if(!this._previewEl){return}this._previewEl.value=value}_closeDialog(){this._dialog.close()}_toggleEditor(){if(this._editorToggle&&"js"===this._configValue.format){this._configValue={format:"yaml",value:js_yaml_default.a.safeDump(this._configValue.value)}}else if(this._configElement&&"yaml"===this._configValue.format){this._configValue={format:"js",value:js_yaml_default.a.safeLoad(this._configValue.value)};this._configElement.setConfig(this._configValue.value)}this._editorToggle=!this._editorToggle}async _loadConfig(){const cardConfig=await getCardConfig(this.hass,this._cardId);this._configValue={format:"yaml",value:cardConfig};this._originalConfigYaml=cardConfig;Object(fire_event.a)(this._dialog,"iron-resize")}async _loadConfigElement(){const conf=js_yaml_default.a.safeLoad(this._configValue.value),tag=conf.type.startsWith(CUSTOM_TYPE_PREFIX)?conf.type.substr(CUSTOM_TYPE_PREFIX.length):`hui-${conf.type}-card`,elClass=customElements.get(tag);let configElement;try{configElement=await elClass.getConfigElement()}catch(err){this._configElement=null;return}configElement.setConfig(conf);configElement.hass=this.hass;configElement.addEventListener("config-changed",ev=>this._handleJSConfigChanged(ev.detail.config));this._configValue={format:"js",value:conf};this._configElement=configElement;Object(fire_event.a)(this._dialog,"iron-resize")}async _updateConfigInBackend(){if("js"===this._configValue.format){this._configValue={format:"yaml",value:js_yaml_default.a.safeDump(this._configValue.value)}}if(this._configValue.value===this._originalConfigYaml){this._dialog.close();return}try{await updateCardConfig(this.hass,this._cardId,this._configValue.value);this._dialog.close();this._reloadLovelace()}catch(err){alert(`Saving failed: ${err.reason}`)}}}customElements.define("hui-dialog-edit-card",hui_dialog_edit_card_HuiDialogEditCard)}}]);
//# sourceMappingURL=432abd3aa93413b691cd.chunk.js.map
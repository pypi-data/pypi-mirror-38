(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{198:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(26),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(29),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(42),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(3),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},218:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(26),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(42),_paper_item_shared_styles_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(128),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(3),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(0),_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(98);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[_paper_item_behavior_js__WEBPACK_IMPORTED_MODULE_6__.a]})},249:function(module,__webpack_exports__,__webpack_require__){"use strict";var _Mathround=Math.round,_Mathabs=Math.abs,_Mathceil=Math.ceil,_Mathfloor=Math.floor,_Mathmax=Math.max,_Mathmin=Math.min,spacing=__webpack_require__(221),style=__webpack_require__(225),overlay=__webpack_require__(358);const $_documentContainer=document.createElement("template");$_documentContainer.innerHTML=`<dom-module id="lumo-vaadin-overlay" theme-for="vaadin-overlay">
  <template>
    <style include="lumo-overlay">
      /* stylelint-disable no-empty-source */
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content);var vaadin_overlay=__webpack_require__(299),menu_overlay=__webpack_require__(359);const vaadin_combo_box_dropdown_styles_$_documentContainer=document.createElement("template");vaadin_combo_box_dropdown_styles_$_documentContainer.innerHTML=`<dom-module id="lumo-combo-box-overlay" theme-for="vaadin-combo-box-overlay">
  <template>
    <style include="lumo-overlay lumo-menu-overlay-core">
      [part="content"] {
        padding: 0;
      }

      :host {
        /* TODO: using a legacy mixin (unsupported) */
        --iron-list-items-container: {
          border-width: var(--lumo-space-xs);
          border-style: solid;
          border-color: transparent;
        };
      }

      /* TODO: workaround ShadyCSS issue when using inside of the dom-if */
      :host([opened]) {
        --iron-list-items-container_-_border-width: var(--lumo-space-xs);
        --iron-list-items-container_-_border-style: solid;
        --iron-list-items-container_-_border-color: transparent;
      }

      /* Loading state */

      /* When items are empty, the sinner needs some room */
      :host(:not([closing])) [part~="content"] {
        min-height: calc(2 * var(--lumo-space-s) + var(--lumo-icon-size-s));
      }

      [part~="overlay"] {
        position: relative;
      }

      :host([loading]) [part~="loader"] {
        box-sizing: border-box;
        width: var(--lumo-icon-size-s);
        height: var(--lumo-icon-size-s);
        position: absolute;
        z-index: 1;
        left: var(--lumo-space-s);
        right: var(--lumo-space-s);
        top: var(--lumo-space-s);
        margin-left: auto;
        margin-inline-start: auto;
        margin-inline-end: 0;
        border: 2px solid transparent;
        border-color:
          var(--lumo-primary-color-50pct)
          var(--lumo-primary-color-50pct)
          var(--lumo-primary-color)
          var(--lumo-primary-color);
        border-radius: calc(0.5 * var(--lumo-icon-size-s));
        opacity: 0;
        animation:
          1s linear infinite lumo-combo-box-loader-rotate,
          .3s .1s lumo-combo-box-loader-fade-in both;
        pointer-events: none;
      }

      @keyframes lumo-combo-box-loader-fade-in {
        0% {
          opacity: 0;
        }

        100% {
          opacity: 1;
        }
      }

      @keyframes lumo-combo-box-loader-rotate {
        0% {
          transform: rotate(0deg);
        }

        100% {
          transform: rotate(360deg);
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_combo_box_dropdown_styles_$_documentContainer.content);var color=__webpack_require__(233),font_icons=__webpack_require__(300),sizing=__webpack_require__(234),typography=__webpack_require__(238);const vaadin_item_styles_$_documentContainer=document.createElement("template");vaadin_item_styles_$_documentContainer.innerHTML=`<dom-module id="lumo-item" theme-for="vaadin-item">
  <template>
    <style>
      :host {
        display: flex;
        align-items: center;
        box-sizing: border-box;
        font-family: var(--lumo-font-family);
        font-size: var(--lumo-font-size-m);
        line-height: var(--lumo-line-height-xs);
        padding: 0.5em 1em;
        min-height: var(--lumo-size-m);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-tap-highlight-color: transparent;
      }

      /* Selectable items have a checkmark icon */
      :host([tabindex])::before {
        display: var(--_lumo-item-selected-icon-display, none);
        content: var(--lumo-icons-checkmark);
        font-family: lumo-icons;
        font-size: var(--lumo-icon-size-m);
        line-height: 1;
        font-weight: normal;
        width: 1em;
        height: 1em;
        margin: calc((1 - var(--lumo-line-height-xs)) * var(--lumo-font-size-m) / 2) 0;
        color: var(--lumo-primary-text-color);
        flex: none;
        opacity: 0;
        transition: transform 0.2s cubic-bezier(.12, .32, .54, 2), opacity 0.1s;
      }

      :host([selected])::before {
        opacity: 1;
      }

      :host([active]:not([selected]))::before {
        transform: scale(0.8);
        opacity: 0;
        transition-duration: 0s;
      }

      [part="content"] {
        flex: auto;
      }

      /* Disabled item */

      :host([disabled]) {
        color: var(--lumo-disabled-text-color);
        cursor: default;
        pointer-events: none;
      }

      /* Slotted icons */

      :host ::slotted(iron-icon) {
        width: var(--lumo-icon-size-m);
        height: var(--lumo-icon-size-m);
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_item_styles_$_documentContainer.content);var polymer_element=__webpack_require__(4),vaadin_themable_mixin=__webpack_require__(222);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const ItemMixin=superClass=>class extends superClass{static get properties(){return{_hasVaadinItemMixin:{value:!0},disabled:{type:Boolean,value:!1,observer:"_disabledChanged",reflectToAttribute:!0},selected:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_selectedChanged"},_value:String}}constructor(){super();this.value}get value(){return this._value!==void 0?this._value:this.textContent.trim()}set value(value){this._value=value}ready(){super.ready();const attrValue=this.getAttribute("value");if(null!==attrValue){this.value=attrValue}this.addEventListener("focus",()=>this._setFocused(!0),!0);this.addEventListener("blur",()=>this._setFocused(!1),!0);this.addEventListener("mousedown",()=>{this._setActive(this._mousedown=!0);const mouseUpListener=()=>{this._setActive(this._mousedown=!1);document.removeEventListener("mouseup",mouseUpListener)};document.addEventListener("mouseup",mouseUpListener)});this.addEventListener("keydown",e=>this._onKeydown(e));this.addEventListener("keyup",e=>this._onKeyup(e))}disconnectedCallback(){super.disconnectedCallback();if(this.hasAttribute("active")){this._setFocused(!1)}}_selectedChanged(selected){this.setAttribute("aria-selected",selected)}_disabledChanged(disabled){if(disabled){this.selected=!1;this.setAttribute("aria-disabled","true");this.blur()}else{this.removeAttribute("aria-disabled")}}_setFocused(focused){if(focused){this.setAttribute("focused","");if(!this._mousedown){this.setAttribute("focus-ring","")}}else{this.removeAttribute("focused");this.removeAttribute("focus-ring");this._setActive(!1)}}_setActive(active){if(active){this.setAttribute("active","")}else{this.removeAttribute("active")}}_onKeydown(event){if(/^( |SpaceBar|Enter)$/.test(event.key)&&!event.defaultPrevented){event.preventDefault();this._setActive(!0)}}_onKeyup(){if(this.hasAttribute("active")){this._setActive(!1);this.click()}}};var html_tag=__webpack_require__(0);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_item_ItemElement extends ItemMixin(Object(vaadin_themable_mixin.a)(polymer_element.a)){static get template(){return html_tag.a`
    <style>
      :host {
        display: inline-block;
      }

      :host([hidden]) {
        display: none !important;
      }
    </style>
    <div part="content">
      <slot></slot>
    </div>
`}static get is(){return"vaadin-item"}static get version(){return"2.1.0"}}customElements.define(vaadin_item_ItemElement.is,vaadin_item_ItemElement);const vaadin_combo_box_item_styles_$_documentContainer=document.createElement("template");vaadin_combo_box_item_styles_$_documentContainer.innerHTML=`<dom-module id="lumo-combo-box-item" theme-for="vaadin-combo-box-item">
  <template>
    <style include="lumo-item">
      /* TODO partly duplicated from vaadin-list-box styles. Should find a way to make it DRY */

      :host {
        cursor: default;
        -webkit-tap-highlight-color: var(--lumo-primary-color-10pct);
        padding-left: calc(var(--lumo-border-radius) / 4);
        padding-right: calc(var(--lumo-space-l) + var(--lumo-border-radius) / 4);
        transition: background-color 100ms;
        border-radius: var(--lumo-border-radius);
        overflow: hidden;
        --_lumo-item-selected-icon-display: block;
      }

      /* ShadyCSS workaround (show the selected item checkmark) */
      :host::before {
        display: block;
      }

      :host(:hover) {
        background-color: var(--lumo-primary-color-10pct);
      }

      :host([focused]:not([disabled])) {
        box-shadow: inset 0 0 0 2px var(--lumo-primary-color-50pct);
      }

      @media (pointer: coarse) {
        :host(:hover) {
          background-color: transparent;
        }

        :host([focused]:not([disabled])) {
          box-shadow: none;
        }
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild(vaadin_combo_box_item_styles_$_documentContainer.content);var vaadin_theme_property_mixin=__webpack_require__(301),utils_async=__webpack_require__(8),flush=__webpack_require__(20),templatize=__webpack_require__(28),iron_a11y_announcer=__webpack_require__(71),iron_a11y_keys_behavior=__webpack_require__(13),flattened_nodes_observer=__webpack_require__(58);/**
@license
Copyright (c) 2018 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const ComboBoxPlaceholder=class{toString(){return""}},ComboBoxMixin=subclass=>class extends subclass{static get properties(){return{opened:{type:Boolean,notify:!0,value:!1,reflectToAttribute:!0,observer:"_openedChanged"},disabled:{type:Boolean,value:!1,reflectToAttribute:!0},readonly:{type:Boolean,value:!1,reflectToAttribute:!0},renderer:Function,items:{type:Array,observer:"_itemsChanged"},allowCustomValue:{type:Boolean,value:!1},filteredItems:{type:Array},value:{type:String,observer:"_valueChanged",notify:!0,value:""},_lastCommittedValue:String,loading:{type:Boolean,value:!1,reflectToAttribute:!0},_focusedIndex:{type:Number,value:-1},filter:{type:String,value:"",notify:!0},selectedItem:{type:Object,notify:!0},itemLabelPath:{type:String,value:"label"},itemValuePath:{type:String,value:"value"},itemIdPath:String,name:{type:String},invalid:{type:Boolean,reflectToAttribute:!0,notify:!0,value:!1},_toggleElement:Object,_clearElement:Object,_inputElementValue:String,_closeOnBlurIsPrevented:Boolean,_previousDocumentPointerEvents:String,_itemTemplate:Object}}static get observers(){return["_filterChanged(filter, itemValuePath, itemLabelPath)","_itemsOrPathsChanged(items.*, itemValuePath, itemLabelPath)","_filteredItemsChanged(filteredItems.*, itemValuePath, itemLabelPath)","_templateOrRendererChanged(_itemTemplate, renderer)","_loadingChanged(loading)","_selectedItemChanged(selectedItem)","_toggleElementChanged(_toggleElement)"]}ready(){super.ready();this.addEventListener("focusout",e=>{if(e.relatedTarget===this.$.overlay.$.dropdown.$.overlay){e.composedPath()[0].focus();return}if(!this._closeOnBlurIsPrevented){this.close()}});this._lastCommittedValue=this.value;iron_a11y_announcer.a.requestAvailability();this.$.overlay.addEventListener("selection-changed",this._overlaySelectedItemChanged.bind(this));this.addEventListener("vaadin-combo-box-dropdown-closed",this._onClosed.bind(this));this.addEventListener("vaadin-combo-box-dropdown-opened",this._onOpened.bind(this));this.addEventListener("keydown",this._onKeyDown.bind(this));this.addEventListener("click",this._onClick.bind(this));this.$.overlay.addEventListener("vaadin-overlay-touch-action",this._onOverlayTouchAction.bind(this));this.addEventListener("touchend",e=>{if(!this._clearElement||e.composedPath()[0]!==this._clearElement){return}e.preventDefault();this._clear()});this._observer=new flattened_nodes_observer.a(this,info=>{this._setTemplateFromNodes(info.addedNodes)})}render(){this.$.overlay._selector.querySelectorAll("vaadin-combo-box-item").forEach(item=>item._render())}_setTemplateFromNodes(nodes){this._itemTemplate=nodes.filter(node=>node.localName&&"template"===node.localName)[0]||this._itemTemplate}_removeNewRendererOrTemplate(template,oldTemplate,renderer,oldRenderer){if(template!==oldTemplate){this._itemTemplate=void 0}else if(renderer!==oldRenderer){this.renderer=void 0}}_templateOrRendererChanged(template,renderer){if(template&&renderer){this._removeNewRendererOrTemplate(template,this._oldTemplate,renderer,this._oldRenderer);throw new Error("You should only use either a renderer or a template for combo box items")}this._oldTemplate=template;this._oldRenderer=renderer}open(){if(!this.disabled&&!this.readonly){this.opened=!0}}close(){this.opened=!1}_openedChanged(value,old){if(old===void 0){return}if(this.opened){this._openedWithFocusRing=this.hasAttribute("focus-ring")||this.focusElement&&this.focusElement.hasAttribute("focus-ring");if(!this.$.overlay.touchDevice){if(!this.focused){this.focus()}}}else{if(this._openedWithFocusRing&&this.hasAttribute("focused")){this.focusElement.setAttribute("focus-ring","")}this._onClosed()}}_onOverlayTouchAction(){this._closeOnBlurIsPrevented=!0;this.inputElement.blur();this._closeOnBlurIsPrevented=!1}_onClick(e){this._closeOnBlurIsPrevented=!0;const path=e.composedPath();if(-1!==path.indexOf(this._clearElement)){this._clear();this.focus()}else if(-1!==path.indexOf(this.inputElement)){if(-1<path.indexOf(this._toggleElement)&&this.opened){this.close()}else{this.open()}}this._closeOnBlurIsPrevented=!1}_onKeyDown(e){if(this._isEventKey(e,"down")){this._closeOnBlurIsPrevented=!0;this._onArrowDown();this._closeOnBlurIsPrevented=!1;e.preventDefault()}else if(this._isEventKey(e,"up")){this._closeOnBlurIsPrevented=!0;this._onArrowUp();this._closeOnBlurIsPrevented=!1;e.preventDefault()}else if(this._isEventKey(e,"enter")){this._onEnter(e)}else if(this._isEventKey(e,"esc")){this._onEscape(e)}}_isEventKey(e,k){return iron_a11y_keys_behavior.a.keyboardEventMatchesKeys(e,k)}_getItemLabel(item){return this.$.overlay.getItemLabel(item)}_getItemValue(item){let value=item?this.get(this.itemValuePath,item):void 0;if(value===void 0){value=item?item.toString():""}return value}_onArrowDown(){if(this.opened){if(this.$.overlay._items){this._focusedIndex=_Mathmin(this.$.overlay._items.length-1,this._focusedIndex+1);this._prefillFocusedItemLabel()}}else{this.open()}}_onArrowUp(){if(this.opened){if(-1<this._focusedIndex){this._focusedIndex=_Mathmax(0,this._focusedIndex-1)}else{if(this.$.overlay._items){this._focusedIndex=this.$.overlay._items.length-1}}this._prefillFocusedItemLabel()}else{this.open()}}_prefillFocusedItemLabel(){if(-1<this._focusedIndex){this._inputElementValue="";setTimeout(()=>{this._inputElementValue=this._getItemLabel(this.$.overlay._focusedItem);this._markAllSelectionRange()},1)}}_setSelectionRange(start,end){const input=this._nativeInput||this.inputElement;if(this.hasAttribute("focused")&&input&&input.setSelectionRange){try{input.setSelectionRange(start,end)}catch(ignore){}}}_markAllSelectionRange(){if(this._inputElementValue!==void 0){this._setSelectionRange(0,this._inputElementValue.length)}}_clearSelectionRange(){if(this._inputElementValue!==void 0){const pos=this._inputElementValue?this._inputElementValue.length:0;this._setSelectionRange(pos,pos)}}_onEnter(e){if(this.opened&&(this.allowCustomValue||""===this._inputElementValue||-1<this._focusedIndex)){this.close();e.preventDefault()}}_onEscape(e){if(this.opened){this._stopPropagation(e);if(-1<this._focusedIndex){this._focusedIndex=-1;this._revertInputValue()}else{this.cancel()}}}_toggleElementChanged(toggleElement){if(toggleElement){toggleElement.addEventListener("mousedown",e=>e.preventDefault())}}_clear(){this.selectedItem=null;if(this.allowCustomValue){this.value=""}if(!this.opened){this._detectAndDispatchChange()}}cancel(){this._revertInputValueToValue();this._lastCommittedValue=this.value;this.close()}_onOpened(){Object(flush.b)();this.$.overlay.ensureItemsRendered();this.$.overlay._selector.toggleScrollListener(!0);this.$.overlay.updateViewportBoundaries();utils_async.c.run(()=>this.$.overlay.adjustScrollPosition());setTimeout(()=>this._resizeDropdown(),1);this._lastCommittedValue=this.value}_onClosed(){if(this.opened){this.close()}if(this.$.overlay._items&&-1<this._focusedIndex){const focusedItem=this.$.overlay._items[this._focusedIndex];if(this.selectedItem!==focusedItem){this.selectedItem=focusedItem}this._inputElementValue=this._getItemLabel(this.selectedItem)}else if(""===this._inputElementValue||this._inputElementValue===void 0){this.selectedItem=null;if(this.allowCustomValue){this.value=""}}else{if(this.allowCustomValue){const e=new CustomEvent("custom-value-set",{detail:this._inputElementValue,composed:!0,cancelable:!0,bubbles:!0});this.dispatchEvent(e);if(!e.defaultPrevented){const customValue=this._inputElementValue;this._selectItemForValue(customValue);this.value=customValue}}else{this._inputElementValue=this.selectedItem?this._getItemLabel(this.selectedItem):""}}this._detectAndDispatchChange();this._clearSelectionRange();if(!this.dataProvider){this.filter=""}}_inputValueChanged(e){if(-1!==e.composedPath().indexOf(this.inputElement)){this._inputElementValue=this.inputElement.value;this._filterFromInput()}}_filterFromInput(){if(!this.opened){this.open()}if(this.filter===this._inputElementValue){this._filterChanged(this.filter,this.itemValuePath,this.itemLabelPath)}else{this.filter=this._inputElementValue}}_filterChanged(filter,itemValuePath,itemLabelPath){if(filter===void 0||itemValuePath===void 0||itemLabelPath===void 0){return}if(this.items){this.filteredItems=this._filterItems(this.items,filter)}else{this._filteredItemsChanged({path:"filteredItems",value:this.filteredItems},itemValuePath,itemLabelPath)}}_loadingChanged(loading){if(loading){this._focusedIndex=-1}}_revertInputValue(){if(""!==this.filter){this._inputElementValue=this.filter}else{this._revertInputValueToValue()}this._clearSelectionRange()}_revertInputValueToValue(){if(this.allowCustomValue&&!this.selectedItem){this._inputElementValue=this.value}else{this._inputElementValue=this._getItemLabel(this.selectedItem)}}_resizeDropdown(){this.$.overlay.$.dropdown.notifyResize()}_updateHasValue(hasValue){if(hasValue){this.setAttribute("has-value","")}else{this.removeAttribute("has-value")}}_selectedItemChanged(selectedItem){if(null===selectedItem||selectedItem===void 0){if(this.filteredItems){if(!this.allowCustomValue){this.value=""}this._updateHasValue(""!==this.value);this._inputElementValue=this.value}}else{const value=this._getItemValue(selectedItem);if(this.value!==value){this.value=value}this._updateHasValue(!0);this._inputElementValue=this._getItemLabel(selectedItem);if(this.inputElement){this.inputElement.value=this._inputElementValue}}this.$.overlay._selectedItem=selectedItem;if(this.filteredItems&&this.$.overlay._items){this._focusedIndex=this.filteredItems.indexOf(selectedItem)}}_valueChanged(value,oldVal){if(""===value&&oldVal===void 0){return}if(this._isValidValue(value)){let item;if(this._getItemValue(this.selectedItem)!==value){this._selectItemForValue(value)}else{item=this.selectedItem}if(!item&&this.allowCustomValue){this._inputElementValue=value}this._updateHasValue(""!==this.value)}else{this.selectedItem=null}this._lastCommittedValue=void 0}_detectAndDispatchChange(){if(this.value!==this._lastCommittedValue){this.dispatchEvent(new CustomEvent("change",{bubbles:!0}));this._lastCommittedValue=this.value}}_itemsChanged(items,oldItems){this._ensureItemsOrDataProvider(()=>{this.items=oldItems})}_itemsOrPathsChanged(e,itemValuePath,itemLabelPath){if(e.value===void 0||itemValuePath===void 0||itemLabelPath===void 0){return}if("items"===e.path||"items.splices"===e.path){this.filteredItems=this.items?this.items.slice(0):this.items;const valueIndex=this._indexOfValue(this.value,this.items);this._focusedIndex=valueIndex;const item=-1<valueIndex&&this.items[valueIndex];if(item){this.selectedItem=item}}}_filteredItemsChanged(e,itemValuePath,itemLabelPath){if(e.value===void 0||itemValuePath===void 0||itemLabelPath===void 0){return}if("filteredItems"===e.path||"filteredItems.splices"===e.path){this._setOverlayItems(this.filteredItems);this._focusedIndex=this.opened?this.$.overlay.indexOfLabel(this.filter):this._indexOfValue(this.value,this.filteredItems);if(this.opened){this._repositionOverlay()}}}_filterItems(arr,filter){if(!arr){return arr}return arr.filter(item=>{filter=filter?filter.toString().toLowerCase():"";return-1<this._getItemLabel(item).toString().toLowerCase().indexOf(filter)})}_selectItemForValue(value){const valueIndex=this._indexOfValue(value,this.filteredItems);this.selectedItem=0<=valueIndex?this.filteredItems[valueIndex]:this.dataProvider&&this.selectedItem===void 0?void 0:null}_setOverlayItems(items){this.$.overlay.set("_items",items);if(this.opened){this._resizeDropdown()}}_repositionOverlay(){setTimeout(()=>{this._resizeDropdown();this.$.overlay.updateViewportBoundaries();this.$.overlay.ensureItemsRendered();this.$.overlay._selector.notifyResize();Object(flush.b)()},1)}_indexOfValue(value,items){if(items&&this._isValidValue(value)){for(let i=0;i<items.length;i++){if(this._getItemValue(items[i])===value){return i}}}return-1}_isValidValue(value){return value!==void 0&&null!==value}_overlaySelectedItemChanged(e){e.stopPropagation();if(e.detail.item instanceof ComboBoxPlaceholder){return}if(this.selectedItem!==e.detail.item){this.selectedItem=e.detail.item}if(this.opened){this.close()}}validate(){return!(this.invalid=!this.checkValidity())}checkValidity(){if(this.inputElement.validate){return this.inputElement.validate()}}get _instanceProps(){return{item:!0,index:!0,selected:!0,focused:!0}}_ensureTemplatized(){if(!this._TemplateClass){const tpl=this._itemTemplate||this.querySelector("template");if(tpl){this._TemplateClass=Object(templatize.b)(tpl,this,{instanceProps:this._instanceProps,forwardHostProp:function(prop,value){const items=this.$.overlay._selector.querySelectorAll("vaadin-combo-box-item");Array.prototype.forEach.call(items,item=>{if(item._itemTemplateInstance){item._itemTemplateInstance.set(prop,value);item._itemTemplateInstance.notifyPath(prop,value,!0)}})}})}}}_preventInputBlur(){if(this._toggleElement){this._toggleElement.addEventListener("click",this._preventDefault)}if(this._clearElement){this._clearElement.addEventListener("click",this._preventDefault)}}_restoreInputBlur(){if(this._toggleElement){this._toggleElement.removeEventListener("click",this._preventDefault)}if(this._clearElement){this._clearElement.removeEventListener("click",this._preventDefault)}}_preventDefault(e){e.preventDefault()}_stopPropagation(e){e.stopPropagation()}},ComboBoxDataProviderMixin=superClass=>class extends superClass{static get properties(){return{pageSize:{type:Number,value:50,observer:"_pageSizeChanged"},size:{type:Number,observer:"_sizeChanged"},dataProvider:{type:Object,observer:"_dataProviderChanged"},_pendingRequests:{value:()=>{return{}}}}}static get observers(){return["_dataProviderFilterChanged(filter, dataProvider)","_dataProviderClearFilter(dataProvider, opened, value)","_warnDataProviderValue(dataProvider, value)","_ensureFirstPage(opened)"]}_dataProviderClearFilter(dataProvider){if(dataProvider&&this.filter){this.size=void 0;this._pendingRequests={};this.filter="";this.clearCache()}}ready(){super.ready();this.clearCache();this.$.overlay.addEventListener("index-requested",e=>{const index=e.detail.index;if(index!==void 0){const page=this._getPageForIndex(index);if(!this._hasPage(page)){this._loadPage(page)}}})}_dataProviderFilterChanged(){if(this.dataProvider&&this.opened){this.size=void 0;this._pendingRequests={};this.clearCache()}}_ensureFirstPage(opened){if(opened&&!this._hasPage(0)){this._loadPage(0)}}_hasPage(page){if(!this.filteredItems){return!1}const loadedItem=this.filteredItems[page*this.pageSize];return loadedItem!==void 0&&!(loadedItem instanceof ComboBoxPlaceholder)}_loadPage(page){if(!this._pendingRequests[page]&&this.dataProvider){this.loading=!0;const params={page,pageSize:this.pageSize,filter:this.filter},callback=(items,size)=>{if(this._pendingRequests[page]===callback){if(!this.filteredItems){const filteredItems=[];filteredItems.splice(params.page*params.pageSize,items.length,...items);this.filteredItems=filteredItems}else{this.splice("filteredItems",params.page*params.pageSize,items.length,...items)}if(this._isValidValue(this.value)&&this._getItemValue(this.selectedItem)!==this.value){this._selectItemForValue(this.value)}this.size=size;delete this._pendingRequests[page];if(0===Object.keys(this._pendingRequests).length){this.loading=!1}}};this._pendingRequests[page]=callback;this.dataProvider(params,callback)}}_getPageForIndex(index){return _Mathfloor(index/this.pageSize)}clearCache(){if(!this.dataProvider){return}this._pendingRequests={};const filteredItems=[];for(let i=0;i<(this.size||0);i++){filteredItems.push(new ComboBoxPlaceholder)}this.filteredItems=filteredItems;if(this.opened){this._loadPage(0)}}_sizeChanged(size=0){const filteredItems=(this.filteredItems||[]).slice(0);for(let i=0;i<size;i++){filteredItems[i]=filteredItems[i]!==void 0?filteredItems[i]:new ComboBoxPlaceholder}this.filteredItems=filteredItems}_pageSizeChanged(pageSize,oldPageSize){if(_Mathfloor(pageSize)!==pageSize||0===pageSize){this.pageSize=oldPageSize;throw new Error("`pageSize` value must be an integer > 0")}this.clearCache()}_dataProviderChanged(dataProvider,oldDataProvider){this._ensureItemsOrDataProvider(()=>{this.dataProvider=oldDataProvider})}_ensureItemsOrDataProvider(restoreOldValueCallback){if(this.items!==void 0&&this.dataProvider!==void 0){restoreOldValueCallback();throw new Error("Using `items` and `dataProvider` together is not supported")}}_warnDataProviderValue(dataProvider,value){if(dataProvider&&""!==value&&(this.selectedItem===void 0||null===this.selectedItem)){const valueIndex=this._indexOfValue(value,this.filteredItems);if(0>valueIndex||!this._getItemLabel(this.filteredItems[valueIndex])){console.warn("Warning: unable to determine the label for the provided `value`. "+"Nothing to display in the text field. This usually happens when "+"setting an initial `value` before any items are returned from "+"the `dataProvider` callback. Consider setting `selectedItem` "+"instead of `value`")}}}};/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*//**
@license
Copyright (c) 2018 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/var polymer_legacy=__webpack_require__(2),iron_resizable_behavior=__webpack_require__(44),iron_scroll_target_behavior=__webpack_require__(149),mutable_data_behavior=__webpack_require__(97),polymer_fn=__webpack_require__(3),polymer_dom=__webpack_require__(1),templatizer_behavior=__webpack_require__(96),debounce=__webpack_require__(14),path=__webpack_require__(5),IOS=navigator.userAgent.match(/iP(?:hone|ad;(?: U;)? CPU) OS (\d+)/),IOS_TOUCH_SCROLLING=IOS&&8<=IOS[1],DEFAULT_PHYSICAL_COUNT=3,HIDDEN_Y="-10000px",SECRET_TABINDEX=-100,IS_V2=null!=flush.b,ANIMATION_FRAME=IS_V2?utils_async.a:0,IDLE_TIME=IS_V2?utils_async.b:1,MICRO_TASK=IS_V2?utils_async.c:2;/**
@license
Copyright (c) 2016 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/if(!mutable_data_behavior.a){Polymer.OptionalMutableDataBehavior={}}Object(polymer_fn.a)({_template:html_tag.a`
    <style>
      :host {
        display: block;
      }

      @media only screen and (-webkit-max-device-pixel-ratio: 1) {
        :host {
          will-change: transform;
        }
      }

      #items {
        @apply --iron-list-items-container;
        position: relative;
      }

      :host(:not([grid])) #items > ::slotted(*) {
        width: 100%;
      }

      #items > ::slotted(*) {
        box-sizing: border-box;
        margin: 0;
        position: absolute;
        top: 0;
        will-change: transform;
      }
    </style>

    <array-selector id="selector" items="{{items}}" selected="{{selectedItems}}" selected-item="{{selectedItem}}"></array-selector>

    <div id="items">
      <slot></slot>
    </div>
`,is:"iron-list",properties:{items:{type:Array},as:{type:String,value:"item"},indexAs:{type:String,value:"index"},selectedAs:{type:String,value:"selected"},grid:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_gridChanged"},selectionEnabled:{type:Boolean,value:!1},selectedItem:{type:Object,notify:!0},selectedItems:{type:Object,notify:!0},multiSelection:{type:Boolean,value:!1},scrollOffset:{type:Number,value:0}},observers:["_itemsChanged(items.*)","_selectionEnabledChanged(selectionEnabled)","_multiSelectionChanged(multiSelection)","_setOverflow(scrollTarget, scrollOffset)"],behaviors:[templatizer_behavior.a,iron_resizable_behavior.a,iron_scroll_target_behavior.a,mutable_data_behavior.a],_ratio:.5,_scrollerPaddingTop:0,_scrollPosition:0,_physicalSize:0,_physicalAverage:0,_physicalAverageCount:0,_physicalTop:0,_virtualCount:0,_estScrollHeight:0,_scrollHeight:0,_viewportHeight:0,_viewportWidth:0,_physicalItems:null,_physicalSizes:null,_firstVisibleIndexVal:null,_collection:null,_lastVisibleIndexVal:null,_maxPages:2,_focusedItem:null,_focusedVirtualIndex:-1,_focusedPhysicalIndex:-1,_offscreenFocusedItem:null,_focusBackfillItem:null,_itemsPerRow:1,_itemWidth:0,_rowHeight:0,_templateCost:0,_parentModel:!0,get _physicalBottom(){return this._physicalTop+this._physicalSize},get _scrollBottom(){return this._scrollPosition+this._viewportHeight},get _virtualEnd(){return this._virtualStart+this._physicalCount-1},get _hiddenContentSize(){var size=this.grid?this._physicalRows*this._rowHeight:this._physicalSize;return size-this._viewportHeight},get _itemsParent(){return Object(polymer_dom.b)(Object(polymer_dom.b)(this._userTemplate).parentNode)},get _maxScrollTop(){return this._estScrollHeight-this._viewportHeight+this._scrollOffset},get _maxVirtualStart(){var virtualCount=this._convertIndexToCompleteRow(this._virtualCount);return _Mathmax(0,virtualCount-this._physicalCount)},set _virtualStart(val){val=this._clamp(val,0,this._maxVirtualStart);if(this.grid){val=val-val%this._itemsPerRow}this._virtualStartVal=val},get _virtualStart(){return this._virtualStartVal||0},set _physicalStart(val){val=val%this._physicalCount;if(0>val){val=this._physicalCount+val}if(this.grid){val=val-val%this._itemsPerRow}this._physicalStartVal=val},get _physicalStart(){return this._physicalStartVal||0},get _physicalEnd(){return(this._physicalStart+this._physicalCount-1)%this._physicalCount},set _physicalCount(val){this._physicalCountVal=val},get _physicalCount(){return this._physicalCountVal||0},get _optPhysicalSize(){return 0===this._viewportHeight?Infinity:this._viewportHeight*this._maxPages},get _isVisible(){return!!(this.offsetWidth||this.offsetHeight)},get firstVisibleIndex(){var idx=this._firstVisibleIndexVal;if(null==idx){var physicalOffset=this._physicalTop+this._scrollOffset;idx=this._iterateItems(function(pidx,vidx){physicalOffset+=this._getPhysicalSizeIncrement(pidx);if(physicalOffset>this._scrollPosition){return this.grid?vidx-vidx%this._itemsPerRow:vidx}if(this.grid&&this._virtualCount-1===vidx){return vidx-vidx%this._itemsPerRow}})||0;this._firstVisibleIndexVal=idx}return idx},get lastVisibleIndex(){var idx=this._lastVisibleIndexVal;if(null==idx){if(this.grid){idx=_Mathmin(this._virtualCount,this.firstVisibleIndex+this._estRowsInView*this._itemsPerRow-1)}else{var physicalOffset=this._physicalTop+this._scrollOffset;this._iterateItems(function(pidx,vidx){if(physicalOffset<this._scrollBottom){idx=vidx}physicalOffset+=this._getPhysicalSizeIncrement(pidx)})}this._lastVisibleIndexVal=idx}return idx},get _defaultScrollTarget(){return this},get _virtualRowCount(){return _Mathceil(this._virtualCount/this._itemsPerRow)},get _estRowsInView(){return _Mathceil(this._viewportHeight/this._rowHeight)},get _physicalRows(){return _Mathceil(this._physicalCount/this._itemsPerRow)},get _scrollOffset(){return this._scrollerPaddingTop+this.scrollOffset},ready:function(){this.addEventListener("focus",this._didFocus.bind(this),!0)},attached:function(){this._debounce("_render",this._render,ANIMATION_FRAME);this.listen(this,"iron-resize","_resizeHandler");this.listen(this,"keydown","_keydownHandler")},detached:function(){this.unlisten(this,"iron-resize","_resizeHandler");this.unlisten(this,"keydown","_keydownHandler")},_setOverflow:function(scrollTarget){this.style.webkitOverflowScrolling=scrollTarget===this?"touch":"";this.style.overflowY=scrollTarget===this?"auto":"";this._lastVisibleIndexVal=null;this._firstVisibleIndexVal=null;this._debounce("_render",this._render,ANIMATION_FRAME)},updateViewportBoundaries:function(){var styles=window.getComputedStyle(this);this._scrollerPaddingTop=this.scrollTarget===this?0:parseInt(styles["padding-top"],10);this._isRTL=!!("rtl"===styles.direction);this._viewportWidth=this.$.items.offsetWidth;this._viewportHeight=this._scrollTargetHeight;this.grid&&this._updateGridMetrics()},_scrollHandler:function(){var scrollTop=_Mathmax(0,_Mathmin(this._maxScrollTop,this._scrollTop)),delta=scrollTop-this._scrollPosition,isScrollingDown=0<=delta;this._scrollPosition=scrollTop;this._firstVisibleIndexVal=null;this._lastVisibleIndexVal=null;if(_Mathabs(delta)>this._physicalSize&&0<this._physicalSize){delta=delta-this._scrollOffset;var idxAdjustment=_Mathround(delta/this._physicalAverage)*this._itemsPerRow;this._virtualStart=this._virtualStart+idxAdjustment;this._physicalStart=this._physicalStart+idxAdjustment;this._physicalTop=_Mathfloor(this._virtualStart/this._itemsPerRow)*this._physicalAverage;this._update()}else if(0<this._physicalCount){var reusables=this._getReusables(isScrollingDown);if(isScrollingDown){this._physicalTop=reusables.physicalTop;this._virtualStart=this._virtualStart+reusables.indexes.length;this._physicalStart=this._physicalStart+reusables.indexes.length}else{this._virtualStart=this._virtualStart-reusables.indexes.length;this._physicalStart=this._physicalStart-reusables.indexes.length}this._update(reusables.indexes,isScrollingDown?null:reusables.indexes);this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,0),MICRO_TASK)}},_getReusables:function(fromTop){var ith,offsetContent,physicalItemHeight,idxs=[],protectedOffsetContent=this._hiddenContentSize*this._ratio,virtualStart=this._virtualStart,virtualEnd=this._virtualEnd,physicalCount=this._physicalCount,top=this._physicalTop+this._scrollOffset,bottom=this._physicalBottom+this._scrollOffset,scrollTop=this._scrollTop,scrollBottom=this._scrollBottom;if(fromTop){ith=this._physicalStart;this._physicalEnd;offsetContent=scrollTop-top}else{ith=this._physicalEnd;this._physicalStart;offsetContent=bottom-scrollBottom}while(!0){physicalItemHeight=this._getPhysicalSizeIncrement(ith);offsetContent=offsetContent-physicalItemHeight;if(idxs.length>=physicalCount||offsetContent<=protectedOffsetContent){break}if(fromTop){if(virtualEnd+idxs.length+1>=this._virtualCount){break}if(top+physicalItemHeight>=scrollTop-this._scrollOffset){break}idxs.push(ith);top=top+physicalItemHeight;ith=(ith+1)%physicalCount}else{if(0>=virtualStart-idxs.length){break}if(top+this._physicalSize-physicalItemHeight<=scrollBottom){break}idxs.push(ith);top=top-physicalItemHeight;ith=0===ith?physicalCount-1:ith-1}}return{indexes:idxs,physicalTop:top-this._scrollOffset}},_update:function(itemSet,movingUp){if(itemSet&&0===itemSet.length||0===this._physicalCount){return}this._manageFocus();this._assignModels(itemSet);this._updateMetrics(itemSet);if(movingUp){while(movingUp.length){var idx=movingUp.pop();this._physicalTop-=this._getPhysicalSizeIncrement(idx)}}this._positionItems();this._updateScrollerSize()},_createPool:function(size){this._ensureTemplatized();var i,inst,physicalItems=Array(size);for(i=0;i<size;i++){inst=this.stamp(null);physicalItems[i]=inst.root.querySelector("*");this._itemsParent.appendChild(inst.root)}return physicalItems},_isClientFull:function(){return 0!=this._scrollBottom&&this._physicalBottom-1>=this._scrollBottom&&this._physicalTop<=this._scrollPosition},_increasePoolIfNeeded:function(count){var nextPhysicalCount=this._clamp(this._physicalCount+count,DEFAULT_PHYSICAL_COUNT,this._virtualCount-this._virtualStart);nextPhysicalCount=this._convertIndexToCompleteRow(nextPhysicalCount);if(this.grid){var correction=nextPhysicalCount%this._itemsPerRow;if(correction&&nextPhysicalCount-correction<=this._physicalCount){nextPhysicalCount+=this._itemsPerRow}nextPhysicalCount-=correction}var delta=nextPhysicalCount-this._physicalCount,nextIncrease=_Mathround(.5*this._physicalCount);if(0>delta){return}if(0<delta){var ts=window.performance.now();[].push.apply(this._physicalItems,this._createPool(delta));for(var i=0;i<delta;i++){this._physicalSizes.push(0)}this._physicalCount=this._physicalCount+delta;if(this._physicalStart>this._physicalEnd&&this._isIndexRendered(this._focusedVirtualIndex)&&this._getPhysicalIndex(this._focusedVirtualIndex)<this._physicalEnd){this._physicalStart=this._physicalStart+delta}this._update();this._templateCost=(window.performance.now()-ts)/delta;nextIncrease=_Mathround(.5*this._physicalCount)}if(this._virtualEnd>=this._virtualCount-1||0===nextIncrease){}else if(!this._isClientFull()){this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,nextIncrease),MICRO_TASK)}else if(this._physicalSize<this._optPhysicalSize){this._debounce("_increasePoolIfNeeded",this._increasePoolIfNeeded.bind(this,this._clamp(_Mathround(50/this._templateCost),1,nextIncrease)),IDLE_TIME)}},_render:function(){if(!this.isAttached||!this._isVisible){return}if(0!==this._physicalCount){var reusables=this._getReusables(!0);this._physicalTop=reusables.physicalTop;this._virtualStart=this._virtualStart+reusables.indexes.length;this._physicalStart=this._physicalStart+reusables.indexes.length;this._update(reusables.indexes);this._update();this._increasePoolIfNeeded(0)}else if(0<this._virtualCount){this.updateViewportBoundaries();this._increasePoolIfNeeded(DEFAULT_PHYSICAL_COUNT)}},_ensureTemplatized:function(){if(this.ctor){return}this._userTemplate=this.queryEffectiveChildren("template");if(!this._userTemplate){console.warn("iron-list requires a template to be provided in light-dom")}var instanceProps={__key__:!0};instanceProps[this.as]=!0;instanceProps[this.indexAs]=!0;instanceProps[this.selectedAs]=!0;instanceProps.tabIndex=!0;this._instanceProps=instanceProps;this.templatize(this._userTemplate,this.mutableData)},_gridChanged:function(newGrid,oldGrid){if("undefined"===typeof oldGrid)return;this.notifyResize();flush.b?Object(flush.b)():Object(polymer_dom.c)();newGrid&&this._updateGridMetrics()},_itemsChanged:function(change){if("items"===change.path){this._virtualStart=0;this._physicalTop=0;this._virtualCount=this.items?this.items.length:0;this._collection=null;this._physicalIndexForKey={};this._firstVisibleIndexVal=null;this._lastVisibleIndexVal=null;this._physicalCount=this._physicalCount||0;this._physicalItems=this._physicalItems||[];this._physicalSizes=this._physicalSizes||[];this._physicalStart=0;if(this._scrollTop>this._scrollOffset){this._resetScrollPosition(0)}this._removeFocusedItem();this._debounce("_render",this._render,ANIMATION_FRAME)}else if("items.splices"===change.path){this._adjustVirtualIndex(change.value.indexSplices);this._virtualCount=this.items?this.items.length:0;var itemAddedOrRemoved=change.value.indexSplices.some(function(splice){return 0<splice.addedCount||0<splice.removed.length});if(itemAddedOrRemoved){var activeElement=this._getActiveElement();if(this.contains(activeElement)){activeElement.blur()}}var affectedIndexRendered=change.value.indexSplices.some(function(splice){return splice.index+splice.addedCount>=this._virtualStart&&splice.index<=this._virtualEnd},this);if(!this._isClientFull()||affectedIndexRendered){this._debounce("_render",this._render,ANIMATION_FRAME)}}else if("items.length"!==change.path){this._forwardItemPath(change.path,change.value)}},_forwardItemPath:function(path,value){path=path.slice(6);var dot=path.indexOf(".");if(-1===dot){dot=path.length}var isIndexRendered,pidx,inst,offscreenInstance=this.modelForElement(this._offscreenFocusedItem);if(IS_V2){var vidx=parseInt(path.substring(0,dot),10);isIndexRendered=this._isIndexRendered(vidx);if(isIndexRendered){pidx=this._getPhysicalIndex(vidx);inst=this.modelForElement(this._physicalItems[pidx])}else if(offscreenInstance){inst=offscreenInstance}if(!inst||inst[this.indexAs]!==vidx){return}}else{var key=path.substring(0,dot);if(offscreenInstance&&offscreenInstance.__key__===key){inst=offscreenInstance}else{pidx=this._physicalIndexForKey[key];inst=this.modelForElement(this._physicalItems[pidx]);if(!inst||inst.__key__!==key){return}}}path=path.substring(dot+1);path=this.as+(path?"."+path:"");IS_V2?inst._setPendingPropertyOrPath(path,value,!1,!0):inst.notifyPath(path,value,!0);inst._flushProperties&&inst._flushProperties(!0);if(isIndexRendered){this._updateMetrics([pidx]);this._positionItems();this._updateScrollerSize()}},_adjustVirtualIndex:function(splices){splices.forEach(function(splice){splice.removed.forEach(this._removeItem,this);if(splice.index<this._virtualStart){var delta=_Mathmax(splice.addedCount-splice.removed.length,splice.index-this._virtualStart);this._virtualStart=this._virtualStart+delta;if(0<=this._focusedVirtualIndex){this._focusedVirtualIndex=this._focusedVirtualIndex+delta}}},this)},_removeItem:function(item){this.$.selector.deselect(item);if(this._focusedItem&&this.modelForElement(this._focusedItem)[this.as]===item){this._removeFocusedItem()}},_iterateItems:function(fn,itemSet){var pidx,vidx,rtn,i;if(2===arguments.length&&itemSet){for(i=0;i<itemSet.length;i++){pidx=itemSet[i];vidx=this._computeVidx(pidx);if(null!=(rtn=fn.call(this,pidx,vidx))){return rtn}}}else{pidx=this._physicalStart;vidx=this._virtualStart;for(;pidx<this._physicalCount;pidx++,vidx++){if(null!=(rtn=fn.call(this,pidx,vidx))){return rtn}}for(pidx=0;pidx<this._physicalStart;pidx++,vidx++){if(null!=(rtn=fn.call(this,pidx,vidx))){return rtn}}}},_computeVidx:function(pidx){if(pidx>=this._physicalStart){return this._virtualStart+(pidx-this._physicalStart)}return this._virtualStart+(this._physicalCount-this._physicalStart)+pidx},_assignModels:function(itemSet){this._iterateItems(function(pidx,vidx){var el=this._physicalItems[pidx],item=this.items&&this.items[vidx];if(null!=item){var inst=this.modelForElement(el);inst.__key__=this._collection?this._collection.getKey(item):null;this._forwardProperty(inst,this.as,item);this._forwardProperty(inst,this.selectedAs,this.$.selector.isSelected(item));this._forwardProperty(inst,this.indexAs,vidx);this._forwardProperty(inst,"tabIndex",this._focusedVirtualIndex===vidx?0:-1);this._physicalIndexForKey[inst.__key__]=pidx;inst._flushProperties&&inst._flushProperties(!0);el.removeAttribute("hidden")}else{el.setAttribute("hidden","")}},itemSet)},_updateMetrics:function(itemSet){flush.b?Object(flush.b)():Object(polymer_dom.c)();var newPhysicalSize=0,oldPhysicalSize=0,prevAvgCount=this._physicalAverageCount,prevPhysicalAvg=this._physicalAverage;this._iterateItems(function(pidx){oldPhysicalSize+=this._physicalSizes[pidx];this._physicalSizes[pidx]=this._physicalItems[pidx].offsetHeight;newPhysicalSize+=this._physicalSizes[pidx];this._physicalAverageCount+=this._physicalSizes[pidx]?1:0},itemSet);if(this.grid){this._updateGridMetrics();this._physicalSize=_Mathceil(this._physicalCount/this._itemsPerRow)*this._rowHeight}else{oldPhysicalSize=1===this._itemsPerRow?oldPhysicalSize:_Mathceil(this._physicalCount/this._itemsPerRow)*this._rowHeight;this._physicalSize=this._physicalSize+newPhysicalSize-oldPhysicalSize;this._itemsPerRow=1}if(this._physicalAverageCount!==prevAvgCount){this._physicalAverage=_Mathround((prevPhysicalAvg*prevAvgCount+newPhysicalSize)/this._physicalAverageCount)}},_updateGridMetrics:function(){this._itemWidth=0<this._physicalCount?this._physicalItems[0].getBoundingClientRect().width:200;this._rowHeight=0<this._physicalCount?this._physicalItems[0].offsetHeight:200;this._itemsPerRow=this._itemWidth?_Mathfloor(this._viewportWidth/this._itemWidth):this._itemsPerRow},_positionItems:function(){this._adjustScrollPosition();var y=this._physicalTop;if(this.grid){var totalItemWidth=this._itemsPerRow*this._itemWidth,rowOffset=(this._viewportWidth-totalItemWidth)/2;this._iterateItems(function(pidx,vidx){var modulus=vidx%this._itemsPerRow,x=_Mathfloor(modulus*this._itemWidth+rowOffset);if(this._isRTL){x=-1*x}this.translate3d(x+"px",y+"px",0,this._physicalItems[pidx]);if(this._shouldRenderNextRow(vidx)){y+=this._rowHeight}})}else{this._iterateItems(function(pidx){this.translate3d(0,y+"px",0,this._physicalItems[pidx]);y+=this._physicalSizes[pidx]})}},_getPhysicalSizeIncrement:function(pidx){if(!this.grid){return this._physicalSizes[pidx]}if(this._computeVidx(pidx)%this._itemsPerRow!==this._itemsPerRow-1){return 0}return this._rowHeight},_shouldRenderNextRow:function(vidx){return vidx%this._itemsPerRow===this._itemsPerRow-1},_adjustScrollPosition:function(){var deltaHeight=0===this._virtualStart?this._physicalTop:_Mathmin(this._scrollPosition+this._physicalTop,0);if(0!==deltaHeight){this._physicalTop=this._physicalTop-deltaHeight;var scrollTop=this._scrollTop;if(!IOS_TOUCH_SCROLLING&&0<scrollTop){this._resetScrollPosition(scrollTop-deltaHeight)}}},_resetScrollPosition:function(pos){if(this.scrollTarget&&0<=pos){this._scrollTop=pos;this._scrollPosition=this._scrollTop}},_updateScrollerSize:function(forceUpdate){if(this.grid){this._estScrollHeight=this._virtualRowCount*this._rowHeight}else{this._estScrollHeight=this._physicalBottom+_Mathmax(this._virtualCount-this._physicalCount-this._virtualStart,0)*this._physicalAverage}forceUpdate=forceUpdate||0===this._scrollHeight;forceUpdate=forceUpdate||this._scrollPosition>=this._estScrollHeight-this._physicalSize;forceUpdate=forceUpdate||this.grid&&this.$.items.style.height<this._estScrollHeight;if(forceUpdate||_Mathabs(this._estScrollHeight-this._scrollHeight)>=this._viewportHeight){this.$.items.style.height=this._estScrollHeight+"px";this._scrollHeight=this._estScrollHeight}},scrollToItem:function(item){return this.scrollToIndex(this.items.indexOf(item))},scrollToIndex:function(idx){if("number"!==typeof idx||0>idx||idx>this.items.length-1){return}flush.b?Object(flush.b)():Object(polymer_dom.c)();if(0===this._physicalCount){return}idx=this._clamp(idx,0,this._virtualCount-1);if(!this._isIndexRendered(idx)||idx>=this._maxVirtualStart){this._virtualStart=this.grid?idx-2*this._itemsPerRow:idx-1}this._manageFocus();this._assignModels();this._updateMetrics();this._physicalTop=_Mathfloor(this._virtualStart/this._itemsPerRow)*this._physicalAverage;var currentTopItem=this._physicalStart,currentVirtualItem=this._virtualStart,targetOffsetTop=0,hiddenContentSize=this._hiddenContentSize;while(currentVirtualItem<idx&&targetOffsetTop<=hiddenContentSize){targetOffsetTop=targetOffsetTop+this._getPhysicalSizeIncrement(currentTopItem);currentTopItem=(currentTopItem+1)%this._physicalCount;currentVirtualItem++}this._updateScrollerSize(!0);this._positionItems();this._resetScrollPosition(this._physicalTop+this._scrollOffset+targetOffsetTop);this._increasePoolIfNeeded(0);this._firstVisibleIndexVal=null;this._lastVisibleIndexVal=null},_resetAverage:function(){this._physicalAverage=0;this._physicalAverageCount=0},_resizeHandler:function(){this._debounce("_render",function(){this._firstVisibleIndexVal=null;this._lastVisibleIndexVal=null;_Mathabs(this._viewportHeight-this._scrollTargetHeight);this.updateViewportBoundaries();if(this._isVisible){this.toggleScrollListener(!0);this._resetAverage();this._render()}else{this.toggleScrollListener(!1)}},ANIMATION_FRAME)},selectItem:function(item){return this.selectIndex(this.items.indexOf(item))},selectIndex:function(index){if(0>index||index>=this._virtualCount){return}if(!this.multiSelection&&this.selectedItem){this.clearSelection()}if(this._isIndexRendered(index)){var model=this.modelForElement(this._physicalItems[this._getPhysicalIndex(index)]);if(model){model[this.selectedAs]=!0}this.updateSizeForIndex(index)}if(this.$.selector.selectIndex){this.$.selector.selectIndex(index)}else{this.$.selector.select(this.items[index])}},deselectItem:function(item){return this.deselectIndex(this.items.indexOf(item))},deselectIndex:function(index){if(0>index||index>=this._virtualCount){return}if(this._isIndexRendered(index)){var model=this.modelForElement(this._physicalItems[this._getPhysicalIndex(index)]);model[this.selectedAs]=!1;this.updateSizeForIndex(index)}if(this.$.selector.deselectIndex){this.$.selector.deselectIndex(index)}else{this.$.selector.deselect(this.items[index])}},toggleSelectionForItem:function(item){return this.toggleSelectionForIndex(this.items.indexOf(item))},toggleSelectionForIndex:function(index){var isSelected=this.$.selector.isIndexSelected?this.$.selector.isIndexSelected(index):this.$.selector.isSelected(this.items[index]);isSelected?this.deselectIndex(index):this.selectIndex(index)},clearSelection:function(){this._iterateItems(function(pidx){this.modelForElement(this._physicalItems[pidx])[this.selectedAs]=!1});this.$.selector.clearSelection()},_selectionEnabledChanged:function(selectionEnabled){var handler=selectionEnabled?this.listen:this.unlisten;handler.call(this,this,"tap","_selectionHandler")},_selectionHandler:function(e){var model=this.modelForElement(e.target);if(!model){return}var modelTabIndex,activeElTabIndex,target=Object(polymer_dom.b)(e).path[0],activeEl=this._getActiveElement(),physicalItem=this._physicalItems[this._getPhysicalIndex(model[this.indexAs])];if("input"===target.localName||"button"===target.localName||"select"===target.localName){return}modelTabIndex=model.tabIndex;model.tabIndex=SECRET_TABINDEX;activeElTabIndex=activeEl?activeEl.tabIndex:-1;model.tabIndex=modelTabIndex;if(activeEl&&physicalItem!==activeEl&&physicalItem.contains(activeEl)&&activeElTabIndex!==SECRET_TABINDEX){return}this.toggleSelectionForItem(model[this.as])},_multiSelectionChanged:function(multiSelection){this.clearSelection();this.$.selector.multi=multiSelection},updateSizeForItem:function(item){return this.updateSizeForIndex(this.items.indexOf(item))},updateSizeForIndex:function(index){if(!this._isIndexRendered(index)){return null}this._updateMetrics([this._getPhysicalIndex(index)]);this._positionItems();return null},_manageFocus:function(){var fidx=this._focusedVirtualIndex;if(0<=fidx&&fidx<this._virtualCount){if(this._isIndexRendered(fidx)){this._restoreFocusedItem()}else{this._createFocusBackfillItem()}}else if(0<this._virtualCount&&0<this._physicalCount){this._focusedPhysicalIndex=this._physicalStart;this._focusedVirtualIndex=this._virtualStart;this._focusedItem=this._physicalItems[this._physicalStart]}},_convertIndexToCompleteRow:function(idx){this._itemsPerRow=this._itemsPerRow||1;return this.grid?_Mathceil(idx/this._itemsPerRow)*this._itemsPerRow:idx},_isIndexRendered:function(idx){return idx>=this._virtualStart&&idx<=this._virtualEnd},_isIndexVisible:function(idx){return idx>=this.firstVisibleIndex&&idx<=this.lastVisibleIndex},_getPhysicalIndex:function(vidx){return IS_V2?(this._physicalStart+(vidx-this._virtualStart))%this._physicalCount:this._physicalIndexForKey[this._collection.getKey(this.items[vidx])]},focusItem:function(idx){this._focusPhysicalItem(idx)},_focusPhysicalItem:function(idx){if(0>idx||idx>=this._virtualCount){return}this._restoreFocusedItem();if(!this._isIndexRendered(idx)){this.scrollToIndex(idx)}var physicalItem=this._physicalItems[this._getPhysicalIndex(idx)],model=this.modelForElement(physicalItem),focusable;model.tabIndex=SECRET_TABINDEX;if(physicalItem.tabIndex===SECRET_TABINDEX){focusable=physicalItem}if(!focusable){focusable=Object(polymer_dom.b)(physicalItem).querySelector("[tabindex=\""+SECRET_TABINDEX+"\"]")}model.tabIndex=0;this._focusedVirtualIndex=idx;focusable&&focusable.focus()},_removeFocusedItem:function(){if(this._offscreenFocusedItem){this._itemsParent.removeChild(this._offscreenFocusedItem)}this._offscreenFocusedItem=null;this._focusBackfillItem=null;this._focusedItem=null;this._focusedVirtualIndex=-1;this._focusedPhysicalIndex=-1},_createFocusBackfillItem:function(){var fpidx=this._focusedPhysicalIndex;if(this._offscreenFocusedItem||0>this._focusedVirtualIndex){return}if(!this._focusBackfillItem){var inst=this.stamp(null);this._focusBackfillItem=inst.root.querySelector("*");this._itemsParent.appendChild(inst.root)}this._offscreenFocusedItem=this._physicalItems[fpidx];this.modelForElement(this._offscreenFocusedItem).tabIndex=0;this._physicalItems[fpidx]=this._focusBackfillItem;this._focusedPhysicalIndex=fpidx;this.translate3d(0,HIDDEN_Y,0,this._offscreenFocusedItem)},_restoreFocusedItem:function(){if(!this._offscreenFocusedItem||0>this._focusedVirtualIndex){return}this._assignModels();var fpidx=this._focusedPhysicalIndex=this._getPhysicalIndex(this._focusedVirtualIndex),onScreenItem=this._physicalItems[fpidx];if(!onScreenItem){return}var onScreenInstance=this.modelForElement(onScreenItem),offScreenInstance=this.modelForElement(this._offscreenFocusedItem);if(onScreenInstance[this.as]===offScreenInstance[this.as]){this._focusBackfillItem=onScreenItem;onScreenInstance.tabIndex=-1;this._physicalItems[fpidx]=this._offscreenFocusedItem;this.translate3d(0,HIDDEN_Y,0,this._focusBackfillItem)}else{this._removeFocusedItem();this._focusBackfillItem=null}this._offscreenFocusedItem=null},_didFocus:function(e){var targetModel=this.modelForElement(e.target),focusedModel=this.modelForElement(this._focusedItem),hasOffscreenFocusedItem=null!==this._offscreenFocusedItem,fidx=this._focusedVirtualIndex;if(!targetModel){return}if(focusedModel===targetModel){if(!this._isIndexVisible(fidx)){this.scrollToIndex(fidx)}}else{this._restoreFocusedItem();if(focusedModel){focusedModel.tabIndex=-1}targetModel.tabIndex=0;fidx=targetModel[this.indexAs];this._focusedVirtualIndex=fidx;this._focusedPhysicalIndex=this._getPhysicalIndex(fidx);this._focusedItem=this._physicalItems[this._focusedPhysicalIndex];if(hasOffscreenFocusedItem&&!this._offscreenFocusedItem){this._update()}}},_keydownHandler:function(e){switch(e.keyCode){case 40:if(this._focusedVirtualIndex<this._virtualCount-1)e.preventDefault();this._focusPhysicalItem(this._focusedVirtualIndex+(this.grid?this._itemsPerRow:1));break;case 39:if(this.grid)this._focusPhysicalItem(this._focusedVirtualIndex+(this._isRTL?-1:1));break;case 38:if(0<this._focusedVirtualIndex)e.preventDefault();this._focusPhysicalItem(this._focusedVirtualIndex-(this.grid?this._itemsPerRow:1));break;case 37:if(this.grid)this._focusPhysicalItem(this._focusedVirtualIndex+(this._isRTL?1:-1));break;case 13:this._focusPhysicalItem(this._focusedVirtualIndex);if(this.selectionEnabled)this._selectionHandler(e);break;}},_clamp:function(v,min,max){return _Mathmin(max,_Mathmax(min,v))},_debounce:function(name,cb,asyncModule){if(IS_V2){this._debouncers=this._debouncers||{};this._debouncers[name]=debounce.a.debounce(this._debouncers[name],asyncModule,cb.bind(this));Object(flush.a)(this._debouncers[name])}else{Object(polymer_dom.a)(this.debounce(name,cb))}},_forwardProperty:function(inst,name,value){if(IS_V2){inst._setPendingProperty(name,value)}else{inst[name]=value}},_forwardHostPropV2:function(prop,value){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach(function(item){if(item){this.modelForElement(item).forwardHostProp(prop,value)}},this)},_notifyInstancePropV2:function(inst,prop,value){if(Object(path.e)(this.as,prop)){var idx=inst[this.indexAs];if(prop==this.as){this.items[idx]=value}this.notifyPath(Object(path.i)(this.as,"items."+idx,prop),value)}},_getStampedChildren:function(){return this._physicalItems},_forwardInstancePath:function(inst,path,value){if(0===path.indexOf(this.as+".")){this.notifyPath("items."+inst.__key__+"."+path.slice(this.as.length+1),value)}},_forwardParentPath:function(path,value){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach(function(item){if(item){this.modelForElement(item).notifyPath(path,value,!0)}},this)},_forwardParentProp:function(prop,value){(this._physicalItems||[]).concat([this._offscreenFocusedItem,this._focusBackfillItem]).forEach(function(item){if(item){this.modelForElement(item)[prop]=value}},this)},_getActiveElement:function(){var itemsHost=this._itemsParent.node.domHost;return Object(polymer_dom.b)(itemsHost?itemsHost.root:document).activeElement}});/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_combo_box_item_ComboBoxItemElement extends Object(vaadin_themable_mixin.a)(polymer_element.a){static get template(){return html_tag.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
         display: none;
      }
    </style>
    <div part="content" id="content"></div>
`}static get is(){return"vaadin-combo-box-item"}static get properties(){return{index:Number,item:Object,label:String,selected:{type:Boolean,value:!1,reflectToAttribute:!0},focused:{type:Boolean,value:!1,reflectToAttribute:!0},_itemTemplateInstance:Object,renderer:Function,_oldRenderer:Function}}static get observers(){return["_rendererOrItemChanged(renderer, index, item.*)","_updateLabel(label, _itemTemplateInstance)","_updateTemplateInstanceVariable(\"index\", index, _itemTemplateInstance)","_updateTemplateInstanceVariable(\"item\", item, _itemTemplateInstance)","_updateTemplateInstanceVariable(\"selected\", selected, _itemTemplateInstance)","_updateTemplateInstanceVariable(\"focused\", focused, _itemTemplateInstance)"]}connectedCallback(){super.connectedCallback();if(!this._itemTemplateInstance){const overlay=this.getRootNode().host.getRootNode().host,dropdown=overlay.__dataHost,comboBoxOverlay=dropdown.getRootNode().host;this._comboBox=comboBoxOverlay.getRootNode().host;this._comboBox._ensureTemplatized();if(this._comboBox._TemplateClass){this._itemTemplateInstance=new this._comboBox._TemplateClass({});this.$.content.textContent="";this.$.content.appendChild(this._itemTemplateInstance.root)}}}_render(){if(!this.renderer){return}const model={index:this.index,item:this.item};this.renderer(this.$.content,this._comboBox,model)}_rendererOrItemChanged(renderer,index,item){if(item===void 0||index===void 0){return}if(this._oldRenderer!==renderer){this.$.content.innerHTML=""}if(renderer){this._oldRenderer=renderer;this._render()}}_updateLabel(label,_itemTemplateInstance){if(_itemTemplateInstance===void 0&&this.$.content&&!this.renderer){this.$.content.textContent=label}}_updateTemplateInstanceVariable(variable,value,_itemTemplateInstance){if(variable===void 0||value===void 0||_itemTemplateInstance===void 0){return}_itemTemplateInstance[variable]=value}}customElements.define(vaadin_combo_box_item_ComboBoxItemElement.is,vaadin_combo_box_item_ComboBoxItemElement);var legacy_class=__webpack_require__(55);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_combo_box_dropdown_ComboBoxOverlayElement extends vaadin_overlay.a{static get is(){return"vaadin-combo-box-overlay"}ready(){super.ready();const loader=document.createElement("div");loader.setAttribute("part","loader");const content=this.shadowRoot.querySelector(["[part~=\"content\"]"]);content.parentNode.insertBefore(loader,content)}}customElements.define(vaadin_combo_box_dropdown_ComboBoxOverlayElement.is,vaadin_combo_box_dropdown_ComboBoxOverlayElement);class vaadin_combo_box_dropdown_ComboBoxDropdownElement extends Object(legacy_class.b)(iron_resizable_behavior.a,polymer_element.a){static get template(){return html_tag.a`
    <style>
      :host {
        display: block;
      }

      :host > #overlay {
        display: none;
      }
    </style>
    <vaadin-combo-box-overlay id="overlay" hidden\$="[[hidden]]" opened="[[opened]]" template="{{template}}" style="align-items: stretch; margin: 0;" theme\$="[[theme]]">
      <slot></slot>
    </vaadin-combo-box-overlay>
`}static get is(){return"vaadin-combo-box-dropdown"}static get properties(){return{opened:Boolean,template:{type:Object,notify:!0},positionTarget:{type:Object},alignedAbove:{type:Boolean,value:!1},theme:String}}static get observers(){return["_openedChanged(opened)"]}constructor(){super();this._boundSetPosition=this._setPosition.bind(this);this._boundOutsideClickListener=this._outsideClickListener.bind(this)}connectedCallback(){super.connectedCallback();this.addEventListener("iron-resize",this._boundSetPosition)}ready(){super.ready();this.$.overlay.addEventListener("vaadin-overlay-outside-click",e=>{e.preventDefault()})}disconnectedCallback(){super.disconnectedCallback();this.removeEventListener("iron-resize",this._boundSetPosition);this.opened=!1}notifyResize(){super.notifyResize();if(this.positionTarget&&this.opened){this._setPosition();requestAnimationFrame(this._setPosition.bind(this))}}_openedChanged(opened){if(opened){this.$.overlay.style.position=this._isPositionFixed(this.positionTarget)?"fixed":"absolute";this._setPosition();window.addEventListener("scroll",this._boundSetPosition,!0);document.addEventListener("click",this._boundOutsideClickListener,!0);this.dispatchEvent(new CustomEvent("vaadin-combo-box-dropdown-opened",{bubbles:!0,composed:!0}))}else{window.removeEventListener("scroll",this._boundSetPosition,!0);document.removeEventListener("click",this._boundOutsideClickListener,!0);this.dispatchEvent(new CustomEvent("vaadin-combo-box-dropdown-closed",{bubbles:!0,composed:!0}))}}_outsideClickListener(event){const eventPath=event.composedPath();if(0>eventPath.indexOf(this.positionTarget)&&0>eventPath.indexOf(this.$.overlay)){this.opened=!1}}_isPositionFixed(element){const offsetParent=this._getOffsetParent(element);return"fixed"===window.getComputedStyle(element).position||offsetParent&&this._isPositionFixed(offsetParent)}_getOffsetParent(element){if(element.assignedSlot){return element.assignedSlot.parentElement}else if(element.parentElement){return element.offsetParent}const parent=element.parentNode;if(parent&&11===parent.nodeType&&parent.host){return parent.host}}_verticalOffset(overlayRect,targetRect){return this.alignedAbove?-overlayRect.height:targetRect.height}_shouldAlignAbove(targetRect){const spaceBelow=(window.innerHeight-targetRect.bottom-_Mathmin(document.body.scrollTop,0))/window.innerHeight;return .3>spaceBelow}_setPosition(e){if(e&&e.target){const target=e.target===document?document.body:e.target,parent=this.$.overlay.parentElement;if(!(target.contains(this.$.overlay)||target.contains(this.positionTarget))||parent!==document.body){return}}const targetRect=this.positionTarget.getBoundingClientRect();this.alignedAbove=this._shouldAlignAbove(targetRect);const overlayRect=this.$.overlay.getBoundingClientRect();this._translateX=targetRect.left-overlayRect.left+(this._translateX||0);this._translateY=targetRect.top-overlayRect.top+(this._translateY||0)+this._verticalOffset(overlayRect,targetRect);const _devicePixelRatio=window.devicePixelRatio||1;this._translateX=_Mathround(this._translateX*_devicePixelRatio)/_devicePixelRatio;this._translateY=_Mathround(this._translateY*_devicePixelRatio)/_devicePixelRatio;this.$.overlay.style.transform=`translate3d(${this._translateX}px, ${this._translateY}px, 0)`;this.$.overlay.style.width=this.positionTarget.clientWidth+"px";this.$.overlay.style.justifyContent=this.alignedAbove?"flex-end":"flex-start";this.dispatchEvent(new CustomEvent("position-changed"))}}customElements.define(vaadin_combo_box_dropdown_ComboBoxDropdownElement.is,vaadin_combo_box_dropdown_ComboBoxDropdownElement);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/const TOUCH_DEVICE=(()=>{try{document.createEvent("TouchEvent");return!0}catch(e){return!1}})();class vaadin_combo_box_dropdown_wrapper_ComboBoxDropdownWrapperElement extends class extends polymer_element.a{}{static get template(){return html_tag.a`
    <style>
      #scroller {
        overflow: auto;

        /* Fixes item background from getting on top of scrollbars on Safari */
        transform: translate3d(0, 0, 0);

        /* Enable momentum scrolling on iOS (iron-list v1.2+ no longer does it for us) */
        -webkit-overflow-scrolling: touch;

        /* Fixes scrollbar disappearing when "Show scroll bars: Always" enabled in Safari */
        box-shadow: 0 0 0 white;
      }
    </style>
    <vaadin-combo-box-dropdown id="dropdown" hidden="[[_hidden(_items.*, loading)]]" position-target="[[positionTarget]]" on-template-changed="_templateChanged" on-position-changed="_setOverlayHeight" theme="[[theme]]">
      <template>
        <div id="scroller" on-click="_stopPropagation">
          <iron-list id="selector" role="listbox" items="[[_getItems(opened, _items)]]" scroll-target="[[_scroller]]">
            <template>
              <vaadin-combo-box-item on-click="_onItemClick" index="[[__requestItemByIndex(item, index)]]" item="[[item]]" label="[[getItemLabel(item)]]" selected="[[_isItemSelected(item, _selectedItem, _itemIdPath)]]" renderer="[[renderer]]" role\$="[[_getAriaRole(index)]]" aria-selected\$="[[_getAriaSelected(_focusedIndex,index)]]" focused="[[_isItemFocused(_focusedIndex,index)]]" tabindex="-1" theme\$="[[theme]]">
              </vaadin-combo-box-item>
            </template>
          </iron-list>
        </div>
      </template>
    </vaadin-combo-box-dropdown>
`}static get is(){return"vaadin-combo-box-dropdown-wrapper"}static get properties(){return{touchDevice:{type:Boolean,value:TOUCH_DEVICE},opened:Boolean,positionTarget:{type:Object},renderer:Function,loading:{type:Boolean,value:!1,reflectToAttribute:!0,observer:"_setOverlayHeight"},theme:String,_selectedItem:{type:Object},_items:{type:Object},_focusedIndex:{type:Number,value:-1,observer:"_focusedIndexChanged"},_focusedItem:{type:String,computed:"_getFocusedItem(_focusedIndex)"},_itemLabelPath:{type:String,value:"label"},_itemValuePath:{type:String,value:"value"},_selector:Object,_itemIdPath:String}}static get observers(){return["_selectorChanged(_selector)","_loadingChanged(loading)","_openedChanged(opened, _items, loading)"]}_fireTouchAction(sourceEvent){this.dispatchEvent(new CustomEvent("vaadin-overlay-touch-action",{detail:{sourceEvent:sourceEvent}}))}_getItems(opened,items){return opened?items:[]}_openedChanged(opened,items,loading){this.$.dropdown.opened=!!(opened&&(loading||this.$.dropdown.opened||items&&items.length))}ready(){super.ready();if(/Trident/.test(navigator.userAgent)){this._scroller.setAttribute("unselectable","on")}this.$.dropdown.$.overlay.addEventListener("touchend",e=>this._fireTouchAction(e));this.$.dropdown.$.overlay.addEventListener("touchmove",e=>this._fireTouchAction(e));this.$.dropdown.$.overlay.addEventListener("mousedown",e=>e.preventDefault())}_templateChanged(){this._selector=this.$.dropdown.$.overlay.content.querySelector("#selector");this._scroller=this.$.dropdown.$.overlay.content.querySelector("#scroller")}_loadingChanged(loading){if(loading){this.$.dropdown.$.overlay.setAttribute("loading","")}else{this.$.dropdown.$.overlay.removeAttribute("loading")}}_selectorChanged(){this._patchWheelOverScrolling()}_setOverlayHeight(){if(!this.opened||!this.positionTarget||!this._selector){return}const targetRect=this.positionTarget.getBoundingClientRect();this._scroller.style.maxHeight=(window.ShadyCSS?window.ShadyCSS.getComputedStyleValue(this,"--vaadin-combo-box-overlay-max-height"):getComputedStyle(this).getPropertyValue("--vaadin-combo-box-overlay-max-height"))||"65vh";const maxHeight=this._maxOverlayHeight(targetRect);this.$.dropdown.$.overlay.style.maxHeight=maxHeight;this._selector.style.maxHeight=maxHeight;this.updateViewportBoundaries()}_maxOverlayHeight(targetRect){const margin=8,minHeight=116,bottom=_Mathmin(window.innerHeight,document.body.scrollHeight-document.body.scrollTop);if(this.$.dropdown.alignedAbove){return _Mathmax(targetRect.top-margin+_Mathmin(document.body.scrollTop,0),minHeight)+"px"}else{return _Mathmax(bottom-targetRect.bottom-margin,minHeight)+"px"}}_getFocusedItem(focusedIndex){if(0<=focusedIndex){return this._items[focusedIndex]}}_isItemSelected(item,selectedItem,itemIdPath){if(item instanceof ComboBoxPlaceholder){return!1}else if(itemIdPath&&item!==void 0&&selectedItem!==void 0){return this.get(itemIdPath,item)===this.get(itemIdPath,selectedItem)}else{return item===selectedItem}}_onItemClick(e){if(e.detail&&e.detail.sourceEvent&&e.detail.sourceEvent.stopPropagation){this._stopPropagation(e.detail.sourceEvent)}this.dispatchEvent(new CustomEvent("selection-changed",{detail:{item:e.model.item}}))}indexOfLabel(label){if(this._items&&label){for(let i=0;i<this._items.length;i++){if(this.getItemLabel(this._items[i]).toString().toLowerCase()===label.toString().toLowerCase()){return i}}}return-1}__requestItemByIndex(item,index){if(item instanceof ComboBoxPlaceholder&&index!==void 0){this.dispatchEvent(new CustomEvent("index-requested",{detail:{index}}))}return index}getItemLabel(item){let label=item?this.get(this._itemLabelPath,item):void 0;if(label===void 0||null===label){label=item?item.toString():""}return label}_isItemFocused(focusedIndex,itemIndex){return focusedIndex==itemIndex}_getAriaSelected(focusedIndex,itemIndex){return this._isItemFocused(focusedIndex,itemIndex).toString()}_getAriaRole(itemIndex){return itemIndex!==void 0?"option":!1}_focusedIndexChanged(index){if(0<=index){this._scrollIntoView(index)}}_scrollIntoView(index){const visibleItemsCount=this._visibleItemsCount();if(visibleItemsCount===void 0){return}let targetIndex=index;if(index>this._selector.lastVisibleIndex-1){targetIndex=index-visibleItemsCount+1}else if(index>this._selector.firstVisibleIndex){targetIndex=this._selector.firstVisibleIndex}this._selector.scrollToIndex(_Mathmax(0,targetIndex));const pidx=this._selector._getPhysicalIndex(index),physicalItem=this._selector._physicalItems[pidx];if(!physicalItem){return}const physicalItemRect=physicalItem.getBoundingClientRect(),scrollerRect=this._scroller.getBoundingClientRect(),scrollTopAdjust=physicalItemRect.bottom-scrollerRect.bottom+this._viewportTotalPaddingBottom;if(0<scrollTopAdjust){this._scroller.scrollTop+=scrollTopAdjust}}ensureItemsRendered(){this._selector._render()}adjustScrollPosition(){if(this.opened&&this._items){this._scrollIntoView(this._focusedIndex)}}_patchWheelOverScrolling(){const selector=this._selector;selector.addEventListener("wheel",e=>{const scroller=selector._scroller||selector.scrollTarget,scrolledToTop=0===scroller.scrollTop,scrolledToBottom=1>=scroller.scrollHeight-scroller.scrollTop-scroller.clientHeight;if(scrolledToTop&&0>e.deltaY){e.preventDefault()}else if(scrolledToBottom&&0<e.deltaY){e.preventDefault()}})}updateViewportBoundaries(){this._cachedViewportTotalPaddingBottom=void 0;this._selector.updateViewportBoundaries()}get _viewportTotalPaddingBottom(){if(this._cachedViewportTotalPaddingBottom===void 0){const itemsStyle=window.getComputedStyle(this._selector.$.items);this._cachedViewportTotalPaddingBottom=[itemsStyle.paddingBottom,itemsStyle.borderBottomWidth].map(v=>{return parseInt(v,10)}).reduce((sum,v)=>{return sum+v})}return this._cachedViewportTotalPaddingBottom}_visibleItemsCount(){if(!this._selector){return}this._selector.flushDebouncer("_debounceTemplate");this._selector.scrollToIndex(this._selector.firstVisibleIndex);this.updateViewportBoundaries();return this._selector.lastVisibleIndex-this._selector.firstVisibleIndex+1}_selectItem(item){item="number"===typeof item?this._items[item]:item;if(this._selector.selectedItem!==item){this._selector.selectItem(item)}}_preventDefault(e){if(e.cancelable){e.preventDefault()}}_stopPropagation(e){e.stopPropagation()}_hidden(){return!this.loading&&(!this._items||!this._items.length)}}customElements.define(vaadin_combo_box_dropdown_wrapper_ComboBoxDropdownWrapperElement.is,vaadin_combo_box_dropdown_wrapper_ComboBoxDropdownWrapperElement);var case_map=__webpack_require__(15);/**
@license
Copyright (c) 2017 Vaadin Ltd.
This program is available under Apache License Version 2.0, available at https://vaadin.com/license/
*/class vaadin_combo_box_light_ComboBoxLightElement extends Object(vaadin_theme_property_mixin.a)(Object(vaadin_themable_mixin.a)(ComboBoxDataProviderMixin(ComboBoxMixin(polymer_element.a)))){static get template(){return html_tag.a`
    <slot></slot>

    <vaadin-combo-box-dropdown-wrapper id="overlay" opened="[[opened]]" position-target="[[inputElement]]" renderer="[[renderer]]" _focused-index="[[_focusedIndex]]" _item-id-path="[[itemIdPath]]" _item-label-path="[[itemLabelPath]]" loading="[[loading]]" theme="[[theme]]">
    </vaadin-combo-box-dropdown-wrapper>
`}static get is(){return"vaadin-combo-box-light"}static get properties(){return{attrForValue:{type:String,value:"value"},inputElement:{type:Element,readOnly:!0}}}constructor(){super();this._boundInputValueChanged=this._inputValueChanged.bind(this)}ready(){super.ready();this._toggleElement=this.querySelector(".toggle-button");this._clearElement=this.querySelector(".clear-button")}get focused(){return this.getRootNode().activeElement===this.inputElement}connectedCallback(){super.connectedCallback();this._setInputElement(this.querySelector("vaadin-text-field,iron-input,paper-input,.paper-input-input,.input"));this._revertInputValue();this.inputElement.addEventListener("input",this._boundInputValueChanged);this._preventInputBlur()}disconnectedCallback(){super.disconnectedCallback();this.inputElement.removeEventListener("input",this._boundInputValueChanged);this._restoreInputBlur()}get _propertyForValue(){return Object(case_map.b)(this.attrForValue)}get _inputElementValue(){return this.inputElement&&this.inputElement[this._propertyForValue]}set _inputElementValue(value){if(this.inputElement){this.inputElement[this._propertyForValue]=value}}}customElements.define(vaadin_combo_box_light_ComboBoxLightElement.is,vaadin_combo_box_light_ComboBoxLightElement)}}]);
//# sourceMappingURL=2b7842ad636c465443ee.chunk.js.map
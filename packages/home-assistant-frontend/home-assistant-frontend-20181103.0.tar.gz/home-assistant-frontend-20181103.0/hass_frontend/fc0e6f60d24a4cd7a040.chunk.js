(window.webpackJsonp=window.webpackJsonp||[]).push([[35],{307:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_iron_image_iron_image__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(166),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(0),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(4),_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(16);class HaEntityMarker extends Object(_mixins_events_mixin__WEBPACK_IMPORTED_MODULE_3__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__.a`
    <style include="iron-positioning"></style>
    <style>
    .marker {
      vertical-align: top;
      position: relative;
      display: block;
      margin: 0 auto;
      width: 2.5em;
      text-align: center;
      height: 2.5em;
      line-height: 2.5em;
      font-size: 1.5em;
      border-radius: 50%;
      border: 0.1em solid var(--ha-marker-color, var(--default-primary-color));
      color: rgb(76, 76, 76);
      background-color: white;
    }
    iron-image {
      border-radius: 50%;
    }
    </style>

    <div class="marker">
      <template is="dom-if" if="[[entityName]]">[[entityName]]</template>
      <template is="dom-if" if="[[entityPicture]]">
        <iron-image sizing="cover" class="fit" src="[[entityPicture]]"></iron-image>
      </template>
    </div>
`}static get properties(){return{hass:{type:Object},entityId:{type:String,value:""},entityName:{type:String,value:null},entityPicture:{type:String,value:null}}}ready(){super.ready();this.addEventListener("click",ev=>this.badgeTap(ev))}badgeTap(ev){ev.stopPropagation();if(this.entityId){this.fire("hass-more-info",{entityId:this.entityId})}}}customElements.define("ha-entity-marker",HaEntityMarker)},308:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return setupLeafletMap});var leaflet__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(276),leaflet__WEBPACK_IMPORTED_MODULE_0___default=__webpack_require__.n(leaflet__WEBPACK_IMPORTED_MODULE_0__);function setupLeafletMap(mapElement){const map=leaflet__WEBPACK_IMPORTED_MODULE_0___default.a.map(mapElement),style=document.createElement("link");style.setAttribute("href","/static/images/leaflet/leaflet.css");style.setAttribute("rel","stylesheet");mapElement.parentNode.appendChild(style);map.setView([51.505,-.09],13);leaflet__WEBPACK_IMPORTED_MODULE_0___default.a.tileLayer(`https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}${leaflet__WEBPACK_IMPORTED_MODULE_0___default.a.Browser.retina?"@2x.png":".png"}`,{attribution:"&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>, &copy; <a href=\"https://carto.com/attributions\">CARTO</a>",subdomains:"abcd",minZoom:0,maxZoom:20}).addTo(map);return map}},704:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(121),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(0),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(4),leaflet__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(276),leaflet__WEBPACK_IMPORTED_MODULE_3___default=__webpack_require__.n(leaflet__WEBPACK_IMPORTED_MODULE_3__),_components_ha_menu_button__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(134),_components_ha_icon__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(88),_ha_entity_marker__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(307),_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(23),_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(27),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(10),_common_dom_setup_leaflet_map__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(308);leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.Icon.Default.imagePath="/static/images/leaflet";class HaPanelMap extends Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_9__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_2__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_1__.a`
    <style include="ha-style">
      #map {
        height: calc(100% - 64px);
        width: 100%;
        z-index: 0;
      }
    </style>

    <app-toolbar>
      <ha-menu-button narrow='[[narrow]]' show-menu='[[showMenu]]'></ha-menu-button>
      <div main-title>[[localize('panel.map')]]</div>
    </app-toolbar>

    <div id='map'></div>
    `}static get properties(){return{hass:{type:Object,observer:"drawEntities"},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1}}}connectedCallback(){super.connectedCallback();var map=this._map=Object(_common_dom_setup_leaflet_map__WEBPACK_IMPORTED_MODULE_10__.a)(this.$.map);this.drawEntities(this.hass);setTimeout(()=>{map.invalidateSize();this.fitMap()},1)}disconnectedCallback(){if(this._map){this._map.remove()}}fitMap(){var bounds;if(0===this._mapItems.length){this._map.setView(new leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.LatLng(this.hass.config.latitude,this.hass.config.longitude),14)}else{bounds=new leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.latLngBounds(this._mapItems.map(item=>item.getLatLng()));this._map.fitBounds(bounds.pad(.5))}}drawEntities(hass){var map=this._map;if(!map)return;if(this._mapItems){this._mapItems.forEach(function(marker){marker.remove()})}var mapItems=this._mapItems=[];Object.keys(hass.states).forEach(function(entityId){var entity=hass.states[entityId],title=Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(entity);if(entity.attributes.hidden&&"zone"!==Object(_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_7__.a)(entity)||"home"===entity.state||!("latitude"in entity.attributes)||!("longitude"in entity.attributes)){return}var icon;if("zone"===Object(_common_entity_compute_state_domain__WEBPACK_IMPORTED_MODULE_7__.a)(entity)){if(entity.attributes.passive)return;var iconHTML="";if(entity.attributes.icon){const el=document.createElement("ha-icon");el.setAttribute("icon",entity.attributes.icon);iconHTML=el.outerHTML}else{iconHTML=title}icon=leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.divIcon({html:iconHTML,iconSize:[24,24],className:""});mapItems.push(leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.marker([entity.attributes.latitude,entity.attributes.longitude],{icon:icon,interactive:!1,title:title}).addTo(map));mapItems.push(leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.circle([entity.attributes.latitude,entity.attributes.longitude],{interactive:!1,color:"#FF9800",radius:entity.attributes.radius}).addTo(map));return}var entityPicture=entity.attributes.entity_picture||"",entityName=title.split(" ").map(function(part){return part.substr(0,1)}).join("");icon=leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.divIcon({html:"<ha-entity-marker entity-id='"+entity.entity_id+"' entity-name='"+entityName+"' entity-picture='"+entityPicture+"'></ha-entity-marker>",iconSize:[45,45],className:""});mapItems.push(leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.marker([entity.attributes.latitude,entity.attributes.longitude],{icon:icon,title:Object(_common_entity_compute_state_name__WEBPACK_IMPORTED_MODULE_8__.a)(entity)}).addTo(map));if(entity.attributes.gps_accuracy){mapItems.push(leaflet__WEBPACK_IMPORTED_MODULE_3___default.a.circle([entity.attributes.latitude,entity.attributes.longitude],{interactive:!1,color:"#0288D1",radius:entity.attributes.gps_accuracy}).addTo(map))}})}}customElements.define("ha-panel-map",HaPanelMap)}}]);
//# sourceMappingURL=fc0e6f60d24a4cd7a040.chunk.js.map
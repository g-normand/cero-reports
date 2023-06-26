<template>
  <b-container fluid class="h-100 d-flex flex-column">
    <b-row class="flex-grow-1">
      <l-map
        :bounds="bounds"
        @update:bounds="boundsUpdated"
        :options="{ zoomControl: false, preferCanvas: true }"
        ref="map"
      >
        <l-control-layers position="topright"></l-control-layers>
        <l-control position="topleft">
          <b-button v-b-toggle.sidebar-1><b-icon-layout-sidebar-inset></b-icon-layout-sidebar-inset></b-button>
        </l-control>
        <l-tile-layer
          v-for="tileProvider in tileProviders"
          :key="tileProvider.name"
          :name="tileProvider.name"
          :visible="tileProvider.visible"
          :url="tileProvider.url"
          :attribution="tileProvider.attribution"
          layer-type="base"
        />
        <l-control-zoom position="bottomright"></l-control-zoom>
        <v-marker-cluster
          :options="{
            showCoverageOnHover: false,
            maxClusterRadius: 50,
            iconCreateFunction: iconCreateFunction,
          }"
        >
          <l-marker
            ref="markers"
            :options="{ count: loc.obs.length }"
            :name="loc.locId + loc.obs.map((x) => x.speciesCode).join('_')"
            v-for="loc in locationFiltered"
           :key="loc.locId"
            :lat-lng="loc.latLng"
            @click="clickMarker(loc)"
            :icon="getIcon(loc)"
          >
          </l-marker>
        </v-marker-cluster>

        <l-marker ref="marker" v-if="popup != false" :lat-lng="popup.latLng">
          <l-icon
            :popup-anchor="[0, -34]"
            :icon-anchor="[12.5, 34]"
            :icon-size="[25, 34]"
          />
          <l-popup :options="{ width: 600 }">
            <div class="mb-2 d-flex justify-content-between align-items-center">
              <span>
                <a
                  v-bind:href="'https://ebird.org/hotspot/' + popup.locId"
                  target="_blank"
                  title="eBird hotspot"
                  v-if="popup.locId.startsWith('L')"
                  >{{ popup.locName }}</a
                >
                <span v-else>{{ popup.locName }}</span>
              </span>
              <span>
                <a
                  v-bind:href="
                    'https://www.google.com/maps/search/?api=1&query=' + popup.latLng.lat + ',' + popup.latLng.lng
                  "
                  target="_blank"
                  title="direction on google map"
                >
                  <font-awesome-icon icon="directions" class="ml-2" />
                </a>
              </span>
            </div>
            <div>
              <b-card no-body v-for="spe in popup.sp" :key="spe.speciesCode" class="mx-0 mb-1">
                <b-card-header class="p-1 d-flex justify-content-between align-items-center">
                  <span>
                    {{ spe.comName }}
                    <b-badge v-if="(spe.aba >= 3) & (spe.aba <= 6)" :class="'ml-2 font-weight-normal bg-aba-' + spe.aba"
                      >ABA-{{ spe.aba }}</b-badge
                    >
                  </span>
                  <b-badge pill style="background-color: #343a40">{{ spe.obs.length }}</b-badge>
                </b-card-header>
                <b-list-group flush class="mh-240">
                  <b-list-group-item v-for="obs in spe.obs" :key="obs.subId" class="py-1 px-0 hover-darken">
                    <b-col class="d-flex w-100 justify-content-between">
                      <small>
                        <a v-if="obs.subId"
                          v-bind:href="'https://ebird.org/checklist/' + obs.subId + '#' + spe.speciesCode"
                          target="_blank"
                        >
                          {{ obs.obsDt }}, {{ obs.howMany }} ind. {{ obs.userDisplayName }}
                        </a>
                        <span v-if="!obs.subId">{{ obs.obsDt }}, {{ obs.howMany }} ind. {{ obs.userDisplayName }}</span>
                      </small>
                      <span v-if="obs.hasRichMedia | obs.hasComments">
                        <span v-if="obs.hasRichMedia">
                          <small>
                            <b-icon-camera-fill class="mr-1" @click="addMedia(obs.obsId)" />
                          </small>
                        </span>
                        <span v-if="obs.hasComments">
                          <small><b-icon-chat-square-text-fill></b-icon-chat-square-text-fill></small>
                        </span>
                      </span>
                    </b-col>
                  </b-list-group-item>
                </b-list-group>
              </b-card>
            </div>
          </l-popup>
        </l-marker>

      </l-map>

      <b-sidebar id="sidebar-1" title="Official rare sightings of Ecuador" visible shadow>
        <b-overlay :show="showOverlay" rounded="sm">
          <div class="px-3 py-2">
            This map shows the official rare sightings in Ecuador according to the last CERO report published in 2021.<br />
            You can find the report here :  
            <b-form>
             <a href="https://revistas.usfq.edu.ec/index.php/reo/article/view/2856">6th report</a>
            </b-form>
            <br />

            List of the other CERO reports :
            <b-form>
             <a href="https://revistas.usfq.edu.ec/index.php/reo/article/view/1990">5th report</a>
            </b-form>
            <b-form>
             <a href="https://revistas.usfq.edu.ec/index.php/reo/article/view/1277">4th report</a>
            </b-form>
            <b-form>
             <a href="https://revistas.usfq.edu.ec/index.php/reo/article/view/446">3rd report</a>
            </b-form>
          </div>
        </b-overlay>
        <template #footer>
          <div class="d-flex bg-dark text-light align-items-center px-3 py-2 w-100 justify-content-between">
            Inspired by 
            <a href="https://zoziologie.raphaelnussbaumer.com/global-rare-ebird/" target="_blank" title="zoziologie.com"
              ><b-img :src="logo_zoziologie" class="zozio"></b-img
            ></a>
          </div>
        </template>
      </b-sidebar>
    </b-row>
  </b-container>
</template>

<script>
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "leaflet/dist/images/marker-shadow.png";

import "vue-multiselect/dist/vue-multiselect.min.css";

import "./style.scss";

import { latLngBounds, latLng } from "leaflet";
import {
  LMap,
  LTileLayer,
  LControlLayers,
  LControl,
  LControlZoom,
  LMarker,
  LPopup,
  LIcon,
  LCircle,
  LCircleMarker,
} from "vue2-leaflet";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";
import obs_list from "./assets/obs_list.json";
import logo_zoziologie from "./assets/logo_zoziologie.svg";


export default {
  components: {
    LMap,
    LTileLayer,
    LControlLayers,
    LControl,
    LControlZoom,
    LMarker,
    LPopup,
    LIcon,
    LCircle,
    LCircleMarker,
    "v-marker-cluster": Vue2LeafletMarkerCluster,
  },
  data() {
    return {
      logo_zoziologie: logo_zoziologie,
      location: null,
      bounds: latLngBounds([
        [10, -80],
        [-15, -100],
      ]),
      tileProviders: [
        {
          name: "OpenStreetMap",
          visible: true,
          attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        },
        {
          name: "Mapbox.Streets",
          visible: false,
          url: "https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmFmbnVzcyIsImEiOiIzMVE1dnc0In0.3FNMKIlQ_afYktqki-6m0g",
          attribution: "",
        },
        {
          name: "Mapbox.Satellite",
          visible: false,
          url: "https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmFmbnVzcyIsImEiOiIzMVE1dnc0In0.3FNMKIlQ_afYktqki-6m0g",
          attribution: "",
        },
        {
          name: "Esri.WorldImagery",
          visible: false,
          url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          attribution:
            "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
        },
      ],
      debounce_time: 200,
      observationsRegion: [],
      obs_list: obs_list,
      showOverlay: false,
      popup: false,
      copy_status: "...",
    };
  },
  mounted() {
    this.showOverlay = true;
    this.observationsRegion.push(...this.processObs(this.obs_list));
    if (this.observationsRegion.length > 0) {
      this.$refs.map.mapObject.fitBounds(this.observationsRegion.map((m) => m.latLng));
    }
    this.showOverlay = false;
  },
  methods: {
    boundsUpdated(bounds) {
      this.bounds = bounds;
    },  
    processObs(obs) {
      // This filtering is due when using detail=full in api. Maybe because of adding comments/media later? Need to check, but it would be then worth filtering more
      var id = obs.map((item) => item.speciesCode + item.obsDt + item.subId);
      obs = obs.filter((val, index) => id.indexOf(val.speciesCode + val.obsDt + val.subId) === index);
      obs = obs.map((e) => {
        let o = {};
        o.regionCode = 'EC';
        o.comName = e.comName;
        o.sciName = e.sciName;
        o.speciesCode = e.speciesCode;
        o.howMany = e.howMany ? e.howMany : "x";
        o.locId = e.locId;
        o.subId = e.subId;
        o.locName = e.locName;
        o.locationPrivate = e.locationPrivate;
        o.obsDt = e.obsDt;
        o.latLng = latLng(e.lat, e.lng);

        // Following only present with detail=full in url but we found a way around for all of them
        o.obsId = e.obsId;
        o.userDisplayName = "userDisplayName" in e ? "(" + e.userDisplayName + ")" : "";
        o.hasComments = e.hasComments;
        o.hasRichMedia = e.hasRichMedia;
        console.log(o);
        return o;
      });
      return obs;
    },
    mouseHoverList(markerID) {
      this.$refs.markers.forEach(function (m) {
        if (m.name.includes(markerID)) {
          m.setVisible(true);
        } else {
          m.setVisible(false);
        }
      });
    },
    mouseOutList() {
      this.$refs.markers.forEach(function (m) {
        m.setVisible(true);
      });
    },
    calcCrow(lat1, lon1, lat2, lon2) {
      //This function takes in latitude and longitude of two location and returns the distance between them as the crow flies (in km)
      var R = 6371; // km
      var dLat = this.toRad(lat2 - lat1);
      var dLon = this.toRad(lon2 - lon1);
      var lat1rad = this.toRad(lat1);
      var lat2rad = this.toRad(lat2);

      var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1rad) * Math.cos(lat2rad);
      var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      var d = R * c;
      return d;
    },
    toRad(Value) {
      // Converts numeric degrees to radians
      return (Value * Math.PI) / 180;
    },
    clickMarker(loc) {
      loc.sp = loc.obs.reduce(function (r, i) {
        r[i.speciesCode] = r[i.speciesCode] || {
         obs: [],
          comName: i.comName,
          speciesCode: i.speciesCode,
          aba: i.aba,
        };
       r[i.speciesCode].obs.push(i);
        return r;
      }, {});
      this.popup = loc;
      setTimeout(() => this.$refs.marker.mapObject.openPopup(), 100);
    },
    getIcon(loc) {
      return L.divIcon({
        className: "my-custom-icon",
        popupAnchor: [0, -34],
        iconAnchor: [12.5, 34],
        iconSize: [25, 34],
        html: `
        <?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 33"><path class="${
          loc.locationPrivate ? "marker-perso" : "marker-hotspot"
        }" d="m12.02,32.98c-.32,0-.81-.11-1.29-.67-3.01-3.51-5.41-6.84-7.31-10.17-1.45-2.54-2.39-4.71-2.95-6.8C-.5,11.74.04,8.37,2.05,5.34,3.77,2.76,6.19,1.06,9.23.33c.43-.1.87-.17,1.31-.23.19-.03.39-.06.58-.09h1.69c.27.03.47.06.66.09.44.06.88.13,1.31.23,3.4.85,6.01,2.85,7.75,5.95.85,1.53,1.35,3.25,1.45,5.12.15,2.62-.66,4.95-1.38,6.69-1.24,2.97-2.98,5.97-5.34,9.17-1.02,1.39-2.12,2.75-3.19,4.06l-.79.99c-.46.57-.94.69-1.27.69v-.02Z"/>
        <text x="50%" y="50%" class="marker-text"  dominant-baseline="middle" text-anchor="middle">${
          loc.obs.length
        }</text></svg>`,
      });
    },
    iconCreateFunction: function (cluster) {
      var childCount = cluster.getAllChildMarkers().reduce((acc, x) => acc + x.options.count, 0);
      var c = " marker-cluster-";
      if (childCount < 10) {
        c += "small";
      } else if (childCount < 100) {
        c += "medium";
      } else {
        c += "large";
      }

      return new L.DivIcon({
        html: "<div><span>" + childCount + "</span></div>",
        className: "marker-cluster" + c,
        iconSize: new L.Point(40, 40),
      });
    },
  },
  computed: {
    locationFiltered: function () {
      return this.observationsRegion.reduce(function (r, i) {
        r[i.locId] = r[i.locId] || {
          obs: [],
          count: 0,
          locName: i.locName,
          locationPrivate: i.locationPrivate,
         regionCode: i.regionCode,
          latLng: i.latLng,
          locId: i.locId,
        };
        r[i.locId].obs.push(i);
        r[i.locId].count = r[i.locId].count + 1;
        return r;
      }, {});
    },
  }
};
</script>

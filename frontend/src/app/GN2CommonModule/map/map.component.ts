import { Component, Input, OnInit, ViewChild, OnChanges, Injectable } from '@angular/core';
import { MapService } from './map.service';
import { Map, LatLngExpression } from 'leaflet';
import { HttpClient, HttpParams } from '@angular/common/http';
import * as L from 'leaflet';

import { CommonService } from '../service/common.service';
import { ConfigService } from '@geonature/utils/configModule/core';

import 'leaflet-draw';
import { FormControl } from '@angular/forms';
import { Observable, of } from 'rxjs';
import {
  catchError,
  debounceTime,
  distinctUntilChanged,
  tap,
  switchMap,
  map
} from 'rxjs/operators';

const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
const PARAMS = new HttpParams({
  fromObject: {
    format: 'json',
    limit: '10',
    polygon_geojson: '1'
  }
});

@Injectable()
export class NominatimService {
  constructor(private http: HttpClient) {}

  search(term: string) {
    if (term === '') {
      return of([]);
    }

    return this.http.get(NOMINATIM_URL, { params: PARAMS.set('q', term) }).pipe(map(res => res));
  }
}

/**
 * Ce composant affiche une carte Leaflet ainsi qu'un outil de recherche de lieux dits et d'adresses (basé sur l'API OpenStreetMap).
 * @example
 * <pnx-map [center]="center" [zoom]="zoom"> </pnx-map>`
 */
@Component({
  selector: 'pnx-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
  providers: [NominatimService]
})
export class MapComponent implements OnInit {
  /**
   *  coordonnées du centrage de la carte: [long,lat]
   */
  @Input() center: Array<number>;
  /** Niveaux de zoom à l'initialisation de la carte */
  @Input() zoom: number;
  /** Hauteur de la carte (obligatoire) */
  @Input() height: string;
  /** Activer la barre de recherche */
  @Input() searchBar: boolean = true;
  searchLocation: string;
  public searching = false;
  public searchFailed = false;
  public locationControl = new FormControl();
  public map: Map;
  constructor(
    private mapService: MapService,
    private _commonService: CommonService,
    private _http: HttpClient,
    private _nominatim: NominatimService,
    private _configService: ConfigService
  ) {
    this.searchLocation = '';
  }

  ngOnInit() {
    this.zoom = this.zoom || this._configService.getSettings('MAPCONFIG.ZOOM_LEVEL');
    this.initialize();
  }

  search = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      tap(() => (this.searching = true)),
      switchMap(term =>
        this._nominatim.search(term).pipe(
          tap(() => (this.searchFailed = false)),
          catchError(() => {
            this._commonService.translateToaster('Warning', 'Map.LocationError');
            this.searchFailed = true;
            return of([]);
          })
        )
      ),
      tap(() => (this.searching = false))
    );

  onResultSelected(nomatimObject) {
    const geojson = L.geoJSON(nomatimObject.item.geojson);
    this.map.fitBounds(geojson.getBounds());
  }

  initialize() {
    let center: LatLngExpression;
    if (this.center !== undefined) {
      center = L.latLng(this.center[0], this.center[1]);
    } else {
      center = L.latLng(
        this._configService.getSettings('MAPCONFIG.CENTER')[0],
        this._configService.getSettings('MAPCONFIG.CENTER')[1]
      );
    }

    const createdMap = L.map('map', {
      zoomControl: false,
      center: center,
      zoom: this.zoom,
      preferCanvas: true
    });
    this.map = createdMap;
    (createdMap as any)._onResize();

    L.control.zoom({ position: 'topright' }).addTo(createdMap);
    const baseControl = {};
    this._configService.getSettings('MAPCONFIG.BASEMAP').forEach((basemap, index) => {
      const configObj = (basemap as any).subdomains
        ? { attribution: basemap.attribution, subdomains: (basemap as any).subdomains }
        : { attribution: basemap.attribution };
      baseControl[basemap.name] = L.tileLayer(basemap.layer, configObj);
      if (index === 0) {
        createdMap.addLayer(baseControl[basemap.name]);
      }
    });
    this.mapService.layerControl = L.control.layers(baseControl);
    this.mapService.layerControl.addTo(createdMap);
    L.control.scale().addTo(createdMap);

    this.mapService.setMap(createdMap);
    this.mapService.initializeLeafletDrawFeatureGroup();
  }

  formatter(nominatim) {
    return nominatim.display_name;
  }
}

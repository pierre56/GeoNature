import { Injectable } from "@angular/core";
import { HttpClient, HttpParams, HttpHeaders } from "@angular/common/http";

import { DataFormService } from "@geonature_common/form/data-form.service";
import { ConfigService } from "@geonature/utils/configModule/core";

@Injectable()
export class OccHabDataService {
  public ASBSOLUTE_MODULE_URL: string;
  constructor(
    private _http: HttpClient,
    private _gnDataService: DataFormService,
    private _configService: ConfigService
  ) {
    this.ASBSOLUTE_MODULE_URL =
      this._configService.getSettings("API_ENDPOINT") +
      "/" +
      this._configService.getSettings("OCCHAB.MODULE_URL");
  }

  postStation(data) {
    return this._http.post(`${this.ASBSOLUTE_MODULE_URL}/station`, data);
  }

  getStations(params?) {
    let queryString: HttpParams = new HttpParams();
    for (let key in params) {
      if (params[key]) {
        queryString = queryString.set(key, params[key]);
      }
    }
    return this._http.get<any>(`${this.ASBSOLUTE_MODULE_URL}/stations`, {
      params: queryString
    });
  }

  getOneStation(idStation) {
    return this._http.get<any>(
      `${this.ASBSOLUTE_MODULE_URL}/station/${idStation}`
    );
  }

  deleteOneStation(idStation) {
    return this._http.delete<any>(
      `${this.ASBSOLUTE_MODULE_URL}/station/${idStation}`
    );
  }

  exportStations(export_format, idsStation?: Array<number>) {
    const sub = this._http.post(
      `${this.ASBSOLUTE_MODULE_URL}/export_stations/${export_format}`,
      { idsStation: idsStation },
      {
        observe: "events",
        responseType: "blob",
        reportProgress: true
      }
    );
    this._gnDataService.subscribeAndDownload(sub, "export_hab", export_format);
  }
}
